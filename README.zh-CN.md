# opc-develop

[English](README.md)

opc-develop 是一套面向 Claude Code / Codex 的产品开发 skill。它不是一条要求所有项目
从头跑到底的重流程，而是一组按场景组合的能力：日常小改用 `lite`，标准产品增量用
`build`，产品或架构判断不清时再按需调用决策 skill，发布与线上故障则进入独立的安全流程。

它的核心承诺是：**先跑通一条真实用户旅程，再用与当前版本绑定的证据说明完成到了哪一级。**
人类继续负责产品判断、设计品味和架构方向；agent 负责在明确边界内实现、验证并留下可复核证据。

> 0.5 改的是默认选路，不是删除原有架构。完整的 Harness、交付、反馈、度量和规则固化闭环
> 仍然存在；`brainstorm`、`demo`、`prd`、`architect` 从默认前置链变成了按需决策工具。

## 适合谁

opc-develop 主要为亲自承担产品与工程判断的人设计：OPC（一人公司）创始人、独立 Builder、
小型产品团队，以及由 PM 与架构师/Builder 组成的紧密搭档。你需要能判断“用户价值是否成立、
交互是否对、架构是否值得长期承担”；skill 帮你保护和执行这些判断，不替你假装拥有品味。

它尤其适合以下情况：

- 想让 agent 不只是写代码，还能从真实入口证明用户结果；
- 希望日常小改轻量、产品增量有证据、生产发布默认谨慎；
- 想看见命令、评审、Provider、返工和故障的真实成本，并逐步裁剪流程；
- 团队已有工具和 runbook，希望渐进接入，而不是换掉整套工程系统。

它不适合把所有产品判断外包给 agent，也不擅长主要难点是跨团队路线图、组织审批和资源谈判的
工作。没有人对产品和架构方向负责时，更多门禁只会制造形式感。

## 全景架构

![OPC-Develop 全景架构](assets/opc-develop-skills.zh-CN.png)

从上到下读这张图：

1. **Harness 层**让 agent 真正具备 `run`、`reset`、`observe`、`drive` 四种可执行能力。
2. **交付层**按预算选择 `vibe`、`lite` 或 `build`；需要长期决策时才在 `build` 前调用
   `brainstorm`、`demo`、`prd`、`architect`；之后由 `ship` 和 `deploy` 进入测试与生产。
3. **反馈层**把人类意见分为 `tune`、`revise`、`park`，在最早出错的层修复，而不是一直在
   代码末端打补丁。
4. **度量层**由 feature 账本、验收收据、错误账本和 `retro` 组成，把高价值失败压成
   Benchmark，并把有效规则下沉到脚本、hook 或结构化工件。

右侧的 `oncall` 处理线上故障；`harness` 补齐被交付过程暴露出来的运行能力缺口。

## 5 分钟上手

### 1. 安装

Codex：

```bash
codex plugin marketplace add wallkop/opc-develop --ref main
codex plugin add opc-develop@opc-develop
```

Claude Code 本地加载：

```bash
git clone https://github.com/wallkop/opc-develop.git ~/plugins/opc-develop
claude --plugin-dir ~/plugins/opc-develop
```

Claude Marketplace 的完整配置见 [docs/claude-code.md](docs/claude-code.md)。安装或更新后，
请新开一个 Codex / Claude Code 会话，让新的 skill 定义进入上下文。

### 2. 明确调用方式

Codex 使用 `$opc-develop:<skill>`；Claude Code 使用 `/opc-develop:<skill>`。自然语言也可以
触发 skill，但新人和关键任务建议显式指定，避免选路含糊。

```text
# Codex：日常小改
$opc-develop:lite 修复设置页保存按钮的重复提交，只改这个问题。

# Codex：标准产品增量
$opc-develop:build 在 4 小时预算内交付“用户可以导出本月账单”，先跑通一条真实核心旅程。

# Codex：先评估项目工作台能力
$opc-develop:harness 评估这个项目的 run/reset/observe/drive，只给证据和前三个缺口。
```

Claude Code 中把 `$` 调用改为 `/`：

```text
/opc-develop:lite 修复设置页保存按钮的重复提交，只改这个问题。
/opc-develop:build 在 4 小时预算内交付“用户可以导出本月账单”。
```

### 3. 先选最小路径

先问两个问题：**它是否需要进入测试/生产发布？它能否在一个小时内完成？**

| 路径 | 什么时候用 | 会做什么 | 不会做什么 |
| --- | --- | --- | --- |
| `vibe` | 你明确只要最快代码，并亲自验收 | 直接修改，交给人看 diff | 不测试、不运行、不生成证据，不能声称可发布 |
| `lite` | 单一结果，可信预计不超过 60 分钟 | 定向测试 + 一次真实入口检查 | 不创建 feature 工件，不派 subagent |
| `build` | 单一产品增量，预计 1～4 小时 | 一页结果卡、真实核心旅程、可运行切片、两次评审、新鲜收据 | 不前置生成全套 PRD/技术文档 |
| `build` quick | 即使不到 60 分钟，但必须进入 `ship` / `deploy` | 走精简增量，但保留发布所需收据与评审 | 不能用 `lite` 绕过发布证据 |
| 拆分 | 超过 4 小时，或包含多个可独立使用的结果 | 先拆成多个标准增量，只实现第一个 | 不在一个增量里铺开全部范围 |

![OPC-Develop 预算选路图](assets/opc-develop-routing.zh-CN.png)

这张图只是**选路图和单次增量流程**，不是全景架构图。

### 4. 决策 skill 是叠加条件，不是必经前置

| 仍然不确定的事情 | 先用哪个 skill | 何时可以跳过 |
| --- | --- | --- |
| 产品价值、用户、非目标或核心行为还说不清 | `brainstorm` | 已经能清楚写出用户动作、可见结果和非目标 |
| 页面或交互“感觉对不对”无法靠文字决定 | `demo` | 交互已有明确设计或变更不是体验型工作 |
| 状态机、权限、长期产品规则或 PM→架构交接需要留档 | `prd` | 普通 1～4 小时增量，没有长期产品契约 |
| 公共 API/事件/schema 边界或单向技术决定发生变化 | `architect` | 实现沿用现有架构，决定可逆且局部 |

默认不是 `brainstorm → demo → prd → architect → build` 全部跑一遍。默认是直接从清楚的请求
进入 `lite` 或 `build`，只为真实存在的不确定性增加对应 skill。

## 哪个 skill 在什么场景做什么

### 日常交付

| Skill | 典型场景 | 主要结果 | 下一步 |
| --- | --- | --- | --- |
| `vibe` | 一次性实验、你明确接受未验证代码 | 代码 diff + “未运行测试”说明 | 人工检查；若要发布，重新走 `build` |
| `lite` | bug、文案/布局、配置、小行为调整 | 修改、最小回归、真实入口前后对比 | 完成；若范围扩成多切片，转 `build` |
| `build` | 清晰的 1～4 小时产品增量；发布型快速修复 | `feature-plan.md`、实现、回归、`acceptance.json`、评审记录 | 本地完成后进入 `ship` |

### 按需决策

| Skill | 典型场景 | 主要结果 | 下一步 |
| --- | --- | --- | --- |
| `brainstorm` | 原始想法模糊，需要逐个问题拷打 | `requirement.md`、风险画像、非目标、feature 分支 | 默认 `build`；体验不清再 `demo` |
| `demo` | UI/交互品味未确定，需要先体验 | 真实应用壳中的原型、`prototype.md`、`mock-inventory.md` | 默认 `build`；长期产品规则再 `prd` |
| `prd` | 权限/状态/长期行为需要产品契约，或 PM 交接 | `prd.md`、编号 AC/PD、黑盒 `testcases.md`、签署报告 | 默认 `build`；公共边界变化再 `architect` |
| `architect` | 公共边界、不可逆技术选择、跨角色架构交接 | intake、风险 spike、`technical.md`、编号 TD、签署报告 | `build` |

### 发布、故障和改进

| Skill | 典型场景 | 主要结果 | 下一步 |
| --- | --- | --- | --- |
| `ship` | `build` 已达到新鲜的真实服务核心旅程 | 测试环境部署、同一核心旅程回归、人工验收、合并主干 | 人类选择是否 `deploy` |
| `deploy` | 已人工验收并合入主干，需要生产发布 | fail-closed 预检、备份/回滚、生产回归、观察窗口、MD/HTML 交接 | 稳定后关闭；异常转 `oncall` |
| `oncall` | 测试或生产出故障 | 严重度分诊、证据链、诊断报告、回滚/热修/缓解、错误账本 | 长期修复按 `lite` / `build` / 决策 skill 重新进入 |
| `harness` | agent 无法稳定启动、清状态、追踪请求或执行 E2E | 四动词评分、可执行脚本/seed/日志约定、薄 `AGENTS.md` 索引 | 关闭最高杠杆缺口后回到交付 |
| `retro` | 已积累多次增量/故障，想减少返工和流程成本 | 成本与复发报告、Benchmark 证据、待批准规则/裁剪建议 | 人工批准后在最低层执行 |

## 常见需求的推荐组合

| 需求 | 推荐组合 | 原因 |
| --- | --- | --- |
| 改一个按钮文案或修一个局部 bug | `lite` | 单一结果，不值得创建 feature 工件 |
| 30 分钟热修，但必须当天发布 | `build` quick → `ship` → `deploy` | 发布需要版本绑定的证据，不能走 `lite` |
| 新增一个边界清楚的导出功能 | `build` | 默认标准增量，不需要先写 PRD |
| “做一个 AI 学习教练”，用户和价值还不清 | `brainstorm` → `build` | 先解决产品判断，再实现第一条旅程 |
| 新结算页的交互还没定 | `demo` → `build` | 先用可体验原型解决品味问题 |
| 新权限模型 + 公共 API | `prd` → `architect` → `build` | 同时存在长期产品契约与公共技术边界 |
| 一个需求包含后台、移动端、运营台三个独立结果 | 拆分 → 第一个 `build` | 多个可独立交付旅程不能塞进一次增量 |
| 线上错误率突然上升 | `oncall` | 先证据化诊断和稳定系统，不直接猜修复 |
| agent 每次都在猜启动命令和测试数据 | `harness` | 问题是工作台能力，不是 feature 实现 |

## 最佳实践

1. **从用户动作写起。** 请求里说清“谁从哪个真实入口做什么，看到什么结果”，不要只给
   “做完某模块”这种内部任务名。
2. **按预算和结果数量选路。** 风险只增加对应检查，不自动升级成全套文档链；但需要发布的
   快修必须用 `build` quick。
3. **一个增量只保一条核心旅程。** 多条可独立使用的旅程先拆分；第一片在 45 分钟内穿过
   正式 router/service/页面组装，后续每片 30～90 分钟并保持前一片可运行。
4. **决策工件只为长期判断服务。** 不确定产品意图用 `brainstorm`，不确定体验用 `demo`，
   不确定长期产品契约用 `prd`，不确定公共/单向技术边界用 `architect`。不要把它们当模板清单。
5. **验证从便宜到昂贵。** 逻辑/build → 本地正式服务 + scratch 状态 → UI 浏览器核心旅程 →
   Provider 离线回放 → 一次真实 canary → 人工验收。
6. **UI 必须由浏览器执行关键动作。** 通过 API 造出结果再用浏览器查看，只证明读路径，不能
   证明用户能从 UI 完成操作。
7. **不要拿真实 Provider 当调试循环。** 先稳定本地与离线回放，同一版本默认只做一次真实调用。
8. **把反馈路由到最早错误层。** `tune` 是同一意图的执行调整；`revise` 是上游事实错了并使
   下游证据失效；`park` 是干净停止。
9. **以收据状态而不是测试数量宣称完成。** 代码、测试、结果卡、seed 或配置改变后，旧命令
   结论会自动变旧。
10. **有数据再跑 `retro`。** 建议先积累 3～5 个标准增量或一次高价值故障；没有采集数据时，
    `retro` 应报告缺口，而不是编造效率结论。

## 独立 Builder 和 PM 搭档怎么用

**独立 Builder** 不需要制造交接工件。需求和边界清楚时直接 `build`；只有自己的产品判断、
体验判断或架构判断尚未收敛时，才在前面增加相应决策 skill。

**PM + 架构师/Builder** 可以沿判断边界交接：

1. 产品负责人按实际不确定性使用 `brainstorm` / `demo`，并用 `prd` 固化需要长期存在的
   PD/AC 与黑盒 testcase；
2. `prd` 提交并推送 feature 分支，交接摘要列出 AC、风险、开放问题和 Harness gap；
3. Builder 拉取分支并做 intake；只有公共边界或单向技术决定变化时才运行 `architect`，
   否则直接 `build`；
4. Builder 不替产品负责人静默回答缺失的产品判断，问题以 `revise` 返回最早责任层；
5. `ship` 的测试环境验收是双方重新看见真实结果的共同触点。

## 新项目怎么落地

新项目不需要先建立完整文档体系。第一目标是让 agent 能稳定地运行、清状态、观察和驱动系统。

### 第 0 天：建立最小 Harness

在仓库的新会话中执行：

```text
$opc-develop:harness 初始化这个新项目的最小 Harness。先补 run 和 reset，再建立一个具名 seed，
然后证明一次 observe 链和一条 drive 旅程；AGENTS.md 只做命令索引，不堆说明。
```

最小可用标准：

- 一条命令启动目标栈并能检查健康状态；
- 一条幂等 reset 命令和至少一个具名 seed；
- 一次用户动作可以通过 correlation ID 串起日志，并能只读检查状态；
- 至少一条从真实入口执行的 Tier-1 核心旅程；
- 凭据、生产数据和 `.env` 不进入仓库。

空仓库也可以从 `run` / `reset` 开始；opc-develop 不替你决定框架和产品方向，必要时先用
`brainstorm` 明确第一条用户价值，再让 `build` 创建最小可运行产品切片。

### 第 1 个功能：只交付一条旅程

- 意图清楚：直接 `$opc-develop:build ...`。
- 产品意图不清：`$opc-develop:brainstorm ...`，确认后进入 `build`。
- 体验不清：先 `demo`，感觉确认后进入 `build`。
- 第一轮不要同时引入 PRD、架构文档、完整 CI 和生产部署；只添加真实需要的能力。

### 第一次发布

准备好测试环境 runbook 后使用 `ship`；只有 `ship` 的人工验收和主干合并完成，才进入
`deploy`。生产发布必须有回滚路径、备份和观察窗口，缺任何一项都停止而不是临场发明。

### 稳定后的节奏

- 日常小改：`lite`；
- 产品增量：`build`；
- 测试验收：`ship`；
- 生产发布：`deploy`；
- 3～5 个增量后：`retro`；
- 交付暴露出 run/reset/observe/drive 缺口时：回到 `harness`。

## 老项目怎么接入

老项目应渐进接入，**不要大爆炸迁移**现有文档、CI、测试和发布系统。

### 第一步：只评估，不先重建

```text
$opc-develop:harness 只评估现有项目的 run/reset/observe/drive。实际执行已有命令，
不要先修改项目；列出证据、真实性上限和前三个最高杠杆缺口。
```

保留已有 Makefile、npm scripts、Docker Compose、测试框架、CI 和 runbook。`harness` 应把它们
组织成稳定入口，只有能力缺失时才补脚本，不另造一套平行工具。

### 第二步：从日常 `lite` 开始

选择一周内真实发生的小改，验证 opc-develop 能否：保持范围、跑定向测试、从真实入口检查
结果、诚实报告证据。此阶段不要求创建 `docs/features/`。

### 第三步：选一个低风险功能试点 `build`

选择一条清楚、可回滚、1～4 小时的核心旅程。让它第一次生成：

```text
docs/features/<slug>/feature-plan.md
docs/features/<slug>/acceptance.json
docs/features/<slug>/ledger.jsonl
```

观察 45 分钟首切片、两次评审、收据新鲜度是否真正减少假绿；不要一开始就把所有旧功能
补写成 PRD 或 testcase。

### 第四步：发布流程单独接入

现有测试/生产 runbook 可直接被 `ship` / `deploy` 使用。先在一个低风险增量上接入测试环境，
再决定是否让生产发布进入 opc-develop。没有明确 runbook 和回滚能力时，不要启用 `deploy`。

### 兼容原则

- 旧的 requirement/demo/PRD/technical 工件继续有效；存在时会成为 `build` 的约束，不需要重写。
- 没有这些可选工件也不是 gap，普通新功能可以直接写一页结果卡。
- 历史 v2 账本仍可读取；新标准增量使用 v3 账本与生成式 `acceptance.json`。
- 不回填历史 feature，不替换已有测试，不要求一次性安装 hook；是否把门禁接进 CI 由人明确决定。

## `build` 到底会做什么

```mermaid
flowchart LR
  A["预算门"] --> B["一页结果卡"]
  B --> C["核心旅程先真实失败"]
  C --> D["45 分钟纵向切片"]
  D --> E["现实评审"]
  E --> F["30～90 分钟可运行切片"]
  F --> G["由便宜到昂贵验证"]
  G --> H["最终评审"]
  H --> I["新鲜验收收据"]
```

默认只创建 `docs/features/<slug>/feature-plan.md`，其中记录用户动作、真实入口、可见结果、
非目标、数据来源、两条安全条件、核心旅程、切片和验收命令。`opc_increment.py` 生成
`acceptance.json` 并把命令结论绑定到当前内容树。

完成等级只有四级：

1. `code-build`：当前版本通过构建/逻辑层；
2. `automated-core-journey`：自动化核心旅程通过；
3. `real-service-core-journey`：通过本地正式服务组装和真实入口；
4. `human-accepted`：人类对当前候选版本明确验收。

标准增量只有两个代码评审点：首条纵向切片后的现实评审，以及全部范围集成后的最终评审。
两个评审合计最多两轮修复；仍有阻断则缩小范围或重做设计，不能无限补丁。

常用机械检查：

```bash
python3 shared/scripts/validate_artifacts.py docs/features/<slug>/feature-plan.md
python3 shared/scripts/opc_increment.py check \
  --receipt docs/features/<slug>/acceptance.json \
  --require real-service-core-journey
python3 shared/scripts/opc_ledger.py audit --require-increment-complete \
  --ledger docs/features/<slug>/ledger.jsonl
```

## 发布与故障边界

- `ship` 只负责测试环境：预检、变更清单、部署、同一核心旅程回归、人工验收、合并主干。
- `deploy` 只负责生产：固定 release set、在最终主干刷新收据、备份/回滚、部署、prod-safe 回归、
  观察窗口；每个破坏性步骤都需要人类确认。
- `oncall` 先分诊和证据化诊断。回滚、热修复和缓解由人选择；发布型热修仍需
  `build` quick → `ship` → `deploy`，加速不等于不验证。

## 仓库与项目工件

插件仓库：

- `skills/`：12 个用户入口；
- `shared/core-contract.md`：预算、证据、完成等级、反馈和安全底线；
- `shared/packs/`：按需加载的实现、风险、评审、发布、Harness 规则；
- `shared/formats/`：结果卡、收据、PRD、技术、测试、账本格式；
- `shared/rubrics/`：独立评审清单；
- `shared/scripts/`：标准库 Python 的结构校验、收据、账本、Benchmark 和报告工具；
- `agents/`、`shared/prompts/`：冷上下文 reviewer 与例外 implementer 角色。

项目工件永远写入目标项目的 `docs/features/<slug>/` 和 `docs/opc/`，不写回插件仓库。

## 更新

Codex Marketplace 安装：

```bash
codex plugin marketplace upgrade opc-develop
codex plugin add opc-develop@opc-develop
```

本地 clone：

```bash
cd ~/plugins/opc-develop
git pull --ff-only
```

更新后新开会话。

## 开发与验证

```bash
python3 shared/scripts/test_opc_scripts.py
python3 shared/scripts/opc_benchmark.py validate shared/fixtures/opc-benchmark/registry.json
python3 shared/scripts/opc_benchmark.py run shared/fixtures/opc-benchmark/registry.json --repo .
```

## 安全与语言

项目 `AGENTS.md` 的目标语言规则约束对话、工件、评审和报告；解析器要求的 key、token、ID
和命令保持固定拼写。插件仓库不得包含业务数据、凭据、私有日志、`.env` 或项目生成工件。

破坏性操作、生产变更、权限/安全变更、不可逆 schema/数据操作、force-push 和对外发布，
始终需要人类显式批准。

## License

MIT
