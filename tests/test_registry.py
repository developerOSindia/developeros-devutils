"""
Unit tests for tools.registry plugin contract & lifecycle.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools.registry import ToolRegistry, ToolDefinition


class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.reg = ToolRegistry()

    def test_register_valid_tool(self):
        tool = ToolDefinition(
            id="tool-mock",
            name="Mock Tool",
            description="A test mock tool",
            category="Testing",
            version="1.0.0",
            ui_entrypoint=lambda: None,
            core_module="core.mock",
            input_output_spec={"input": "text", "output": "text"},
            privacy_classification="client_side",
            dependency_requirements=[],
            deployment_support=["streamlit"],
            documentation_link="https://developeros.in",
            related_tools=[]
        )
        self.reg.register(tool)
        self.assertEqual(len(self.reg.list_all()), 1)
        self.assertEqual(self.reg.get("tool-mock").name, "Mock Tool")

    def test_invalid_contract_id(self):
        # ID must start with 'tool-'
        tool = ToolDefinition(
            id="invalid-id",
            name="Invalid",
            description="desc",
            category="cat",
            version="1.0.0",
            ui_entrypoint=lambda: None,
            core_module="core.mock",
            input_output_spec={},
            privacy_classification="client_side",
            dependency_requirements=[],
            deployment_support=[],
            documentation_link=""
        )
        with self.assertRaises(ValueError):
            self.reg.register(tool)

    def test_unregister_tool(self):
        tool = ToolDefinition(
            id="tool-sample",
            name="Sample",
            description="desc",
            category="SampleCat",
            version="1.0.0",
            ui_entrypoint=lambda: None,
            core_module="core.mock",
            input_output_spec={},
            privacy_classification="client_side",
            dependency_requirements=[],
            deployment_support=[],
            documentation_link=""
        )
        self.reg.register(tool)
        self.assertIsNotNone(self.reg.get("tool-sample"))
        removed = self.reg.unregister("tool-sample")
        self.assertEqual(removed.id, "tool-sample")
        self.assertIsNone(self.reg.get("tool-sample"))

    def test_filter_tools(self):
        t1 = ToolDefinition(
            id="tool-a", name="Apple Tool", description="Alpha", category="Fruit",
            version="1.0.0", ui_entrypoint=lambda: None, core_module="core.a",
            input_output_spec={}, privacy_classification="client_side",
            dependency_requirements=[], deployment_support=[], documentation_link=""
        )
        t2 = ToolDefinition(
            id="tool-b", name="Banana Tool", description="Beta", category="Fruit",
            version="1.0.0", ui_entrypoint=lambda: None, core_module="core.b",
            input_output_spec={}, privacy_classification="client_side",
            dependency_requirements=[], deployment_support=[], documentation_link=""
        )
        t3 = ToolDefinition(
            id="tool-c", name="Carrot Tool", description="Gamma", category="Vegetable",
            version="1.0.0", ui_entrypoint=lambda: None, core_module="core.c",
            input_output_spec={}, privacy_classification="client_side",
            dependency_requirements=[], deployment_support=[], documentation_link=""
        )
        self.reg.register(t1)
        self.reg.register(t2)
        self.reg.register(t3)

        fruits = self.reg.filter(category="Fruit")
        self.assertEqual(len(fruits), 2)

        search = self.reg.filter(search_query="carrot")
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].id, "tool-c")


if __name__ == "__main__":
    unittest.main()
