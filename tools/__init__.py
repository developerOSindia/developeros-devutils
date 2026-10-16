"""
DeveloperOS Tools Package & Registration Bootstrap.
Each tool is registered into the ToolRegistry. Tools can be installed or removed
independently without impacting other utilities in the suite.
"""

from tools.registry import registry, ToolDefinition, register_tool

# Batch 1: Formatters & Converters
from tools.json_formatter_view import render_json_formatter_view
from tools.json_validator_view import render_json_validator_view
from tools.json_csv_converter_view import render_json_csv_converter_view
from tools.yaml_json_converter_view import render_yaml_json_converter_view
from tools.xml_formatter_view import render_xml_formatter_view

# Batch 2: Security & Encoders
from tools.base64_codec_view import render_base64_codec_view
from tools.jwt_decoder_view import render_jwt_decoder_view
from tools.uuid_generator_view import render_uuid_generator_view
from tools.regex_tester_view import render_regex_tester_view
from tools.cron_builder_view import render_cron_builder_view

# Batch 3: Text & Inspection
from tools.unix_timestamp_view import render_unix_timestamp_view
from tools.url_codec_view import render_url_codec_view
from tools.text_diff_view import render_text_diff_view
from tools.hash_calculator_view import render_hash_calculator_view
from tools.markdown_previewer_view import render_markdown_previewer_view

# Batch 4: Web & Design Tools
from tools.html_minifier_view import render_html_minifier_view
from tools.css_minifier_view import render_css_minifier_view
from tools.color_converter_view import render_color_converter_view
from tools.text_case_converter_view import render_text_case_converter_view
from tools.qr_code_generator_view import render_qr_code_generator_view


def init_tools():
    """Initializes and registers all 20 utilities in the DevUtils suite."""
    # ----------------------------------------------------
    # Batch 1: Formatters & Converters
    # ----------------------------------------------------
    register_tool(ToolDefinition(
        id="tool-json-formatter",
        name="JSON Formatter",
        description="Prettify, format, sort keys, and minify JSON payloads.",
        category="Formatters & Converters",
        version="1.0.0",
        ui_entrypoint=render_json_formatter_view,
        core_module="core.json_formatter",
        input_output_spec={"input": "application/json (max 2MB)", "output": "formatted JSON"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/json-formatter",
        related_tools=["tool-json-validator", "tool-json-csv-converter", "tool-yaml-json-converter"],
    ))

    register_tool(ToolDefinition(
        id="tool-json-validator",
        name="JSON Validator",
        description="Inspect, validate syntax, and detect line/column syntax errors in JSON.",
        category="Formatters & Converters",
        version="1.0.0",
        ui_entrypoint=render_json_validator_view,
        core_module="core.json_validator",
        input_output_spec={"input": "application/json (max 2MB)", "output": "validation report"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/json-validator",
        related_tools=["tool-json-formatter", "tool-json-csv-converter"],
    ))

    register_tool(ToolDefinition(
        id="tool-json-csv-converter",
        name="JSON ↔ CSV Converter",
        description="Convert structured tabular JSON lists to CSV format and vice-versa.",
        category="Formatters & Converters",
        version="1.0.0",
        ui_entrypoint=render_json_csv_converter_view,
        core_module="core.json_csv_converter",
        input_output_spec={"input": "application/json or text/csv", "output": "converted data"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/json-csv-converter",
        related_tools=["tool-json-formatter", "tool-yaml-json-converter"],
    ))

    register_tool(ToolDefinition(
        id="tool-yaml-json-converter",
        name="YAML ↔ JSON Converter",
        description="Bidirectional translation between YAML documents and JSON representations.",
        category="Formatters & Converters",
        version="1.0.0",
        ui_entrypoint=render_yaml_json_converter_view,
        core_module="core.yaml_json_converter",
        input_output_spec={"input": "text/yaml or application/json", "output": "converted format"},
        privacy_classification="client_side",
        dependency_requirements=["pyyaml>=6.0.1", "streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/yaml-json-converter",
        related_tools=["tool-json-formatter", "tool-xml-formatter"],
    ))

    register_tool(ToolDefinition(
        id="tool-xml-formatter",
        name="XML Formatter",
        description="Prettify or minify XML with security defense against XXE and entity expansion.",
        category="Formatters & Converters",
        version="1.0.0",
        ui_entrypoint=render_xml_formatter_view,
        core_module="core.xml_formatter",
        input_output_spec={"input": "application/xml (max 2MB)", "output": "formatted XML"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/xml-formatter",
        related_tools=["tool-json-formatter", "tool-yaml-json-converter"],
    ))

    # ----------------------------------------------------
    # Batch 2: Security & Encoders
    # ----------------------------------------------------
    register_tool(ToolDefinition(
        id="tool-base64-codec",
        name="Base64 Encoder/Decoder",
        description="Encode and decode text into standard or URL-safe Base64 strings.",
        category="Security & Encoders",
        version="1.0.0",
        ui_entrypoint=render_base64_codec_view,
        core_module="core.base64_codec",
        input_output_spec={"input": "text/plain (max 5MB)", "output": "base64 text"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/base64-codec",
        related_tools=["tool-jwt-decoder", "tool-url-codec"],
    ))

    register_tool(ToolDefinition(
        id="tool-jwt-decoder",
        name="JWT Decoder",
        description="Decode JSON Web Tokens into Header, Claims, and human-readable timestamps.",
        category="Security & Encoders",
        version="1.0.0",
        ui_entrypoint=render_jwt_decoder_view,
        core_module="core.jwt_decoder",
        input_output_spec={"input": "JWT token string", "output": "decoded header & payload"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/jwt-decoder",
        related_tools=["tool-base64-codec", "tool-hash-calculator"],
    ))

    register_tool(ToolDefinition(
        id="tool-uuid-generator",
        name="UUID Generator",
        description="Generate bulk cryptographically strong UUID v4 or time-based v1 identifiers.",
        category="Security & Encoders",
        version="1.0.0",
        ui_entrypoint=render_uuid_generator_view,
        core_module="core.uuid_generator",
        input_output_spec={"input": "formatting parameters", "output": "list of UUID strings"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/uuid-generator",
        related_tools=["tool-hash-calculator", "tool-base64-codec"],
    ))

    register_tool(ToolDefinition(
        id="tool-regex-tester",
        name="Regex Tester",
        description="Evaluate regular expression patterns with capture groups, flags, and substitutions.",
        category="Security & Encoders",
        version="1.0.0",
        ui_entrypoint=render_regex_tester_view,
        core_module="core.regex_tester",
        input_output_spec={"input": "regex pattern and test string", "output": "match list"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/regex-tester",
        related_tools=["tool-text-diff", "tool-text-case-converter"],
    ))

    register_tool(ToolDefinition(
        id="tool-cron-builder",
        name="Cron Builder",
        description="Construct, customize, and explain 5-part cron schedules in human English.",
        category="Security & Encoders",
        version="1.0.0",
        ui_entrypoint=render_cron_builder_view,
        core_module="core.cron_builder",
        input_output_spec={"input": "cron fields or expression", "output": "cron string & meaning"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/cron-builder",
        related_tools=["tool-unix-timestamp", "tool-regex-tester"],
    ))

    # ----------------------------------------------------
    # Batch 3: Text & Inspection
    # ----------------------------------------------------
    register_tool(ToolDefinition(
        id="tool-unix-timestamp",
        name="Unix Timestamp Converter",
        description="Convert epoch timestamps to UTC/local datetimes and parse dates to timestamps.",
        category="Text & Inspection",
        version="1.0.0",
        ui_entrypoint=render_unix_timestamp_view,
        core_module="core.unix_timestamp",
        input_output_spec={"input": "epoch int or date string", "output": "formatted datetimes"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/unix-timestamp",
        related_tools=["tool-cron-builder", "tool-jwt-decoder"],
    ))

    register_tool(ToolDefinition(
        id="tool-url-codec",
        name="URL Encoder/Decoder",
        description="Encode, decode, and parse query parameters and URL path components.",
        category="Text & Inspection",
        version="1.0.0",
        ui_entrypoint=render_url_codec_view,
        core_module="core.url_codec",
        input_output_spec={"input": "url string", "output": "encoded/decoded components"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/url-codec",
        related_tools=["tool-base64-codec", "tool-hash-calculator"],
    ))

    register_tool(ToolDefinition(
        id="tool-text-diff",
        name="Text Diff Checker",
        description="Compare code, configuration, or text side-by-side with change metrics.",
        category="Text & Inspection",
        version="1.0.0",
        ui_entrypoint=render_text_diff_view,
        core_module="core.text_diff",
        input_output_spec={"input": "original & modified texts", "output": "unified diff"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/text-diff",
        related_tools=["tool-markdown-previewer", "tool-regex-tester"],
    ))

    register_tool(ToolDefinition(
        id="tool-hash-calculator",
        name="Hash Calculator",
        description="Compute SHA-256, SHA-512, MD5 hashes, and HMAC digests client-side.",
        category="Text & Inspection",
        version="1.0.0",
        ui_entrypoint=render_hash_calculator_view,
        core_module="core.hash_calculator",
        input_output_spec={"input": "text/plain (max 1MB)", "output": "hash digests"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/hash-calculator",
        related_tools=["tool-jwt-decoder", "tool-base64-codec"],
    ))

    register_tool(ToolDefinition(
        id="tool-markdown-previewer",
        name="Markdown Previewer",
        description="Live preview of Markdown text, table-of-contents extraction, and security checks.",
        category="Text & Inspection",
        version="1.0.0",
        ui_entrypoint=render_markdown_previewer_view,
        core_module="core.markdown_previewer",
        input_output_spec={"input": "text/markdown", "output": "rendered HTML & metrics"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/markdown-previewer",
        related_tools=["tool-html-minifier", "tool-text-diff"],
    ))

    # ----------------------------------------------------
    # Batch 4: Web & Design Tools
    # ----------------------------------------------------
    register_tool(ToolDefinition(
        id="tool-html-minifier",
        name="HTML Minifier",
        description="Compress HTML markup, collapse whitespace, strip comments, and save bandwidth.",
        category="Web & Design Tools",
        version="1.0.0",
        ui_entrypoint=render_html_minifier_view,
        core_module="core.html_minifier",
        input_output_spec={"input": "text/html (max 2MB)", "output": "minified html"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/html-minifier",
        related_tools=["tool-css-minifier", "tool-xml-formatter"],
    ))

    register_tool(ToolDefinition(
        id="tool-css-minifier",
        name="CSS Minifier",
        description="Compress CSS stylesheets, eliminate whitespace and comments, and optimize load speed.",
        category="Web & Design Tools",
        version="1.0.0",
        ui_entrypoint=render_css_minifier_view,
        core_module="core.css_minifier",
        input_output_spec={"input": "text/css (max 2MB)", "output": "minified css"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/css-minifier",
        related_tools=["tool-html-minifier", "tool-color-converter"],
    ))

    register_tool(ToolDefinition(
        id="tool-color-converter",
        name="Color Converter",
        description="Convert HEX, RGB, HSL, and CMYK colors and calculate WCAG contrast ratios.",
        category="Web & Design Tools",
        version="1.0.0",
        ui_entrypoint=render_color_converter_view,
        core_module="core.color_converter",
        input_output_spec={"input": "color code string", "output": "color representations & contrast"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/color-converter",
        related_tools=["tool-css-minifier", "tool-qr-code-generator"],
    ))

    register_tool(ToolDefinition(
        id="tool-text-case-converter",
        name="Text Case Converter",
        description="Transform strings across camelCase, PascalCase, snake_case, kebab-case, and more.",
        category="Web & Design Tools",
        version="1.0.0",
        ui_entrypoint=render_text_case_converter_view,
        core_module="core.text_case_converter",
        input_output_spec={"input": "text/plain", "output": "converted casing variations"},
        privacy_classification="client_side",
        dependency_requirements=["streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/text-case-converter",
        related_tools=["tool-regex-tester", "tool-text-diff"],
    ))

    register_tool(ToolDefinition(
        id="tool-qr-code-generator",
        name="QR Code Generator",
        description="Generate vector SVG and PNG QR codes with configurable error correction.",
        category="Web & Design Tools",
        version="1.0.0",
        ui_entrypoint=render_qr_code_generator_view,
        core_module="core.qr_code_generator",
        input_output_spec={"input": "text or url (max 2048 chars)", "output": "SVG / PNG QR code"},
        privacy_classification="client_side",
        dependency_requirements=["qrcode>=7.4.2", "Pillow>=10.0.0", "streamlit>=1.38.0"],
        deployment_support=["streamlit_community_cloud", "docker"],
        documentation_link="https://developeros.in/docs/tools/qr-code-generator",
        related_tools=["tool-url-codec", "tool-base64-codec"],
    ))


# Automatically initialize all 20 tools upon import
init_tools()

__all__ = ["registry", "init_tools", "ToolDefinition", "register_tool"]
