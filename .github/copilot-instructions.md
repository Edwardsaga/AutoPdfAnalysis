# Copilot Instructions for Auto PDF Analysis

This repository is an **Agent-First Workspace** designed for automated academic paper analysis. The primary workflow involves an AI agent reading instructions, executing Python scripts via `uv`, and generating structured reports.

## Architecture & Data Flow

- **Core Logic (`src/`)**: `src/pdf_tools.py` is the single source of truth for PDF processing. It uses `pypdf` to extract text.
- **Agent Brain (`AGENT_GUIDE.md`)**: This file contains the imperative logic for the Agent. **Always consult this file** before performing analysis tasks.
- **Templates (`prompts/`)**: `prompts/analysis_prompts.md` defines the schema for different analysis types (Summary, Methodology, etc.).
- **Data Flow**:
  1.  **Input**: PDF files placed in `docs/`.
  2.  **Process**: `uv run src/pdf_tools.py` extracts raw text.
  3.  **Analysis**: Agent applies templates from `prompts/` to the raw text.
  4.  **Output**: Markdown reports saved to `output/`.

## Critical Developer Workflows

### Environment & Execution
This project uses **uv** for dependency management. Do not use `pip` directly.

- **Strict Execution Policy:**
  - **禁止**在终端中直接使用 `python`、`python3`、`python -m` 等命令来执行仓库脚本。
  - **强制**使用 `uv run` 来运行仓库里的 Python 脚本，以保证依赖和环境的一致性。

- **Initialize/Update Environment**:
  ```bash
  uv sync
  ```
- **Run Scripts**:
  Always use `uv run` to execute scripts within the virtual environment context. Do not use `python` direct command invocations.
  ```bash
  uv run src/pdf_tools.py docs/paper.pdf
  ```

### Markdown to PDF conversion
We include a script `src/md_to_pdf.py` to convert Markdown analysis outputs into PDF. This module has been upgraded to use `xhtml2pdf` for professional-grade layout and typography.

```bash
# After `uv sync` to ensure the dependencies are present
uv run src/md_to_pdf.py output/paper_analysis.md output/paper_analysis.pdf
```

**Key Features:**
- **High Quality**: Uses HTML/CSS intermediate representation for better control over fonts, margins, and tables.
- **CJK Support**: Automatically detects system CJK fonts. Can be overridden via `CJK_FONT_PATH`.
- **Zero-Dependency**: Runs entirely within the python environment managed by `uv`.

Font notes (CJK):
- If the generated PDF contains missing glyphs (squares), ensure a CJK TTF/OTF is installed or set `CJK_FONT_PATH` to a TTF/OTF path before running the script.

### Analysis Workflow
When asked to analyze a paper:
1.  **Read Context**: Check `AGENT_GUIDE.md` for the latest procedure.
2.  **Extract**: Run the extraction script via terminal.
3.  **Synthesize**: Use the specific prompt template requested (e.g., "Comprehensive Summary").
4.  **Persist**: Save the result as `output/<paper_name>_<analysis_type>.md`.

**Important Constraint (禁止新建脚本)**: During analysis tasks, agents must NOT create, modify, or commit new scripts or source files in this repository. Agents may only use existing tools and templates, and write outputs to `output/`.
分析结果的.md必须为中文！！！

## Project Conventions

- **Agent-Centric Documentation**: Documentation is written for *Agents* to execute, not just humans to read.
- **File Paths**:
  - Inputs: `docs/*.pdf`
  - Outputs: `output/*.md`
  - Source: `src/*.py`
- **Error Handling**: If PDF extraction fails, report the specific error from `pypdf` back to the user.

## Key Files
- `AGENT_GUIDE.md`: The master protocol for analysis tasks.
- `src/pdf_tools.py`: The tool implementation.
- `pyproject.toml`: Dependency definition (managed by `uv`).
