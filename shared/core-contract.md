# OPC 核心契约（Fable 5 版）

所有 opc-develop skill 都加载本契约。**开发流程与 Harness 解耦、互相配合**：
流程只负责"何时做什么、产出什么决策"；"怎么判定对不对"一律交给目标项目的 Harness
（run / observe / drive / deploy、Oracle / Verdict、判定四件套）。流程自身不携带裁决脚本。
Harness 的权威定义见 `${CLAUDE_PLUGIN_ROOT}/docs/harness.zh-CN.md`（本仓库关键参考文档）。

## 路由：一条判据

**这个改动需不需要动产品定义（definition.md：PD 产品底线 + TD 技术决策 + AC 验收标准）？**

- 需要新建或修改产品定义 → 标准链：`brainstorm → demo（可选）→ design → build`。
- 不动产品定义、但需要自动验收 → `lite`：无前置文档，TDD 式实现 + harness 裁决。
- 人类亲自验收、只要最快代码 → `vibe`：不做任何自动验收。
- 项目 harness 能力缺失或不足 → `harness-init`（新项目）/ `harness-retrofit`（存量项目）。
- 复杂度看起来超出 lite 时，只做一次提醒确认，不强制拦截——用户确认后仍可走 lite。
- 永远不按预计工时或笼统风险标签路由、拦截、拆分工作。

## 五条底线（继承自 Harness 总原则）

1. **反馈回路判据**：任何流程环节必须能回答"它缩短了哪条反馈回路"，答不上来就删。
2. **裁决链上不许有假**：判定正确性必须真实环境、真实数据，证据必须属于本次执行；
   假（Mock）只允许出现在探索链（Demo），且必须是声明过的假。
3. **裁判与运动员分离**：Oracle 在实现前锁死（commit）；改 Oracle = 作废全部绿灯、
   说明理由、重走 RED。
4. **结构即提示**：长期约束优先固化进脚手架与门禁，而不是写在流程文本里要求"遵守"。
5. **语言约定**：一切约束性文本（skill、规则、产品定义、报告）一律中文；仅解析用 token、
   命令、路径、代码标识保留原文。

## 判定与宣称

- Verdict 只有三值：PASS / FAIL / INCONCLUSIVE；INCONCLUSIVE 不得被解释为 PASS。
- 绿灯不跨环境迁移：本地 drive 全绿 ≠ 测试/生产可用；发布必经 Core-Case 冒烟投影。
- 未经 harness 裁决，不得宣称 passed / fixed / done / releasable；vibe 例外——它明说未验证。
- 警惕假绿灯：页面无报错、接口 200、日志无 Error、状态 completed，都不能单独证明产品正确。

## 反馈分类

人类反馈三分，且只取其一：`tune`（同一意图的执行调整，当场迭代）、
`revise`（上游事实错了——回最早出错层修复，作废下游结论后重放）、`park`（干净停止）。

## 安全底线（fail-closed）

破坏性操作、生产变更、权限/安全变更、不可逆 schema/数据操作、force-push、对外发布，
始终需要人类显式批准。其余缺口 fail-open：记录 gap、继续，并在收尾如实报告止步层级。
