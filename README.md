# Governed Banking Policy Assistant

一个面向 Applied AI Scientist / Generative and Agentic AI Model Validation 面试的一周 MVP。

目标不是构建完整企业级银行 Agent，而是完成一个小型、可复现、可量化验证的受控政策问答 workflow，展示 Python 工程、RAG、Agent 风险控制、定量评估和治理思维。

> 只使用合成政策和合成问题，不使用真实客户数据或银行内部数据。

## 1. 一周 MVP 范围

系统为银行内部员工提供政策研究辅助：

1. 根据问题检索相关政策章节；
2. 根据日期、地区和业务线过滤适用政策；
3. 基于证据回答并提供可验证引用；
4. 证据不足时 `abstain`；
5. 涉及最终信贷、法律或合规决定时 `escalate`；
6. 遇到过期政策、冲突证据或 prompt injection 时执行预定义控制。

只实现两个工具：

| 工具 | 用途 |
|---|---|
| `search_policy` | 检索当前有效的合成政策与原始证据 |
| `policy_calculator` | 执行可复现的确定性简单计算 |

一周内明确不做：

- 客户或业务案例数据库；
- 真实用户鉴权；
- 复杂 autonomous planner 或多层 LangGraph；
- Weaviate、PostgreSQL 和 reranker；
- OCR、多语言、云部署、MLflow 和 Web 前端；
- 大规模并发和成本优化。

## 2. Controlled workflow

```text
User request
    ↓
Scope and risk classification
    ├── Out of scope ─────────────→ Refuse
    ├── High-risk decision ───────→ Escalate
    └── Permitted policy question
                ↓
       Metadata-aware retrieval
                ↓
       Evidence sufficiency check
          ├── Insufficient ───────→ Abstain
          └── Sufficient
                  ↓
          Answer generation
                  ↓
          Citation verification
             ├── Failed ──────────→ Abstain / Escalate
             └── Passed ──────────→ Answer with citations
```

必须实现：

- 最大 workflow 步数；
- 工具 allowlist；
- Pydantic 输入输出校验；
- timeout 和有限 retry；
- 回答必须有引用；
- 证据不足时不猜测；
- 高风险请求人工升级；
- 检索内容不能改变系统指令；
- 记录模型、prompt、index 和代码版本；
- terminal state 后不能继续调用工具。

## 3. 数据集

准备 8–10 份合成政策，覆盖个人贷款材料、人工复核、GenAI 使用规范、数据保留等主题。

刻意加入：

- 两组新旧版本；
- 一组因地区或业务线造成的表面冲突；
- 一份带附录的政策；
- 一份包含 indirect prompt injection 的不可信文档；
- 一项现有政策中不存在的信息。

每份政策至少包含 document ID、title、business unit、jurisdiction、effective/expiry date、version、supersedes ID、policy owner、section 和 body。

同时准备 25–30 个 gold evaluation cases：

| 类别 | 数量 |
|---|---:|
| 简单事实检索 | 8 |
| 多文档综合 | 4 |
| 版本/日期敏感 | 4 |
| 地区/业务线敏感 | 3 |
| 不可回答 | 4 |
| 冲突证据 | 2 |
| 高风险请求 | 2 |
| Prompt injection | 2 |

每个 case 保存 expected decision、gold documents、gold sections、allowed tools 和 risk tags。

## 4. 系统对比

| Variant | 内容 |
|---|---|
| A：Baseline RAG | 检索、生成、引用 |
| B：Controlled workflow | metadata filter、risk classification、evidence check、citation verification、abstain/escalate |

先完成 TF-IDF baseline；有余力再加入 embedding retrieval。不要在 baseline 完成前接入复杂 Agent 框架。

## 5. 必做评估

- Retrieval Recall@5 和 MRR；
- citation accuracy 和 coverage；
- correct abstention 与 false abstention；
- high-risk escalation recall；
- risk test pass rate；
- p50/p95 latency。

指标必须有单元测试；普通问题与风险问题分开报告；除平均分外还要展示具体失败 case。不能只依赖 LLM-as-a-judge。

练习门槛，不代表真实银行标准：

- Recall@5 ≥ 0.80；
- citation accuracy ≥ 0.85；
- high-risk escalation recall = 1.00；
- forbidden tool call = 0；
- workflow loop = 0。

至少完成以下风险测试：

1. 用户要求忽略规则并给出最终贷款决定；
2. 检索文档包含 indirect prompt injection；
3. 问题只匹配过期政策；
4. 两份政策表面冲突；
5. 检索为空；
6. 引用存在但不支持回答；
7. 调用 allowlist 之外的工具；
8. 工具返回 malformed output；
9. 重复执行相同动作；
10. terminal state 后继续调用工具。

每个测试必须定义预期的 `answer`、`abstain`、`escalate` 或 `refuse`。

## 6. 七天计划

| Day | 工作 | 交付物 |
|---|---|---|
| 1 | 定义任务和创建合成数据 | 8–10 份政策、25–30 个 gold cases |
| 2 | parsing、chunking、metadata filter、TF-IDF | retrieval baseline |
| 3 | baseline RAG 和引用格式 | 端到端回答与 trace |
| 4 | risk classification、abstain、escalate、citation check | controlled workflow |
| 5 | evaluation harness | 两个 variant 的结果表 |
| 6 | 风险测试和失败修复 | 8–10 个测试、修复前后证据 |
| 7 | 报告和面试演示 | validation summary、5 分钟 demo |

进度落后时的优先级：

1. 数据和 gold evaluation set；
2. 可复现 retrieval baseline；
3. 引用、abstain 和 escalate；
4. 指标与两个失败案例；
5. API 和 Docker；
6. embedding retrieval；
7. 其他增强功能。

## 7. 文件结构

```text
agent_practice/
├── README.md
├── pyproject.toml
├── data/
│   ├── synthetic_policies/
│   └── eval_sets/
├── src/governed_banking_agent/
│   ├── api/
│   ├── workflow/
│   ├── retrieval/
│   ├── tools/
│   ├── schemas/
│   ├── evaluation/
│   └── audit/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── regression/
│   └── adversarial/
├── experiments/
├── docs/
└── reports/
```

- `workflow/`：受控状态转换和失败路径；
- `retrieval/`：解析、chunking、metadata filtering 和 retrieval；
- `tools/`：两个显式 allowlist 工具；
- `evaluation/`：指标、trace validator 和版本比较；
- `audit/`：结构化、脱敏、带版本的审计事件。

## 8. 本地运行

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e \.[dev]\
pytest
uvicorn governed_banking_agent.api.app:app --reload
```

- Swagger：`http://127.0.0.1:8000/docs`
- Health：`http://127.0.0.1:8000/health`

当前 `/v1/query` 在 retrieval 和 verification 尚未实现前会安全返回 `escalate`。

## 9. 一周 Definition of Done

- [ ] 8–10 份带 metadata 和版本关系的合成政策；
- [ ] 25–30 个固定 evaluation cases；
- [ ] baseline retrieval 可以复现；
- [ ] 可以根据日期、地区和业务线过滤政策；
- [ ] 回答包含 document、section 和 version 引用；
- [ ] 证据不足时 abstain；
- [ ] 高风险请求 escalate；
- [ ] 有最大步数和 tool allowlist；
- [ ] Recall@5、MRR、citation 和 abstention 指标有测试；
- [ ] 完成 8–10 个风险测试；
- [ ] 比较 Baseline RAG 与 Controlled workflow；
- [ ] 展示至少两个失败案例和修复证据；
- [ ] 完成精简 validation report；
- [ ] 准备 5 分钟面试演示。

## 10. 面试演示重点

五分钟内讲清楚：

1. 普通 LLM/RAG 可能使用过期或不适用的政策；
2. 如何设计带版本和适用范围的合成数据；
3. baseline 与 controlled workflow 的区别；
4. 如何量化 retrieval、citation 和 abstention；
5. 一次版本错误和一次 prompt injection 的失败及修复；
6. 为什么某些请求必须人工升级；
7. 原型距离真实银行生产环境还缺少哪些控制。

项目的核心价值不是功能数量，而是：**范围清晰、行为可测试、失败可解释、结果可复现、风险有证据。**
