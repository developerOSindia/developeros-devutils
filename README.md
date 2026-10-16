# DeveloperOS DevUtils Suite

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io)
[![Privacy: Client--Side](https://img.shields.io/badge/Privacy-Zero--Storage-10b981.svg)](https://developeros.in/privacy)
[![Tests: Passing](https://img.shields.io/badge/Tests-62%20Passing-brightgreen.svg)](tests/)

An independent, production-grade developer utility suite containing **20 offline, zero-storage utilities** built for the [DeveloperOS](https://developeros.in) ecosystem.

---

## 🌟 Overview & Architecture

DeveloperOS DevUtils provides developers with essential formatting, validation, encoding, inspection, and web design utilities. All operations run **strictly in-memory client-side**, with zero analytics, zero server telemetry, and zero remote logging.

### Architectural Principles
- **Decoupled Architecture**: All algorithms and business logic are contained in `core/` as pure Python modules with zero Streamlit dependencies.
- **Plug-and-Play Registry**: Tools self-register through `tools/registry.py` with 13 metadata fields adhering to the DeveloperOS Tool Plugin Contract.
- **Security Guardrails**:
  - ReDoS protection and string length limits on regex execution.
  - XXE and Billion Laughs defense on XML parsing (safe minidom parser with entity expansion rejection).
  - Explicit warning banner on JWT decoding noting structural-only decode without cryptographic verification.
  - Safe payload caps across all file and input parsers.

---

## 🛠️ The 20 DevUtils Utilities

| # | Tool Name | Category | Module | Description & Capabilities |
|---|---|---|---|---|
| **1** | **JSON Formatter** | Formatters & Converters | `core/json_formatter.py` | Prettify, indent (2/4 spaces), sort keys, or minify JSON payloads. |
| **2** | **JSON Validator** | Formatters & Converters | `core/json_validator.py` | Strict RFC 8259 syntax validation with line/column error reporting. |
| **3** | **JSON ↔ CSV Converter** | Formatters & Converters | `core/json_csv_converter.py` | Bidirectional converter between tabular JSON objects and CSV files. |
| **4** | **YAML ↔ JSON Converter** | Formatters & Converters | `core/yaml_json_converter.py` | Seamless translation between YAML manifests and JSON payloads. |
| **5** | **XML Formatter** | Formatters & Converters | `core/xml_formatter.py` | Prettify/minify XML with XXE and entity expansion security defense. |
| **6** | **Base64 Encoder/Decoder** | Security & Encoders | `core/base64_codec.py` | Standard and URL-safe Base64 encoding/decoding with padding normalization. |
| **7** | **JWT Decoder** | Security & Encoders | `core/jwt_decoder.py` | Inspect header & payload claims with timestamps; non-cryptographic disclaimer. |
| **8** | **UUID Generator** | Security & Encoders | `core/uuid_generator.py` | Bulk generate UUIDv4 (random) and UUIDv1 (timestamp) with casing and braces. |
| **9** | **Regex Tester** | Security & Encoders | `core/regex_tester.py` | Real-time pattern evaluation, match group extraction, and text replacement. |
| **10** | **Cron Builder** | Security & Encoders | `core/cron_builder.py` | Visual 5-part cron schedule builder and English schedule explainer. |
| **11** | **Unix Timestamp Converter** | Text & Inspection | `core/unix_timestamp.py` | Epoch seconds/milliseconds to UTC, ISO 8601, local time, and date parsing. |
| **12** | **URL Encoder/Decoder** | Text & Inspection | `core/url_codec.py` | Percent-encoding, decoding, and URL component/query parameter inspector. |
| **13** | **Text Diff Checker** | Text & Inspection | `core/text_diff.py` | Side-by-side and unified diff generator with similarity and delta metrics. |
| **14** | **Hash Calculator** | Text & Inspection | `core/hash_calculator.py` | Multi-algorithm hashing (SHA-256/512/MD5), HMAC, and constant-time verification. |
| **15** | **Markdown Previewer** | Text & Inspection | `core/markdown_previewer.py` | Live preview, heading outline generator, metrics, and XSS script tag alerts. |
| **16** | **HTML Minifier** | Web & Design Tools | `core/html_minifier.py` | Strip comments and collapse whitespace while preserving code/pre blocks. |
| **17** | **CSS Minifier** | Web & Design Tools | `core/css_minifier.py` | Strip comments, collapse selectors/delimiters, and optimize stylesheets. |
| **18** | **Color Converter** | Web & Design Tools | `core/color_converter.py` | Convert HEX, RGB, HSL, CMYK, and verify WCAG AA accessibility contrast. |
| **19** | **Text Case Converter** | Web & Design Tools | `core/text_case_converter.py` | camelCase, PascalCase, snake_case, CONSTANT_CASE, kebab-case, and more. |
| **20** | **QR Code Generator** | Web & Design Tools | `core/qr_code_generator.py` | Generate vector SVG and PNG QR codes with configurable error correction. |

---

## 📁 Repository Structure

```
suites/developeros-devutils/
├── app.py                      # Main Streamlit application entrypoint
├── manifest.yaml               # Suite metadata & 20-tool catalog
├── requirements.txt            # Runtime dependencies
├── pyproject.toml              # Build & test tooling configuration
├── LICENSE                     # MIT License
├── README.md                   # Suite documentation
├── CONTRIBUTING.md             # Developer contribution guidelines
├── .env.example                # Environment variable template
├── .streamlit/
│   └── config.toml             # DeveloperOS dark theme tokens
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions CI workflow
├── assets/                     # Portable branding assets
│   ├── logo.svg
│   └── theme.json
├── components/                 # Reusable DeveloperOS UI widgets
│   ├── header.py
│   ├── footer.py
│   ├── navigation.py
│   ├── privacy.py
│   ├── alerts.py
│   └── related_tools.py
├── core/                       # Pure Python core logic (20 modules)
│   ├── base64_codec.py
│   ├── color_converter.py
│   ├── cron_builder.py
│   ├── css_minifier.py
│   ├── hash_calculator.py
│   ├── html_minifier.py
│   ├── json_csv_converter.py
│   ├── json_formatter.py
│   ├── json_validator.py
│   ├── jwt_decoder.py
│   ├── markdown_previewer.py
│   ├── qr_code_generator.py
│   ├── regex_tester.py
│   ├── text_case_converter.py
│   ├── text_diff.py
│   ├── unix_timestamp.py
│   ├── url_codec.py
│   ├── uuid_generator.py
│   ├── xml_formatter.py
│   └── yaml_json_converter.py
├── tools/                      # Streamlit UI views for all 20 tools
│   ├── __init__.py             # Auto-registration bootstrap
│   ├── registry.py             # ToolRegistry singleton & contract
│   └── *_view.py               # Individual tool UI views
└── tests/                      # Automated unit & integration tests
    ├── test_batch1_formatters.py
    ├── test_batch2_security_encoders.py
    ├── test_batch3_text_inspection.py
    ├── test_batch4_web_design.py
    ├── test_suite_registration.py
    ├── test_manifest.py
    └── test_registry.py
```

---

## 🚀 Running Locally

### 1. Prerequisites
- Python 3.12+

### 2. Setup Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Run Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 4. Run Test Suite
```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 🔒 Security & Privacy Guarantees

- **No Remote Processing**: All utilities execute locally in the client runtime.
- **Strict Bounds**:
  - Payloads capped between 1MB – 5MB depending on tool category.
  - Regex patterns limited to 500 characters and 100,000 text characters to eliminate ReDoS attack vectors.
  - XML parsers explicitly disallow external entity declarations (`<!ENTITY ... SYSTEM ...>`).
- **Cryptographic Disclaimer**: The JWT tool is explicitly marked as a structural decoder only and does not verify signature authenticity.

---

## 🏷️ Recommended GitHub Topics

When configuring this repository on GitHub, apply these topics:
`devutils` `developer-tools` `formatters` `encoders` `validators` `streamlit` `offline-first` `developeros` `open-source`

---

## 📜 License & Attribution

Distributed under the **MIT License**. See [LICENSE](LICENSE) for details.

- **Main Website**: [https://developeros.in](https://developeros.in)
- **Central Tools Directory**: [https://tools.developeros.in](https://tools.developeros.in)
- **GitHub Organization**: [https://github.com/developerOSindia](https://github.com/developerOSindia)

