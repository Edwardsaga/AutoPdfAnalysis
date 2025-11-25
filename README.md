# Auto PDF Analysis Workspace

This workspace is designed to assist AI Agents in automatically analyzing academic literature and technical reports in PDF format.

## Structure

- **`src/`**: Contains Python scripts for PDF processing.
    - `pdf_tools.py`: Tools to extract text from PDFs.
- **`prompts/`**: Contains Markdown templates for different types of analysis.
    - `analysis_prompts.md`: Prompts for Summary, Methodology, Innovation, etc.
- **`output/`**: Destination for generated analysis reports.
- **`docs/`**: Place your PDF files here.
- **`AGENT_GUIDE.md`**: Instructions for the AI Agent on how to use this workspace.

## How to Use

1.  **Setup (using uv)**:
    Ensure you have [uv](https://github.com/astral-sh/uv) installed.
    ```bash
    # Initialize environment and install dependencies
    uv sync
    ```
2.  **Place PDF**: Put your PDF file in the `docs/` folder (or anywhere in the workspace).
3.  **Ask Agent**: Open your IDE's AI Chat (e.g., Copilot) and ask:
    > "Please analyze the PDF `docs/my_paper.pdf` using the instructions in AGENT_GUIDE.md."

**Important rule (execution policy):** Do not run scripts with `python`/`python3` directly. Always use `uv run` for any script invocation. Example:

```bash
# Correct (required):
uv sync
uv run src/pdf_tools.py docs/my_paper.pdf

# Forbidden (do not use these):
python src/pdf_tools.py docs/my_paper.pdf
python3 src/pdf_tools.py docs/my_paper.pdf
```

## Features

- **Modern Tooling**: Uses `uv` for fast and reliable Python environment management.
- **Text Extraction**: Robust PDF text extraction using `pypdf`.
- **Structured Analysis**: Pre-defined prompts ensure consistent and high-quality outputs.
- **Agent-Ready**: Designed specifically to be "read" and "executed" by LLM Agents.
 - **Agent-Ready**: Designed specifically to be "read" and "executed" by LLM Agents.
 - **Important Rule:** When performing analysis tasks, do NOT create or modify scripts or source files in this repository; use existing tools and write outputs to `output/`.
