# Review Trigger Policy

目标是在保持隔离评审价值的前提下，减少无效全量 review。

## Artifact Review

- 首次产出 `demo`、`prd.md`、`technical.md`、`spec.md`、`testcases.md`、`plan/*.md` 后，必须运行对应 `review-*` skill。
- review 必须由 fresh dedicated review subagent 执行，不能 inline 自审。
- 如果 review 返回 `Issues Found`，creator 只修复 blocking issues 及其必要相邻影响。
- creator 修复后必须重新 review，但默认执行 targeted fresh review：只审上轮 blocking issues、被修改区域、以及直接受影响的上游/下游契约。
- 不允许每次小修都重新全量审整个 artifact，除非修改范围已经改变 artifact 的主要语义或 reviewer 明确判定 targeted review 不足。

## Implementation Review

- `tdd-coding` 中，每个 plan 首次完成后必须做一次 fresh `spec compliance review`。
- `code quality review` 不再默认每轮执行，只在命中风险触发条件时执行。
- 后续返修默认只做 targeted implementation review，聚焦上轮 blocking issue、实际 diff、测试证据和受影响契约。

## Code Quality Risk Triggers

命中任一条件时必须执行 code quality review：

- 新增或修改 public API contract。
- 权限、安全、审计、敏感信息、凭据、脱敏、数据泄露风险。
- SaaS / 基础设施组件：datastore/database、cache、queue、object/blob storage、外部 API、模型 provider、鉴权服务等。
- 数据一致性、事务、补偿、幂等、并发、race condition、迁移、回滚。
- agent/tool/harness/runtime evidence/local-e2e 相关能力。
- 跨模块或跨服务改动。
- 大范围重构、删除、迁移或 project rule 影响。
- spec compliance reviewer 明确要求进一步 code quality review。

未命中风险触发条件的小修，例如文案、等待条件、测试稳定性、局部样式微调，使用 targeted spec compliance review 即可。

## Stop-Loss

- 同一 blocking issue 连续 2 轮返修后仍不收敛，停止循环。
- 将 issue、已尝试修复、证据、冲突 artifact 写入 `progress.md`。
- 路由回最早受影响层级：technical、spec、plan，或请求人类裁决。
- advisory notes 不得触发返修循环。

## Evidence

- reviewer 输出不能直接当事实；controller 必须检查 diff、测试输出和报告路径后才能声明通过。
- 所有 Approved 结论只对当前 artifact/code revision 有效。
