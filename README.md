# 🕵️‍♂️ DeepResearch Agent: 基于大模型的多跳推理与自动化检索工作流

![Workflow](https://img.shields.io/badge/Workflow-PAI%20LangStudio-blue)
![LLM](https://img.shields.io/badge/LLM-Qwen3--Max-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)

---

## 项目简介
本项目为【寻找AI全能王：阿里云 Data+AI 全球大奖赛】的高阶 Agent 挑战赛开源项目。
这是一个处理**极度复杂、多跳约束、且包含模糊指代**的真实世界研究问题（Research Question）的智能体工作流。

本项目摒弃了传统的单轮 RAG 问答，在禁止模型微调的前提下，通过 **多步拆解规划 + 动态循环检索 + 严苛特征打分** 的纯 Prompt 与 Python 工具工程，实现了高鲁棒性的事实抽取与知识归一化。

## 🧠 系统架构与流转拓扑
本系统参考了 Plan-and-Execute 模式，并结合了严格的流程控制。整体架构分为四大核心阶段，各阶段关联文件、核心逻辑清晰拆分如下：

### Phase 1: 意图清洗与合规重构
- 关联文件：`prompts/question_confirm.txt`
- 核心逻辑：
  真实世界的业务经常会触发云厂商的安全风控机制（DataInspectionFailed）。
  本阶段强制 Agent 将问题中的敏感词（如 “外国基地”、“国家领导人”）替换为 “中立泛化代称”（如 “海外大型设施”、“官方高层”），在不改变语义约束的前提下，确保后续检索与生成的网络畅通。

### Phase 2: 降维拆解与规划
- 关联文件：`prompts/question_planning.txt`
- 核心逻辑：
  长难句是搜索引擎的杀手，本阶段强制大模型放弃 “一文搜全”，采用降维打法，核心动作包括：
  1. 指纹提取：切分出独特年代、物理特征、罕见理论。
  2. 精确碰撞法则：对特殊长词组强制添加双引号 ""（Exact Match）。
  3. 双语扩召回：除中国本土特有实体外，强制将线索翻译为英文检索组合，突破中文互联网的数据孤岛。

### Phase 3: 动态迭代取证
- 关联文件：`assets/iteration_loop.png`、`tools/smart_search_iqs.py`、`prompts/smart_search.txt`
- 核心逻辑：
  基于 While-Loop 结构构建的多轮检索验证引擎，核心流程分为两步：
  1. 动作执行：调用 `tools/smart_search_iqs.py` 从外部获取 Top 5 网页摘要。
  2. 打分与防幻觉：内置极度严苛的 “全特征打分 SOP”，要求 Agent 对候选实体的 “职业 / 时间 / 空间” 建立检查清单；引入 “细节一票否决制”，一旦年代或关联地点不符，强行熔断大模型的脑补与强行关联，立即抛弃该候选并进入下一轮检索。

### Phase 4: 格式阻断与静默兜底
- 关联文件：`prompts/generate_report.txt`
- 核心逻辑：
  针对自动化评测的归一化要求，设置最终输出防火墙，核心规则包括：
  1. 零容忍格式：强制屏蔽所有 “推理过程”、“语气词” 及 “标点符号”。
  2. Silent Fallback（静默兜底）：当且仅当迭代检索穷尽且证据链彻底断裂时，允许大模型调用内部预训练知识进行补救，但必须依然伪装成严格的实体输出格式，最大化提升容错率。

---

## 💡 核心工程创新点
按“创新点名称+关联文件+核心说明”分层整理，清晰易懂：

### 1. 大模型代码级容错 (Defensive Programming)
- 关联文件：`tools/extract_planning.py`
- 核心说明：
  针对 LLM 偶尔不按规范输出 JSON（如夹杂 Markdown 标记、忘写括号）的痛点，编写了多层正则匹配兜底算法。
  即使彻底解析失败，也能自动注入预设的 `fallback_steps`，确保整个长链路的 Pipeline 绝对不崩溃。

### 2. 状态记忆的优雅传递 (Memory Management)
- 关联文件：`tools/collect_search_info.py`
- 核心说明：
  在可视化工作流的循环节点中，通过该工具动态维护每轮的检索线索与历史结果，实现了类似于 LangChain Memory 的状态累加，为最终的报告生成提供全局视角。

### 3. 工具调用的退避机制 (Backoff Strategy)
- 关联文件：`tools/smart_search_iqs.py`
- 核心说明：
  在该工具的网络层处理中，直接将 API 并发限制（HTTP 429）纳入工具自身的逻辑闭环，通过 `time.sleep()` 结合多轮尝试，屏蔽了由于外部接口波动导致的工作流非正常中断。

---

## 📂 仓库目录结构
为了清晰展示大模型工作流的核心资产，本项目将 LangStudio 的可视化节点拆解为结构化的代码与提示词：

```text
.
├── 📁 assets/                  # 存放工作流可视化截图
│   ├── main_flow.png           # 全局工作流拓扑图
│   └── iteration_loop.png      # 核心迭代搜索（ReAct）循环子图
│
├── 📁 deepresearchworkflow/    # 工作流元数据 (LangStudio Export)
│   └── .export_metadata.json   # 包含原始的画布连线定义与节点参数
│
├── 📁 prompts/                 # 核心 Agent 提示词工程 (Prompt Engineering)
│   ├── question_confirm.txt    # [节点] 问题确认与云平台敏感词脱敏规则
│   ├── question_planning.txt   # [节点] 多维特征拆解与检索步骤规划
│   ├── background_keywords.txt # [节点] 中英双语降维策略与关键词提取
│   ├── smart_search.txt        # [节点] 智能搜索打分器与一票否决规则
│   └── generate_report.txt     # [节点] 终态报告生成、格式阻断与静默兜底
│
└── 📁 tools/                   # 自定义 Python 工具节点 (Tool Coding)
    ├── smart_search_iqs.py     # 阿里云 IQS 搜索引擎调用与防 429 退避策略
    ├── extract_planning.py     # 基于正则的鲁棒性 JSON 解析器（带解析灾难兜底）
    ├── collect_search_info.py  # 跨循环周期的上下文状态（Memory）管理与拼接
    ├── get_search_target.py    # 迭代目标切片控制
    ├── extract_ref_sites.py    # 摘要与参考源结构化提取
    ├── generate_bg_keywords.py # 关键词生成工具逻辑
    ├── summarize_question.py   # 问题总结流转控制
    └── update_step_count.py    # 循环步数累加器与中止条件守护

