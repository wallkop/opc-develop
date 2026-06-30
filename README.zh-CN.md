# opc-develop

[English](README.md)

opc-develop 是一套面向受控 AI 辅助开发的 Codex / Claude Code skill 套件。它把小需求快速迭代的 Lite 流程、完整产品开发的 Full 流程，以及 Harness 初始化/评估能力组合在同一个插件里。

![OPC-Develop skills workflow](assets/opc-develop-skills.png)

## 特点

- 根据用户输入语言自适应输出，而不是固定使用某一种默认语言。
- 在 PRD 和技术方案之前先做真实前端 prototype demo。
- 明确维护 demo parity、前端 mock inventory 和 prototype mock retirement。
- 下游产物和实现前必须经过独立 review gate。
- Harness 优先：文档、测试用例、runtime evidence、本地 E2E、发布验证形成闭环。
- 技术设计阶段必须明确 SaaS / 基础设施决策；数据存储选择必须遵循目标项目既有或已明确批准的架构基线，高影响且未决的选型必须阻塞给人类 review。

## 适合人群

opc-develop 适合 Builder，尤其适合 OPC 创业者、超级个体和独立产品构建者。它默认你本人要对项目的产品判断、设计审美和工程品味负责：你需要判断需求结构是否成立、交互是否顺手、架构是否会长歪。

**它不适合纯研发执行角色，也不适合主要难点在重团队协调、组织博弈、路线对齐或跨团队依赖管理的研发工作。** 这套 workflow 会在实现前故意加重产品和架构审查。如果你期待 AI 代替你的产品 taste、设计判断或工程 owner 意识，这套 skill 会显得过于苛刻。

## 核心思想

opc-develop 是原型驱动开发。人类负责上下文、品味、产品结构和架构方向；当方向足够清晰后，把繁重执行交给 AI。

推荐使用方式：

0. **先做 Harness 初始化。** 用 `harness-init` 和 `harness-eval` 让目标项目对 AI 足够透明：项目规则、文档规范、本地启动手册、runtime evidence、日志、数据库访问、trace、API mock、storage mock、测试门禁、发布流程和验收规则都要尽量补齐。
1. **把原始想法交给 AI，然后持续被它拷打。** 从 `product-brainstorm` 开始，不断回答追问，直到沉淀出清晰的 `requirement.md`，包括领域语言、目标、非目标、方案取舍、约束和验收信号。
2. **在已有真实项目上设计 UI demo。** 用 `create-demo` 或 `build-demo` 直接在真实前端代码里做高保真 prototype，后端行为先用纯前端 mock。然后持续 vibe-coding 和 review，直到交互符合你的产品品味。
3. **设计并审核 PRD 和技术方案。** 用 `build-prd`、`build-technical` 或 `loop-design` 推进产物，然后认真 review。这个阶段用于防止产品结构走歪、工程架构长歪。**如果你不具备产品结构化思维和架构深度，请在这里退出；opc-develop 暂时不适合你。**
4. **把开发、测试和发布大胆交给 AI。** 设计确认后，用 `loop-develop`、`local-e2e-verify` 和 `release-verify` 让 AI 处理实现、Unit/API 测试、黑盒测试、本地 E2E、发布检查和回滚准备。黑盒浏览器验证强烈推荐使用 Codex Computer Use。人类重点负责最后验收和产品质量判断。

## 内容

- `.agents/plugins/marketplace.json` - Codex repo marketplace manifest。
- `.codex-plugin/plugin.json` - Codex 插件 manifest。
- `.claude-plugin/plugin.json` - Claude Code 插件 manifest。
- `skills/` - 原子 skill 和编排 skill。
- `agents/` - Claude Code 自定义 subagents，用于 OPC review 和 implementation 角色。
- `shared/references/` - 共享契约、格式和流程规则。
- `shared/prompts/` - reviewer 和 implementer subagent prompt。
- `shared/scripts/` - 小型产物校验脚本。
- `docs/` - 平台使用说明。
- `SECURITY.md` 和 `CONTRIBUTING.md` - 公开分发与贡献策略。

## 主要流程

- `lite-develop` - 在当前分支处理小型或中低风险开发。
- `product-brainstorm` - 早期需求澄清、领域语言、方案取舍、目标/非目标和验收信号沉淀。
- `loop-design` - demo、PRD、technical design 的设计闭环。
- `loop-develop` - spec、testcases、plan、TDD implementation 和 local verification 的开发闭环。
- `harness-init` - 引导式 Harness 初始化规划。
- `harness-eval` - 可复用的 Harness 成熟度评分。
- `release-verify` - 发布门禁、发布后验证和回滚就绪检查。

## 安装

### Codex

把这个仓库作为 Codex plugin marketplace 使用：

```bash
codex plugin marketplace add wallkop/opc-develop --ref main
codex plugin add opc-develop@opc-develop
```

本地开发时，把这个仓库作为版本源，克隆到你的 Codex personal plugin source 目录，并在 Codex 中启用 `opc-develop` personal plugin。

```bash
git clone https://github.com/wallkop/opc-develop.git ~/plugins/opc-develop
```

如果你的 Codex 使用其他 personal plugin source 目录，请克隆到对应目录。保持这个仓库作为 source of truth，让 Codex 从它安装或缓存。

### Claude Code

同一个仓库也可以作为 Claude Code plugin source：

```bash
claude --plugin-dir ~/plugins/opc-develop
```

Claude Code 中使用 plugin namespace 调用 skill，例如 `/opc-develop:product-brainstorm` 或 `/opc-develop:harness-eval`。

更多说明见 [docs/claude-code.md](docs/claude-code.md)。

## 更新

Peers 可以从 Git tag 或默认分支更新：

```bash
cd ~/plugins/opc-develop
git pull --ff-only
```

更新后，如你的 Codex 或 Claude Code 版本需要，请重启或重新加载插件。

## 发布与发现

GitHub 是历史、tag、diff、issue 和 release notes 的 canonical source。SkillHub、Claude marketplace、Codex marketplace 等目录站更适合做 discovery surface，并链接回这个仓库。

## 安全说明

这个仓库不应该包含项目业务产物、凭据、私有日志、`.env` 文件或生成后的 feature 文档。具体需求的输出应写入目标项目仓库，而不是写进这个插件。

## License

MIT
