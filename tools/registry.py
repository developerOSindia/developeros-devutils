"""
DeveloperOS Tool Plugin Contract & Module Registry.
Provides clean plug-and-play registration for utilities without complex framework bloat.
"""

from dataclasses import dataclass, field
from typing import Callable, List, Dict, Any, Optional


@dataclass
class ToolDefinition:
    """Standardized metadata and execution contract for DeveloperOS utilities."""
    id: str
    name: str
    description: str
    category: str
    version: str
    ui_entrypoint: Callable[[], None]
    core_module: str
    input_output_spec: Dict[str, Any]
    privacy_classification: str
    dependency_requirements: List[str]
    deployment_support: List[str]
    documentation_link: str
    related_tools: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        """Validates contract conformity."""
        errors = []
        if not self.id or not self.id.startswith("tool-"):
            errors.append("id must start with 'tool-'")
        if not self.name:
            errors.append("name cannot be empty")
        if not self.description:
            errors.append("description cannot be empty")
        if not self.category:
            errors.append("category cannot be empty")
        if not self.version:
            errors.append("version cannot be empty")
        if not callable(self.ui_entrypoint):
            errors.append("ui_entrypoint must be callable")
        if not self.core_module:
            errors.append("core_module cannot be empty")
        if self.privacy_classification not in ["client_side", "ephemeral", "hybrid"]:
            errors.append("privacy_classification must be 'client_side', 'ephemeral', or 'hybrid'")
        return errors


class ToolRegistry:
    """Thread-safe, module-level registry for tool plug-and-play lifecycle."""

    def __init__(self):
        self._tools: Dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        """Registers a tool definition. Raises ValueError on contract violation."""
        errors = tool.validate()
        if errors:
            raise ValueError(f"Failed to register '{tool.id}': {', '.join(errors)}")
        self._tools[tool.id] = tool

    def unregister(self, tool_id: str) -> Optional[ToolDefinition]:
        """Safely removes a tool without breaking suite execution."""
        return self._tools.pop(tool_id, None)

    def get(self, tool_id: str) -> Optional[ToolDefinition]:
        """Fetches tool definition by ID."""
        return self._tools.get(tool_id)

    def list_all(self) -> List[ToolDefinition]:
        """Returns all registered tools ordered by category and name."""
        return sorted(self._tools.values(), key=lambda t: (t.category, t.name))

    def get_categories(self) -> List[str]:
        """Returns all unique category names."""
        return sorted(list({t.category for t in self._tools.values()}))

    def filter(
        self,
        category: Optional[str] = None,
        search_query: Optional[str] = None
    ) -> List[ToolDefinition]:
        """Filters registered tools by category and search keyword."""
        results = self.list_all()
        if category and category != "All Categories":
            results = [t for t in results if t.category == category]
        if search_query and search_query.strip():
            q = search_query.strip().lower()
            results = [
                t for t in results
                if q in t.name.lower() or q in t.description.lower() or q in t.id.lower()
            ]
        return results

    def clear(self) -> None:
        """Clears all registered tools (used primarily during testing)."""
        self._tools.clear()


# Global Singleton Registry
registry = ToolRegistry()


def register_tool(tool: ToolDefinition) -> ToolDefinition:
    """Helper function to register a tool into the global singleton registry."""
    registry.register(tool)
    return tool
