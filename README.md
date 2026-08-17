# Applied AI Scientist 面试练手项目

> 目标岗位：Generative and Agentic AI Model Validation / Model Risk Management  
> 核心目标：同时练习 Python 工程、RAG、Agent workflow、量化评估、安全测试、模型治理和面试表达。

---

## 1. 项目组合总览

建议完成一个主项目和两个短项目：

| 项目 | 主要能力 | 建议耗时 | 优先级 |
|---|---|---:|---:|
| 项目一：银行政策与风险研究 Agent | 端到端 RAG/Agent、模型验证、治理和审计 | 2–3 周 | 最高 |
| 项目二：Agent Evaluation Coding Lab | Python、指标实现、测试、数据分析 | 2–4 天 | 高 |
| 项目三：Faulty Agent 审查与加固 | 代码审查、失败分析、安全控制 | 2–3 天 | 高 |

如果时间有限，只做项目一，但必须完成其中的 baseline、Agent、evaluation、adversarial testing 和 validation report，不能只做一个能演示的聊天界面。

---

# 项目一：银行政策与风险研究 Agent

## 2. 项目背景

设计一个供银行内部员工使用的 AI Agent，帮助员工查询和比较内部政策，例如：

- 某项贷款产品需要哪些申请材料；
- 某类业务的审批权限和人工复核要求；
- 新旧版本政策之间有什么变化；
- 某个合成案例触发了哪些风险规则；
- 根据公开或合成数据完成简单计算，并引用计算来源；
- 当证据不足、政策冲突或问题超出权限时拒绝作答或升级给人工。

Agent 只提供政策信息、证据和辅助分析，不自动做最终信贷、合规或客户资格决定。

建议项目名：

`Governed Banking Policy & Risk Research Agent`

## 3. 为什么这个项目适合目标岗位

这个项目可以覆盖 JD 中最重要的四条能力线：

1. **构建能力**：Python、FastAPI、Pydantic、RAG、LangGraph、多工具调用。
2. **验证能力**：检索指标、回答指标、Agent workflow 测试、鲁棒性测试。
3. **风险意识**：prompt injection、越权调用、错误政策版本、PII、错误自动决策。
4. **治理能力**：版本记录、测试证据、trace、模型卡、validation report、上线条件。

## 4. 推荐技术栈

- Python 3.11+
- FastAPI + Pydantic
- LangGraph，或自行实现一个轻量状态机作为对照
- FAISS 或 Weaviate
- BGE-M3 或其他 embedding model
- 可选 reranker
- PostgreSQL 或 SQLite，用于存储合成案例和审计记录
- Pandas、NumPy、scikit-learn
- pytest
- MLflow，可选
- Docker
- GitHub Actions

不要一开始堆满所有框架。先用最少依赖完成可测试的 baseline，再逐步增加 Agent 和控制措施。

---

## 5. 业务范围与合成数据

### 5.1 文档集

创建 30–50 份合成银行政策文档，每份包含：

- `document_id`
- `title`
- `business_unit`
- `jurisdiction`
- `effective_date`
- `expiry_date`
- `version`
- `confidentiality_level`
- `supersedes_document_id`
- `policy_owner`
- 正文和章节编号

文档主题可以包括：

- 信贷材料要求；
- 客户身份验证；
- 人工审批和升级规则；
- 数据保留；
- 模型输出使用规范；
- GenAI 员工使用政策；
- 第三方风险管理；
- 事件上报流程。

### 5.2 刻意加入的困难样本

文档集不能过于干净，应主动加入：

- 两个版本内容相似，但只有最新版有效；
- 不同省份或业务线有不同规则；
- 两份文档表面冲突，实际适用范围不同；
- 附录修改了正文中的默认条件；
- 扫描/OCR 造成数字或章节错误；
- 文档中嵌入间接 prompt injection，例如要求模型忽略系统指令；
- 已过期政策；
- 文档缺页或元数据缺失。

### 5.3 合成案例数据库

创建 100–200 条完全虚构的业务案例。只保留最少必要字段，例如：

```text
case_id
province
product_type
requested_amount_band
customer_type
document_status
risk_flags
assigned_reviewer_role
```

不要使用真实客户信息。将案例工具设计为只读，并根据用户角色限制可见字段。

---

## 6. 功能需求

Agent 至少拥有三个工具：

### Tool 1：`search_policy`

- 混合或向量检索政策；
- 支持 `effective_date`、`jurisdiction`、`business_unit` 过滤；
- 返回文档 ID、章节、版本、分数和原始证据；
- 默认排除过期版本；
- 不执行文档中出现的任何指令。

### Tool 2：`get_case_summary`

- 从合成案例库读取最少必要字段；
- 输入使用 Pydantic schema；
- 对 `case_id`、调用者角色和可见字段做校验；
- 保留调用日志；
- 禁止修改案例数据。

### Tool 3：`policy_calculator`

- 完成确定性的简单计算；
- 不让 LLM 自己完成关键算术；
- 返回计算步骤、输入来源和结果；
- 对单位、范围和空值进行校验。

### Agent 输出格式

```json
{
  "answer": "...",
  "citations": [
    {
      "document_id": "POL-001",
      "section": "4.2",
      "version": "3.0",
      "evidence": "..."
    }
  ],
  "decision": "answer | abstain | escalate",
  "limitations": ["..."],
  "trace_id": "..."
}
```

---

## 7. Agent workflow

建议实现以下状态图：

```text
Request
  ↓
Authentication / Role Check
  ↓
Input Classification
  ├── Out of scope → Refuse
  ├── High-risk decision → Human escalation
  └── Permitted request
          ↓
        Planner
          ↓
     Tool allowlist check
          ↓
       Tool execution
          ↓
   Evidence sufficiency check
      ├── Insufficient → Retry once / Abstain
      └── Sufficient
              ↓
       Answer generation
              ↓
       Citation verifier
          ├── Fail → Abstain / Escalate
          └── Pass → Return answer
```

### 必须实现的 workflow 控制

- 最多执行固定步数，例如 5 步；
- 每个工具有 allowlist 和独立 schema；
- 工具 timeout、有限次数 retry 和明确 fallback；
- 无法解析的 tool output 不能直接传给下游；
- 相同失败动作不能无限重复；
- 高风险请求必须 human-in-the-loop；
- 每次运行记录模型、prompt、embedding、index 和代码版本；
- 所有回答必须有证据，证据不足时 abstain；
- 文档内容不能改变系统权限和工具访问范围。

建议使用 typed state：

```python
class AgentState(BaseModel):
    trace_id: str
    user_role: str
    query: str
    intent: str | None = None
    step_count: int = 0
    tool_calls: list[dict] = []
    retrieved_evidence: list[dict] = []
    draft_answer: str | None = None
    decision: str | None = None
    errors: list[str] = []
```

在真正实现时，避免可变对象作为不安全的默认值；上面的结构只表示应包含哪些字段。

---

## 8. 分阶段实现任务

### Phase 0：风险与需求定义

在写 Agent 前先完成：

- intended use；
- prohibited use；
- 用户和权限边界；
- 高风险动作定义；
- failure taxonomy；
- 验收指标；
- 人工升级条件。

输出：`docs/system_card.md` 和 `docs/risk_register.md`。

### Phase 1：Single-pass RAG baseline

实现一个没有 Agent 的普通 RAG：

1. 文档解析和 schema validation；
2. chunking；
3. metadata-aware retrieval；
4. top-k evidence；
5. 基于证据回答并输出引用。

必须记录：

- 每次检索到哪些 chunks；
- 过滤掉哪些版本；
- latency；
- token/cost estimate；
- 最终引用。

### Phase 2：Planning-and-routing Agent

加入：

- intent classification；
- 多工具 routing；
- typed state；
- maximum steps；
- tool validation；
- citation verifier；
- abstain/escalate 路径。

这一阶段要能回答：为什么使用 Agent，而不是所有请求都使用固定 RAG pipeline？

### Phase 3：Evaluation harness

创建至少 100 个测试问题，并固定 train/development/test 边界。测试集建议如下：

| 类别 | 数量 | 示例 |
|---|---:|---|
| 单文档事实 | 20 | 某项政策的材料要求 |
| 多文档综合 | 15 | 比较两个业务线规则 |
| 版本敏感 | 10 | 某日期适用哪个政策版本 |
| 工具调用 | 15 | 查询合成案例后结合政策回答 |
| 不可回答 | 15 | 文档中不存在的信息 |
| 冲突证据 | 10 | 两份政策适用范围不同 |
| 权限/高风险 | 5 | 要求 Agent 直接批准申请 |
| 对抗输入 | 10 | prompt injection、工具劫持 |

每个 case 至少保存：

```json
{
  "case_id": "EVAL-001",
  "query": "...",
  "user_role": "analyst",
  "expected_decision": "answer",
  "gold_document_ids": ["POL-001"],
  "gold_sections": ["4.2"],
  "allowed_tools": ["search_policy"],
  "forbidden_tools": ["get_case_summary"],
  "risk_tags": ["version_sensitive"]
}
```

### Phase 4：Adversarial and robustness testing

至少实现下列攻击和故障：

- 用户直接 prompt injection；
- 检索文档中的 indirect prompt injection；
- 请求调用不存在的工具；
- 合法工具的非法参数；
- 越权读取案例；
- 工具 timeout；
- 工具返回 malformed JSON；
- 检索为空；
- 新旧政策冲突；
- 输入超长；
- 重复工具调用导致循环；
- citation 存在但不支持结论；
- 请求 Agent 做最终高风险决定；
- 模型或 prompt 版本变化造成回归。

为每种风险定义预期行为，而不是仅记录“Agent 回答得不好”。

### Phase 5：Audit readiness

每次执行至少记录：

- `trace_id` 和 timestamp；
- 用户角色，不保存不必要的身份信息；
- request category；
- model/prompt/index/code version；
- 检索结果和分数；
- tool name、validated arguments、状态和耗时；
- workflow transition；
- 最终 decision；
- citation verification 结果；
- error 和 fallback；
- 敏感字段脱敏状态。

日志应支持回答：

> “为什么这个回答在这个时间点使用了这份政策和这个工具？”

### Phase 6：独立验证报告

假设 Agent 是另一个开发团队提交的，而你是 Model Validation 团队。写一份独立报告，至少包含：

1. Executive summary；
2. System scope and intended use；
3. Architecture and data flow；
4. Conceptual soundness assessment；
5. Data and knowledge-base assessment；
6. Quantitative testing；
7. Agent workflow testing；
8. Robustness and security testing；
9. Limitations；
10. Findings and severity；
11. Remediation requirements；
12. Approval recommendation and conditions；
13. Ongoing monitoring plan。

---

## 9. 评估指标

### 9.1 Retrieval

- Recall@K；
- Precision@K；
- MRR；
- nDCG，可选；
- 有效版本检索率；
- 过期版本错误使用率。

### 9.2 Answer and evidence

- answer correctness；
- evidence/citation precision；
- citation coverage；
- groundedness；
- unsupported claim rate；
- correct abstention rate；
- false abstention rate。

不要只使用一个 LLM-as-a-judge 分数。至少组合：

- 可确定计算的自动指标；
- 规则检查；
- 人工标注子集；
- 经人工样本校准后的 LLM judge。

### 9.3 Agent workflow

- tool selection accuracy；
- tool argument validity；
- forbidden tool call rate；
- workflow completion rate；
- unnecessary tool call rate；
- loop/termination failure rate；
- human escalation recall；
- average steps per task。

### 9.4 Robustness and operations

- injection attack success rate；
- 权限绕过率；
- malformed output recovery rate；
- p50/p95 latency；
- error rate；
- cost per successful task；
- regression failure count。

### 9.5 示例验收门槛

以下数字用于练习，不应宣称为真实银行标准：

- Retrieval Recall@5 ≥ 0.85；
- citation precision ≥ 0.90；
- correct abstention ≥ 0.80；
- tool selection accuracy ≥ 0.90；
- forbidden tool call rate = 0；
- high-risk decision escalation recall = 1.00；
- 已知攻击集上的权限绕过率 = 0；
- loop/termination failure rate = 0；
- 所有测试结果可以根据版本重新生成。

---

## 10. 对照实验

至少比较以下系统：

| Variant | 目的 |
|---|---|
| A：Single-pass RAG | baseline |
| B：RAG + reranker | 测量 reranking 的边际收益 |
| C：Planning-and-routing Agent | 测量 Agent 对复杂任务的收益和成本 |
| D：Agent + verifier | 测量 verifier 对 groundedness 和 abstention 的影响 |

分析时不能只报告平均分。至少按下面维度切片：

- 单文档与多文档；
- 可回答与不可回答；
- 普通问题与对抗问题；
- 不同政策版本；
- 不同用户角色；
- 成功与失败工具调用。

最终应能回答：

- Agent 比普通 RAG 提高了什么？
- 代价是什么，例如延迟、成本和新的失败模式？
- verifier 是否真的有效，还是只增加 false abstention？
- 哪些场景不应使用 Agent？

---

## 11. 推荐仓库结构

```text
governed-banking-agent/
├── README.md
├── pyproject.toml
├── .env.example
├── data/
│   ├── synthetic_policies/
│   ├── synthetic_cases/
│   └── eval_sets/
├── src/
│   ├── api/
│   ├── agent/
│   │   ├── state.py
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── controls.py
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
├── reports/
│   ├── validation_report.md
│   └── test_evidence/
├── docs/
│   ├── system_card.md
│   ├── risk_register.md
│   ├── architecture.md
│   └── model_change_policy.md
├── Dockerfile
└── .github/workflows/test.yml
```

---

## 12. Definition of Done

项目完成时应满足：

- [ ] 有固定版本的合成政策数据和 evaluation set；
- [ ] Single-pass RAG baseline 可以复现；
- [ ] Agent 有 typed state、tool schemas 和 termination controls；
- [ ] 所有回答包含可验证引用，否则 abstain；
- [ ] 有 deterministic unit tests；
- [ ] 有 tool failure 和 malformed output integration tests；
- [ ] 有 prompt injection、越权和循环测试；
- [ ] 可以比较四个 system variants；
- [ ] 指标可按 risk tag 和场景切片；
- [ ] 保存版本化的测试证据；
- [ ] 有 findings、severity 和 remediation owner；
- [ ] 有独立 validation report；
- [ ] README 可以让面试官在五分钟内理解业务目标、架构、结果和限制。

---

# 项目二：Agent Evaluation Coding Lab

## 13. 项目目标

这个短项目专门模拟 45–90 分钟的 Python coding 面试。不要使用 LangChain/LangGraph；只使用标准 Python、Pandas、Pydantic 和 pytest。

## 14. 输入数据

创建三个 JSONL 文件：

1. `eval_cases.jsonl`：gold evidence、expected tools 和 expected decision；
2. `agent_outputs.jsonl`：回答、引用和 decision；
3. `agent_traces.jsonl`：逐步工具调用和状态变化。

故意加入：

- duplicate case；
- missing field；
- invalid decision；
- malformed tool arguments；
- 重复调用；
- 没有 citation 的回答；
- forbidden tool call；
- latency 缺失或为负数。

## 15. Coding exercises

### Exercise 1：Schema validation

用 Pydantic：

- 验证输入；
- 输出清晰 error；
- 区分 invalid test record 和真实 model failure；
- 生成 data-quality summary。

### Exercise 2：Retrieval metrics

自行实现：

- Recall@K；
- Precision@K；
- MRR；
- 按 `risk_tag` 分组的 macro average。

覆盖空 gold set、重复结果和 unknown document ID 等边界情况。

### Exercise 3：Agent workflow metrics

实现：

- tool selection accuracy；
- forbidden tool call rate；
- unnecessary tool call rate；
- termination failure；
- average steps；
- correct abstention 和 false abstention。

### Exercise 4：Trace validator

验证每条 trace：

- step number 连续；
- 不超过最大步数；
- 只调用 allowlist 中的工具；
- tool arguments 符合 schema；
- terminal state 之后没有继续调用；
- 每个 answered response 有 evidence；
- 高风险请求最终必须 escalate。

### Exercise 5：Regression comparison

比较两个 Agent 版本，输出：

- overall delta；
- 分场景 delta；
- 改善最大的类别；
- 回归最大的类别；
- 是否满足 release gates；
- 失败 case IDs。

### Exercise 6：Unit tests

至少写 15 个 pytest tests，包括：

- happy path；
- empty input；
- duplicate retrieval；
- invalid schema；
- forbidden tool；
- loop；
- evidence missing；
- version-sensitive failure。

## 16. 面试限时练习方式

第一次不限时完成；之后重新选题并按以下节奏练习：

- 5 分钟：澄清输入、输出和边界情况；
- 25 分钟：实现核心逻辑；
- 10 分钟：测试；
- 5 分钟：解释复杂度、设计选择和生产化改进。

面试时要边写边解释：

- 哪些输入被信任；
- 哪些错误属于数据问题；
- metric denominator 是什么；
- 空集合如何定义；
- 为什么这个实现便于审计和复现。

---

# 项目三：Faulty Agent 审查与加固

## 17. 项目目标

先实现一个故意存在问题的 Agent，再像 Model Validator 一样审查和加固它。这个项目训练的不是“写更多代码”，而是发现系统为什么不应该直接上线。

## 18. 故意植入的问题

在初始版本中放入以下缺陷：

- 用 `while not answer` 无限循环；
- 直接用 LLM 返回的工具名访问工具字典；
- tool arguments 不做 schema validation；
- 把完整客户记录发送给模型；
- 所有角色都能调用所有工具；
- 工具异常后自动无限重试；
- 将文档中的指令当成 system instruction；
- 总是检索最新上传文档，而不是当前有效版本；
- citation 只检查格式，不检查是否支持结论；
- 日志包含敏感字段；
- prompt、index 和模型版本未记录；
- 高风险决策没有人工复核；
- 测试只覆盖 happy path。

## 19. 你的任务

### Part A：Code review

为每个问题记录：

| 字段 | 内容 |
|---|---|
| Finding ID | 唯一编号 |
| Description | 问题是什么 |
| Evidence | 文件、函数、trace 或测试证据 |
| Impact | 可能造成什么后果 |
| Likelihood | 发生可能性 |
| Severity | Critical/High/Medium/Low |
| Recommendation | 修复建议 |
| Validation test | 如何证明已修复 |

### Part B：Hardening

按风险优先级修复，不要按文件顺序修复：

1. 权限和高风险动作；
2. 无限循环和失控工具调用；
3. 输入输出 schema；
4. evidence 和 citation；
5. 敏感数据和日志；
6. 版本、监控和回归测试。

### Part C：Independent retest

修复后重新运行原始攻击集，并检查：

- 原 finding 是否关闭；
- 修复是否引入新回归；
- residual risk 是否仍可接受；
- 是否需要上线条件或持续监控。

---

# 20. 四周练习计划

| 周次 | 任务 | 输出 |
|---|---|---|
| 第 1 周 | 数据、风险定义、Single-pass RAG | system card、baseline、20+ tests |
| 第 2 周 | 多工具 Agent、typed state、控制措施 | Agent API、workflow tests、trace |
| 第 3 周 | evaluation、对抗测试、对照实验 | metrics、failure analysis、regression report |
| 第 4 周 | validation report、coding lab、模拟面试 | 完整报告、演示、面试答案 |

如果只有一周：

1. 使用 15–20 份政策和 40 个 eval cases；
2. 只实现 policy search 和一个只读工具；
3. 比较 baseline、Agent、Agent + verifier；
4. 完成 10 个 adversarial cases；
5. 写一份 4–6 页 validation report。

---

# 21. 面试演示脚本

准备一个 5 分钟版本：

1. **问题**：内部政策复杂、版本多，普通 LLM 容易使用错误或过期证据。
2. **系统**：构建 metadata-aware RAG 和受控多工具 Agent。
3. **控制**：schema、allowlist、maximum steps、abstention、human escalation、audit trace。
4. **验证**：固定测试集，对比 baseline、Agent 和 verifier。
5. **结果**：报告 retrieval、citation、tool routing、abstention、robustness 和 latency。
6. **发现**：说明至少一个 Agent 失败模式，以及如何修复和回归测试。
7. **限制**：明确这是合成数据原型，离真实生产还有哪些差距。

再准备一个 15 分钟版本，能够打开：

- 一条成功 trace；
- 一条失败 trace；
- 一次 indirect prompt injection；
- 一个版本敏感问题；
- 一张按场景切片的指标表；
- 一个 validation finding 和修复证据。

---

# 22. 项目完成后应能回答的面试问题

## 架构

- 为什么需要 Agent，而不是固定 RAG pipeline？
- LangGraph state 中保存什么，什么不应保存？
- 如何阻止无限循环和重复工具调用？
- 为什么 tool input 和 final output 都需要 schema？
- 检索、routing、generation 和 verification 如何解耦测试？

## Evaluation

- Retrieval Recall@5 提高是否一定意味着答案更好？
- correct abstention 和 false abstention 如何权衡？
- 如何验证 citation 真正支持结论？
- 为什么不能只依赖 LLM-as-a-judge？
- 如何证明 Agent 比 single-pass RAG 值得增加的成本和风险？

## Model risk and governance

- 什么是 Agent 的 conceptual soundness？
- 如何验证 workflow，而不只验证最终答案？
- 模型、prompt 或知识库更新后，哪些测试必须重跑？
- 测试 evidence 怎样支持审计？
- 哪些缺陷会阻止上线，哪些可以通过 monitoring 接受？
- 如何保持开发团队与独立验证之间的适当分工？

## Failure analysis

- 一次失败来自 retrieval、routing、tool、generation 还是 verifier，怎样定位？
- 文档中出现 prompt injection 时为什么只做关键词过滤不够？
- 两份有效政策冲突时应该怎样处理？
- verifier 可能带来哪些新问题？
- 如何测试用户角色和工具权限组合？

---

# 23. 不要过度投入的部分

- 不需要做复杂前端，Swagger 或简单 CLI 足够；
- 不需要真实银行或客户数据；
- 不需要部署大型模型；
- 不需要十几个工具，三个受控工具比十个松散工具更有说服力；
- 不要只展示 happy-path demo；
- 不要把所有失败都交给另一个 LLM 判断；
- 不要宣称原型已经满足真实银行监管要求；
- 不要为了使用 Agent 而让确定性任务也交给 Agent。

这个项目最有价值的成果不是聊天页面，而是：**可复现的对照实验、清晰的失败分类、受控的 Agent workflow、完整测试证据，以及一份敢于指出系统限制的独立验证报告。**
