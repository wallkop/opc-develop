# Artifact Boundary Contract

Full 流程中的 `technical.md`、`spec.md`、`plan/*.md` 分别服务不同读者，不能互相复制或替代。

## Core Boundary

- `technical.md`: 给人类架构师 review 的宏观技术决策和公共技术契约。
- `spec.md`: 给 AI 实现者执行的微观实现契约。
- `plan/*.md`: 给 controller/implementer 编排开发顺序和边界，不承载技术细节。

## technical.md Must Own

- 唯一技术路线和组件选型。不得留下多个候选方案让后续 AI 决定。
- SaaS / 基础设施组件决策：datastore/database、cache、queue、object/blob storage、外部 API、模型 provider、鉴权服务、审计服务等。
- 涉及新增或变更数据存储时，必须遵循项目既有架构基线、既定事实或已批准的人类架构决策；如果没有基线或存在冲突，必须先阻塞并请求人类决策，不能由 AI 隐式选择。
- API 公共输入输出定义：endpoint、method、request schema、response schema、status code、error code、auth/permission boundary、外部依赖失败的公共响应语义。
- 系统边界、source of truth、跨服务关系、数据一致性、事务、补偿、迁移、回滚、运行证据和 gate 分层策略。
- UI-facing work 的 demo 到生产模块映射：真实路由、组件、状态 owner、设计系统约束和允许偏离点。

## technical.md Must Not Own

- 具体代码结构、类/函数拆分、内部模块落点。
- API 的内部实现步骤。
- 本地组件细节，例如 sqlite、本地文件存储、本地缓存、内存状态结构。
- 单测/API 测试的 TDD seed 细节。
- plan worker 的执行步骤。

## spec.md Must Own

- API 内部实现契约：controller/service/provider/tool 如何协作、错误如何在内部映射、哪些模块负责哪些内部行为。
- 具体模块落点、代码结构拆分、本地组件决策：sqlite、本地文件存储、本地缓存、内存状态等。
- UI 状态机、交互细节、组件责任、demo parity 的可执行约束。
- 内部校验规则、内部调用顺序、并发/race guard、缓存失效、tool/agent metadata、Runtime Evidence 细节。
- 单元测试、API 测试、focused implementation-facing 测试的 TDD seed。
- 对 demo、PRD、technical 公共契约的执行映射。

## spec.md Must Not Own

- 新增或替换 SaaS / 基础设施组件。
- 改写 technical 已定义的 API 公共输入输出。
- 架构方案比较、组件选型比较、宏观取舍理由。
- 模糊语句：TODO、TBD、可选方案、后续决定、类似实现、适当处理。

## plan/*.md Must Own

- workstream / task 拆分边界。
- 开发顺序、依赖关系、串并行条件。
- 每个 worker 的允许修改边界和禁止修改边界。
- 需要读取的输入文件和引用位置；可具体到文件、章节、行号或行号区间。
- 每个任务引用的 spec 条目、demo/PRD/technical 来源条目。
- integration order、handoff 到 `local-e2e-verify` / `release-verify` 的边界。

## plan/*.md Must Not Own

- API schema、错误码矩阵、数据库设计、组件选型、算法细节、内部实现步骤。
- RED/GREEN 命令和具体 TDD 测试设计；这些属于 `spec.md` TDD seed 和 `tdd-coding` 执行。
- 产品行为、技术方案或 spec 的重复解释。
- 新技术决策或对 technical/spec 的覆盖。

## Routing Rules

- 如果 create-spec 发现 API 公共输入输出、SaaS 组件或数据存储基线未在 technical 中明确，停止并路由回 `create-technical`。
- 如果 create-plan 需要补技术细节才能让 worker 执行，停止并路由回 `create-spec` 或 `create-technical`，不要把细节写进 plan。
- 如果 review 发现下游 artifact 与上游 Approved artifact 冲突，必须路由到最早受影响层级，而不是在当前层 patch around。
