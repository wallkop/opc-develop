---
name: harness-init
description: "为新项目初始化 Harness：引导提问式，根据项目需求背景逐步明确技术栈、技术标准、技术组件、虚拟化环境与架构立项决策，产出符合 harness.zh-CN.md 要求的开发环境，并以验证用例证明环境真实可用。大量技术决策需要架构师深度参与，模型不代拍板。"
license: MIT
---

# harness-init

流程与 Harness 解耦：本 skill 是流程侧伸向 Harness 的手——只负责引导决策与搭建，
建成什么样以 `${CLAUDE_PLUGIN_ROOT}/docs/harness.zh-CN.md` 为权威。
技术选型是难以回头的重决策：每个问题给出推荐方案与理由，**由架构师确认**，
确认的选型与理由记入奠基 ADR。

## 引导提问（按建设路线分轮，每轮 5-10 问）

1. **项目画像**：应用形态（中后台 / 桌面 / 服务）？目标部署环境？团队既有约定与偏好？
   → 选定脚手架基线（参考 harness 文档第 2 章的形态基线）与语言约定。
2. **操作面先行**：服务怎么启动？日志采用什么结构？trace_id 如何创建与传播？
   → 落地 run / observe 两个动词与结构化日志。
3. **同构基础设施**：数据库 / 缓存 / 对象存储 / LLM 分别选什么、生产在哪？
   → 锁定本地 Docker Compose 同版本镜像（禁 latest、禁伪平替）、Migration 工具、
   受保护资源声明（protected_resources）。
4. **文档最小集与立项决策**：AGENTS.md + 产品/技术地图 + 规则；执行**立项决策**——
   全景架构图初版（Mermaid 文本）、初始 domain.md 集、奠基 ADR（0001 系列）。
5. **裁决面**：drive 沙箱（clone → act → observe → verdict → destroy）与
   机器可读 Case 格式落地；破坏性保护硬校验、无跳过参数。
6. **不预建**：探索面 Mock 机制与公共库——由第一个真实 Demo 需求 / 第二个项目拉动
   （拉动式建设，总原则第 2 条）。

## 验证用例（环境必须被证明是 work 的）

初始化不算完成，直到以下用例全绿并留痕：

- `harness run` 能起停全栈，健康检查通过；
- 一条贯穿 trace_id 的请求可被 `harness observe trace` 完整串出时间线；
- 从空库执行全量 Migration 成功；
- 一条最小 seed Case 经 `harness drive` 完成 clone → 裁决 → 销毁，
  产出 PASS 与判定四件套证据；
- 破坏性保护硬校验生效：配置指向 main 时拒绝启动，且不存在跳过保护的参数。

## 产出

可用的开发环境（脚手架 + 同构基础设施 + 操作面 + 裁决面）、文档最小集与立项决策
（全景图 / domain.md / 奠基 ADR）、全绿的环境验证用例证据。
