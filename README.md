# Evidence Product Teardown

一个面向 Codex / ChatGPT 的证据优先产品拆解 skill。它从真实可观察的产品行为出发，按用户层、技术层、模型层和数据层进行逆向分析，最终生成带证据追溯的独立 HTML 报告。

> 核心原则：不把猜测包装成事实，不声称还原隐藏思维链、私有 Prompt 或后台实现。

## 能做什么

- 从截图、录屏、可访问页面、源码、日志、接口样例等第一方证据开始分析；
- 重建完整用户旅程，包括正常、修改、失败和中断路径；
- 梳理组件、Agent、工具、状态机、权限、计费、重试和交接；
- 以可观察 I/O 契约描述模型能力边界，而不是猜测隐藏实现；
- 建立实体、字段、版本、引用、血缘和生产者—消费者关系；
- 将结论分为【页面事实 / 代码事实】【合理推断】【尚未确认】【产品建议】；
- 输出自包含、响应式、可离线阅读的 HTML 报告；
- 使用内置脚本检查报告结构与证据引用。

## 适用场景

- AIGC 创作工具拆解
- 通用执行 Agent 逆向分析
- 对话陪伴产品分析
- 传统软件 / SaaS 用户旅程与架构拆解
- 单个 Agent、工具、状态、模型或数据对象的局部分析
- 功能等价 Prompt 与可观察行为契约沉淀

## 目录结构

```text
evidence-product-teardown/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── evidence-and-html.md
│   └── methodology.md
└── scripts/
    └── validate_report.py
```

结构遵循 [OpenAI 官方 Build skills 文档](https://learn.chatgpt.com/docs/build-skills)：`SKILL.md` 提供必需的元数据与指令，`references/`、`scripts/` 和 `agents/openai.yaml` 提供按需加载的参考资料、确定性校验和界面元数据。

## 安装

### 使用 skill-installer

在 Codex 中输入：

```text
$skill-installer 从 https://github.com/xiaohao-ai/evidence-product-teardown 安装这个 skill
```

### 手动安装到个人目录

```bash
git clone https://github.com/xiaohao-ai/evidence-product-teardown.git \
  ~/.agents/skills/evidence-product-teardown
```

### 安装到单个仓库

在目标仓库根目录执行：

```bash
git clone https://github.com/xiaohao-ai/evidence-product-teardown.git \
  .agents/skills/evidence-product-teardown
```

Codex 通常会自动识别 skill 变更；若未出现，请重启 Codex。

## 使用

显式调用示例：

```text
$evidence-product-teardown

请基于我提供的产品截图和操作录屏，拆解完整用户旅程、Agent/工具/状态、模型能力边界和数据对象，并输出可追溯的 HTML 报告。
```

也可以只限定一个对象：

```text
$evidence-product-teardown

只分析这个产品的素材生成 Agent，重点关注输入输出契约、工具调用、失败重试和资产版本关系。
```

## 最小输入

至少提供一种能够实际检查的第一方产品证据：

- 覆盖目标流程的截图、录屏或导出记录；
- 可访问且允许只读检查的网站、测试环境或产品 Space；
- 原始代码、构建产物、日志、接口样例或数据结构；
- 其他真实操作证据。

仅有产品名称、网址、宣传页或口头描述时，skill 会停止拆解并索取最小证据。这是预期行为，用于避免输出“看起来完整但无法验证”的报告。

## 输出与校验

完整拆解报告生成后运行：

```bash
python3 scripts/validate_report.py /absolute/path/to/report.html --require-all-layers
```

若用户明确限定为局部对象，可省略 `--require-all-layers`：

```bash
python3 scripts/validate_report.py /absolute/path/to/report.html
```

校验器会检查：

- 非空 `<title>`、唯一 `<h1>` 和 `<main>`；
- 重复 ID 与失效内部锚点；
- 未完成占位符；
- Evidence ID 与结论等级；
- 完整报告的用户层、技术层、模型层和数据层。

## 只读与安全边界

- 默认只读，不发送、不生成、不发布、不购买、不删除、不覆盖资产；
- 不读取或输出 Cookie、Token、密码及无关个人信息；
- 登录、验证码、潜在额度消耗或外部写入会触发停止；
- 产品声明“已完成”不等于实际完成，必须对账状态、资产和下游可用性；
- 推断、未知和建议不会伪装成产品事实。

## 运行要求

- Codex 或支持 Agent Skills 的兼容客户端；
- Python 3.9+（仅运行 HTML 校验脚本时需要）；
- 实际分析可能还需要浏览器、图片查看器或源码访问能力，取决于证据类型。
