# UltraRAG — 知识适配（Knowledge Adaptation）详尽分析

本文档聚焦于 UltraRAG 中“知识适配”部分的深入解析、实施建议、可复现实验与 ablation 方案（中文）。适合用于研究员、工程师和产品经理理解核心技术细节并在 UltraRAG 环境中复现实验。

---

## 1. 总览（Overview）
- 知识适配是 UltraRAG 的核心亮点之一，目标是通过自动化数据构造与端到端训练流程，让 RAG 系统在给定域（如法律、金融或医学）中达到更高的检索与生成准确性。UltraRAG 包含：
  - 知识管理（多格式上传、chunk、索引）
  - 数据构造（自动 query 生成、正负样本、SFT 和 DPO 对）
  - Embedding finetune（检索微调）
  - Generation finetune（SFT + DPO + LoRA）
  - Evaluation 与 Inference（VanillaRAG、DeepNote、RAGAdaptation）

> 目标：提高模型在特定域内的 factual accuracy、精确引用知识（例如引用正确的法律条文）并降低 hallucination。

---

## 2. 数据构造（Data Construction）详解
### 目的
- 自动化生成可用于训练检索器与生成器的高质量样本，尤其是域内 query/response、hard negative 和偏好对。

### 流程
1. 文档上传与 chunk：支持 PDF、TXT、Markdown、JSON 等；chunk_size（示例 512）与 overlap（示例 15%）可配置。
2. Query 生成：基于知识库片段自动生成 query（可使用 LLM 或规则）；生成多种查询类型（短问、长问、跨段/多段）以覆盖多样场景。
3. 正负采样：
   - 正样本（pos）：查询最相关的 chunk（可用人工/规则标注或基于引用）
   - 负样本（neg）：BM25 / ANN nearest / in-batch negatives（hard negative）
4. 生成训练对：构造 SFT 对（query -> high-quality response）与 DPO 偏好对（r+ vs r-）。偏好对可由规则或 learned reward 生成。

### Design Notes
- Query 质量关键：优先使用高质量 LLM 或人工抽验来生成或过滤 queries。
- Hard negative 多样化：混合 BM25 / ANN / in-batch 来形成更强的负样本采样。
- Avoid leakage：训练与验证/测试集应严格分离，避免数据泄露导致性能虚高。

---

## 3. Embedding Finetuning（检索微调）
### 目标
- 提高检索器（dense retriever）在域内的响应相关性，减少引入无关知识或错误条文的概率。

### 常用训练方案
- Loss：InfoNCE / SupCon / MarginRanking 等；
- Batch & Negatives：in-batch negative + top-K hard negatives（ANN）；
- Pooling：weighted mean pooling 或 attention-pooling；
- 训练样本：paper 中示例为 2.8k 样本，建议同时尝试 10k、50k 测试规模影响。

### 超参数建议（参考）
- LR: 2e-5 ~ 2e-4
- Batch size: 64（若显存充足可更大）
- Epochs: 1–5（early stop based on dev retrieval metrics）
- Hard negative top-K: 5–20

### 评价指标
- MRR@10, NDCG@10, Recall@k；同时 check downstream generation result（ROUGE-L / human evaluation）。

---

## 4. Generation Finetuning（生成微调：SFT & DPO）
### 方法回顾
- SFT（监督微调）：基于高质量 query-answer pairs 训练生成模型。
- DPO（Direct Preference Optimization）：利用偏好对对生成模型的概率分布进行优化，不需训练 RL 或显式 reward model。
- LoRA：在大模型上进行高效参数微调（低资源、易部署）。

### 训练策略建议
- 推荐流程：SFT -> DPO（SFT 建立 baseline 质量，DPO 优化偏好对齐）
- LoRA 作为默认微调方式（r=8/16; alpha=16/32），如资源允许可做少量全量微调对比。
- DPO 偏好对生成方式建议多维度规则或引入 learned reward model（cross-encoder 作为相对 label）

### 重要风险/注意点
- 规则型 reward 易引入偏差（例如评分更偏好引用条文数量而非正确性或解释质量）
- DPO 对偏好对质量高度敏感——高质量的人类偏好集或高质量的自动判别器很重要

---

## 5. 推理工作流（Inference Workflow）
### 三种典型流程（UltraRAG）
- VanillaRAG：标准 retriever + generator pipeline
- DeepNote：adaptive memory reviewer，动态更新检索上下文；适合 multi-hop、long-form reasoning
- RAGAdaptation：使用微调后的 embedding 与 generator，效果最佳但训练成本最高

### 选用建议
- 需要高准确性（如法律）选 RAGAdaptation + re-ranker
- 需要更好上下文结构但不想大规模训练选 DeepNote
- 资源/时间受限时使用 VanillaRAG

---

## 6. Ablation 与实验计划（可复现）
> 目标：拆解 Data Construction、Embedding、SFT、DPO 等各部分对整体性能的贡献

### 基线设置
- 知识库：法律文本 > 1000 本
- Embedding：MiniCPM-Embedding-Light（paper 中使用）
- Generator：MiniCPM-3-4B
- Chunk：512, overlap 15%
- 指标：MRR@10 / NDCG@10 / Recall@10 / ROUGE-L / 人工准确率（法律条文引用是否正确）

### 实验清单（优先级顺序）
1. Embedding 数据规模试验：{2.8k, 10k, 50k}
2. Hard negative 策略对比：{BM25, in-batch, ANN nearest}
3. Embedding loss 对比：{InfoNCE, SupCon, Margin}
4. Generator 策略对比：{SFT-only, DPO-only, SFT->DPO}
5. LoRA Rank 对比：r∈{4,8,16,32}
6. Inference Pipeline 对比：Vanilla / DeepNote / RAGAdaptation (+/− re-ranker)
7. Cross-domain 验证（法律 -> 医疗/金融）

### 典型实验（SFT->DPO 复现示例）
- Step1: 使用 DataConstructor 生成 query / sft_pairs / pref_pairs
- Step2: SFT 微调（MiniCPM-3-4B）：LoRA 或常规微调，LR 5e-5, batch 8–16, Epoch 1–3
- Step3: DPO 微调（LoRA）：r=8, alpha=16, LR 1e-4, batch 8, Epoch 1–3
- Step4: 评估：ROUGE-L / 人工核查 / legal article citation recall

### 预期结果举例（paper 中的经验值）
- Embedding Finetune 带来 MRR(36.46 -> 37.57)、NDCG(40.05 -> 42.12)
- Generator SFT/DPO 带来 ROUGE-L 的可观提升（如 VanillaRAG 40.75 -> DDR 53.14）

---

## 7. 可复制命令样例（示例 CLI / WebUI 操作）
> 说明：以下是伪命令示例，实际命令依 UltraRAG WebUI 或 CLI 实现为准：

```bash
# 1. 索引与分块
uv run ultrarag index --kb docs/legal/*.pdf --chunk-size 512 --overlap 0.15

# 2. 生成 queries
uv run ultrarag gen-queries --kb-id law_kb --num-per-doc 3 --out data/queries.json

# 3. 构造训练数据 (pos/neg / sft / pref pairs)
uv run ultrarag construct-data --kb-id law_kb --queries data/queries.json --out data/train_data.json

# 4. Embedding finetune
uv run ultrarag finetune-embed --model miniCPM-embed --train data/embed_train.json --out ckpts/embed_ckpt

# 5. Generator SFT 微调（LoRA）
uv run ultrarag finetune-gen --model miniCPM-3-4B --train data/sft.json --method sft --lora --r 8 --out ckpts/gen_sft

# 6. Generator DPO 微调
uv run ultrarag dpo-tune --model ckpts/gen_sft --pairs data/pref_pairs.json --lora --r 8 --out ckpts/gen_dpo

# 7. 评估与推理
uv run ultrarag eval --pipeline RAGAdaptation --eval data/eval_queries.json --out results/eval.json
```

---

## 8. 高级改进方向（Research / Production Focus）
1. 引入 learned reward model 替代完全规则化的 DPO 生成偏好对
2. 使用 cross-encoder re-ranker 做二阶段检索以提高检索精度
3. 对 long-context 場景使用 hierarchical embedding，并做 multi-hop 检索训练
4. 研究增量索引与在线微调（支持 streaming KB）
5. 更严格的生成事实性评估（FactScore、GPT-4o 人工审核）

---

## 9. 总结
- UltraRAG 的知识适配是通过数据构造 + embedding/generation 微调联合实现的，重点在高质量的合成数据与偏好对、以及硬负样本的选取。
- 建议的实验与 ablation 有助于明确各模块对整体性能的贡献，并指导如何在真实生产中部署最优 pipeline。

---

> 注：本文档为 UltraRAG 知识适配模块的专门读物，基于 `docs/UltraRag.pdf` 文件中的信息进行整理与实践建议。欲进一步把该文档转为 PDF (markdown -> pdf)，可使用仓库内 `src/md_to_pdf.py` 工具。