---
name: build
description: "definition.md 定案后的自主开发环节：AC 展开为机器可读 Case 并锁死 Oracle，先跑 RED 再实现（TDD，模型自主规划路线），harness drive 全量裁决转 GREEN，仅一次现实评审，最终以 Core-Case 冒烟投影在真实环境收口。裁决全部由项目 Harness 执行，本 skill 不携带任何裁决脚本。"
license: MIT
---

# build

契约是产品定义，裁判是 Harness，路线归模型。产出是证据，不是文档。

## 前置

加载 `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`。`definition.md` 已定案；
项目 harness 的 run / observe / drive 可用——缺口先走 `harness-retrofit`，
不在 build 里临时凑合裁决方式。

## 协议

1. **展开**：AC → `cases/*.yaml`（must / must_not / 超时 / 必需证据 / budget），
   标注 Core-Case，commit 锁死 Oracle（裁判与运动员分离）。
2. **RED**：`harness drive` 全量执行——必须全 FAIL 才算基线成立。出现 INCONCLUSIVE
   说明 harness 有缺口（驱动不到入口、取不到证据），先修 harness 再开工；
   严禁临场发明新 Oracle。
3. **实现**：模型自主规划路线——切片顺序、是否并行、内循环节奏都不是契约。
   走生产装配；白盒测试按 TD 风险随代码写，与代码同放，不进长期文档。
   编码期间用最便宜的定向检查内循环，浏览器全量裁决留给 drive。
4. **现实评审（仅此一次）**：Core-Case 首次转绿时做一次冷上下文评审，只查一类问题——
   可逆但铺开就贵的结构性别扭（坏抽象即将被复制八遍）。结论回写 rules / ADR，
   不保留评审文档。
5. **GREEN**：铺开剩余 AC；每次 drive 全量跑——棘轮由 harness 保证：已绿的不许变红。
   全 PASS + 判定四件套留痕即完成。改 Oracle = 作废全部绿灯、说明理由、回到第 2 步。
6. **真实冒烟（必经）**：部署到真实环境后执行 Core-Case 冒烟投影——同一条 Case、
   must 子集裁决、非破坏、数据可识别，Playwright + 必要时 Computer Use。
   绿灯不跨环境迁移，本地全绿不能代替这一步；真实外部 Provider 的一次真实调用
   也落在这里，严禁把它当调试循环。

## 重入

FAIL 的 Case 就是重入点：修复 → 重跑受影响 Case + 全量棘轮。人类验收拒绝时按
tune / revise 分类：实现缺陷回第 3 步；产品定义本身错了回 `design`，作废下游结论。

## 产出

绿的 run 证据（本地全量 + 真实冒烟）+ definition.md 状态更新。
无 feature-plan、无 acceptance 文档、无 ledger——过程状态由 Git 与 run 记录承载。
