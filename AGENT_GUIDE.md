# Agent Guide: PDF Literature Analysis

This document guides the AI Agent on how to use the tools in this workspace to analyze academic PDF documents.

## Workflow Overview

1.  **Environment Setup**: Ensure dependencies are installed via `uv` (do not use `pip` directly).

```bash
# Install or update project dependencies using uv
uv sync
```
2.  **Text Extraction**: Use `src/pdf_tools.py` to extract text from a target PDF.
3.  **Analysis**: Use the prompts in `prompts/analysis_prompts.md` to analyze the extracted text.
4.  **Reporting**: Save the analysis results to the `output/` directory.

## Detailed Steps for Agent

### Step 1: Check Environment
Run the following command to ensure the environment is synced and dependencies are installed using `uv`:
```bash
uv sync
```

### Step 2: Extract Text
When the user provides a PDF file (e.g., `paper.pdf`), **do not** use direct `python`/`python3` terminal commands. Always use `uv run` to execute the scripts in this workspace.
**Command:**
```bash
# Correct (REQUIRED):
uv run src/pdf_tools.py path/to/paper.pdf
```
**Prohibited:**
```bash
# Do NOT use these direct invocations (forbidden):
python src/pdf_tools.py path/to/paper.pdf
python3 src/pdf_tools.py path/to/paper.pdf
python -m src.pdf_tools path/to/paper.pdf
```
*Note: Agents running Python code within the repository should do so via commands executed under the `uv` environment (i.e., using `uv run`). If you need to import functions in an interactive or programmatic context, make sure the code runs inside the `uv` environment.*

### Step 3: Analyze Content
Once you have the text content:
1.  Read `prompts/analysis_prompts.md` to select the appropriate analysis type.
    - For general overview: Use **1. Comprehensive Summary**.
    - For specific technical details: Use **2. Methodology Analysis**.
    - For **detailed, visual, and in-depth analysis**: Use **5. Deep Analysis & Visualization**.
2.  Apply the prompt to the extracted text.
3.  Generate the response.
    - If using Prompt 5, ensure you generate **Mermaid** code blocks for diagrams and **Markdown tables** for data.

**Important Constraint (禁止新建脚本)**: 当执行文档分析任务时，**禁止创建、修改或提交新的脚本或源代码文件到仓库**。Agent 只能：
- 使用仓库中已有的脚本（例如 `src/pdf_tools.py`, `src/md_to_pdf.py`）。
- 生成或修改输出文件在 `output/`（如 `.md` 或 `.pdf`），或本地临时数据（如提取的文本）
- 更新/使用 `prompts/` 中的模板或 `output/` 中已有的分析文件。

如果需要自动化或新增脚本的功能，请先与人类协同者确认并在获得书面许可后再进行代码修改或添加脚本。

### Step 4: Save Output
Create a Markdown file in `output/` named after the paper (e.g., `output/paper_analysis.md`).
The file should contain:
- The name of the paper.
- The type of analysis performed.
- The content generated in Step 3.

### Step 5: Convert Markdown to PDF (Optional)

If you want a PDF version of the analysis, we provide `src/md_to_pdf.py` as a robust converter that renders Markdown into a professional-looking PDF. Use it like this:

```bash
# Ensure dependencies are installed (including xhtml2pdf)
uv sync

# Convert a markdown report to PDF
uv run src/md_to_pdf.py output/paper_analysis.md output/paper_analysis.pdf
```

Notes:
- The script now uses `markdown` + `xhtml2pdf` for high-quality rendering, supporting tables, code blocks, and images.
- **Charts & Diagrams**: If your analysis contains **Mermaid** diagrams, they will appear as **code blocks** in the generated PDF. To view the rendered diagrams, please open the Markdown file in a compatible viewer (like VS Code or GitHub).
- **CJK Support**: The script automatically detects common CJK fonts on macOS, Linux, and Windows. If you see boxes instead of characters, ensure a CJK font is installed or set `CJK_FONT_PATH`.

```bash
# Example: Force a specific font if auto-detection fails
export CJK_FONT_PATH=/path/to/your/font.ttf
uv run src/md_to_pdf.py output/paper_analysis.md output/paper_analysis.pdf
```

## Example Interaction

**User:** "Analyze this paper for me: `docs/deep_learning.pdf`"

**Agent Action:**
1.  Run `uv run src/pdf_tools.py docs/deep_learning.pdf` to get the text.
2.  (Internal) Read the text output.
3.  (Internal) Read `prompts/analysis_prompts.md` -> "Comprehensive Summary".
4.  (Internal) Generate summary using the text and prompt.
5.  Create file `output/deep_learning_summary.md` with the result.
6.  Reply to user: "I have analyzed the paper. You can find the summary in `output/deep_learning_summary.md`."
