# Contributing to DeveloperOS Suite

Thank you for your interest in contributing to the DeveloperOS tools ecosystem!

## Core Principles

1. **Decoupled Architecture**: All business logic must reside in `core/` and have zero imports of Streamlit or any other UI framework.
2. **Zero-Trust Ephemeral Privacy**: Never write user payloads to disk, files, or local storage. Never log user data or transmit it to external services.
3. **Plug-and-Play Contract**: Every tool must be defined via `ToolDefinition` in `tools/` and registered into the singleton `ToolRegistry`. Removing a tool must never break the suite.
4. **Comprehensive Testing**: Every function in `core/` must have unit test coverage in `tests/`.

---

## Development Workflow

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/developerOSindia/<suite-name>.git
   cd <suite-name>
   ```

2. **Environment Setup**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   pip install pytest ruff
   ```

3. **Code Style & Linting**:
   ```bash
   ruff check .
   ruff format .
   ```

4. **Running Tests**:
   ```bash
   pytest tests/
   ```

5. **Submitting a Pull Request**:
   - Provide a clear PR title matching Conventional Commits (`feat(tools): add uuid generator`).
   - Confirm that all unit tests pass locally.
   - Ensure `manifest.yaml` reflects your new utility.

---

## Code of Conduct
We adhere to welcoming, inclusive, and professional open-source standards. See [DeveloperOS Code of Conduct](https://developeros.in/conduct).
