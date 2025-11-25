# Academic Paper Analysis Prompts

Use these prompts to analyze the extracted text from PDF documents.

IMPORTANT: **禁止在终端中使用 `python`/`python3`/`python -m` 等命令直接执行仓库脚本。**
始终使用 `uv run` 来运行脚本，并在 `uv` 管理的虚拟环境内执行任何导入或脚本调用。

IMPORTANT: When performing analysis with these prompts, **do not create, modify, or commit new scripts or source files** in the repository. Use only existing tools and save outputs under `output/`.

## 1. Comprehensive Summary (综合摘要)

**Context:** You are an expert academic researcher.
**Note:** During analysis, do NOT create or modify scripts in the repository—only use existing tools and write outputs to `output/`.
**Task:** Summarize the following academic paper text.
**Input:** [Insert Paper Text Here]
**Output Format:**
- **Title:** [Infer title if possible]
- **Core Problem:** What problem is the paper trying to solve?
- **Proposed Solution:** What is their main contribution or method?
- **Key Results:** What were the main findings?
- **Significance:** Why does this matter?

---

## 2. Methodology Analysis (方法论分析)

**Context:** You are a technical reviewer.
**Note:** During analysis, do NOT create or modify scripts in the repository—only use existing tools and write outputs to `output/`.
**Task:** Analyze the methodology section of the paper.
**Input:** [Insert Paper Text Here]
**Output Format:**
- **Algorithm/Model:** Describe the core algorithm or model architecture.
- **Dataset:** What data was used?
- **Baselines:** What did they compare against?
- **Metrics:** What metrics were used for evaluation?

---

## 3. Innovation & Critique (创新与批判)

**Context:** You are a critical thinker.
**Note:** During analysis, do NOT create or modify scripts in the repository—only use existing tools and write outputs to `output/`.
**Task:** Evaluate the novelty and limitations of the paper.
**Input:** [Insert Paper Text Here]
**Output Format:**
- **Novelty:** What is truly new here? (vs. existing work)
- **Strengths:** What did they do well?
- **Weaknesses/Limitations:** What are the flaws or missing parts?
- **Future Work:** What do the authors suggest for future research?

---

## 4. Code Implementation Guide (代码实现指南)

**Context:** You are a senior software engineer.
**Note:** During analysis, do NOT create or modify scripts in the repository—only use existing tools and write outputs to `output/`.
**Task:** Based on the paper, outline how one would implement this.
**Input:** [Insert Paper Text Here]
**Output Format:**
- **Key Classes/Functions:** What modules are needed?
- **Dependencies:** What libraries would be useful?
- **Pseudocode:** A high-level logic flow.

---

## 5. Deep Analysis & Visualization (深度分析与可视化)

**Context:** You are a Principal Researcher and Data Scientist.
**Note:** During analysis, do NOT create or modify scripts in the repository—only use existing tools and write outputs to `output/`.
**Task:** Perform a deep-dive analysis of the paper, including structural visualizations and comparative data.
**Input:** [Insert Paper Text Here]
**Output Format:**

### 1. Executive Summary (执行摘要)
- **Problem Statement:** Clear definition of the problem.
- **Core Contribution:** The "one-liner" value proposition.
- **Impact:** Why this is a breakthrough.

### 2. Technical Architecture (技术架构)
- **Workflow Diagram:** (Generate a **Mermaid** flowchart representing the method's pipeline. Use `graph TD` or `graph LR`.)
- **Component Analysis:** Detailed breakdown of each module.

### 3. Mathematical & Theoretical Foundation (数学与理论基础)
- **Key Equations:** (Use LaTeX format)
- **Derivation Logic:** Explain the steps between equations.

### 4. Experimental Analysis (实验分析)
- **Datasets:** Detailed table of datasets used.
- **Results Comparison:** (Create a Markdown Table comparing this method vs. SOTA baselines).
- **Ablation Studies:** What components matter most?

### 5. Critical Discussion (批判性讨论)
- **Strengths:** (Bullet points)
- **Weaknesses:** (Bullet points)
- **Future Directions:** Where to go next?

### 6. Implementation Roadmap (实现路线图)
- **Class Diagram:** (Generate a **Mermaid** class diagram `classDiagram` showing the proposed code structure).
- **Key Dependencies:** List of libraries.

**Note on Charts:**
- Use `mermaid` code blocks for diagrams.
- Use Markdown tables for data.
