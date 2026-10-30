# 教学网页 · 逻辑回归实验

这是与 39 页教学 PPT、32 页补充手册同源的前端教学页；另附 Markdown 手册。

## 打开方式

**直接打开（推荐，离线可用）**

双击 `index.html`，或用浏览器打开：

```text
file:///.../teaching-site/index.html
```

KaTeX、字体、图片、数据全部在本地，不依赖 CDN。`file://` 下已实际渲染验证：13 个公式、2 张图、交互均正常。

**本地服务器（可选）**

```powershell
cd deliverables\teaching-site
python -m http.server 8765
# 打开 http://127.0.0.1:8765/
```

## 页面内容

| 区块 | 内容 | 交互 |
|---|---|---|
| Hero | 两条主线、课程索引、材料规格 | 锚点导航 |
| 00 地图 | 模型线 / 工程线、六个关键数字 | 侧边栏阅读定位 |
| 01 数据 | 47 → 44 列账本、划分、缺失、五步管线 | MinMax 公式 |
| 02 DataLoader | Dataset / DataLoader 代码、独立 generator | **batch 计算器** |
| 03 模型 | logit / sigmoid / BCE / L1-L2、代码、形状 | KaTeX 公式 |
| 04 训练 | 配置、五步循环、模板问题 | — |
| 05 评估 | 指标表、结果图、曲线 | **阈值滑块 + 混淆矩阵** |
| 06 Agent | 经典 Agent、ReAct、Prompt / Context / Harness、AGENTS.md | **Prompt 生成器 + 复制** |
| 07 验收 | 10 分细则、提交命名 | **10 项验收清单 + 进度** |
| 08 练习 | 5 道选择题、3 个课堂练习 | **即时判分 + 解释** |
| 09 参考 | Markdown / 公式源 / PPT PDF / 手册 PDF | 下载 |

## 文件结构

```text
teaching-site/
├── index.html                 # 单页教学站
├── styles.css                 # 极简编辑风样式（响应式 / 打印）
├── app.js                     # 阈值、batch、prompt、清单、quiz、导航
├── data.js                    # 1000 条测试集概率（离线交互）
├── handbook.md                # Markdown 教学手册
├── formulas.tex               # 公式源
├── assets/
│   ├── results.png / curves.png
│   ├── sigmoid.png / scores.png
│   └── favicon.svg
├── downloads/
│   ├── teaching-slides.pdf    # 39 页 PPT
│   └── handbook-print.pdf     # 32 页补充手册
└── vendor/katex/              # KaTeX 0.19.1（本地）
```

## 设计与交互原则

- **风格**：`#F7F5EF` 米白 + `#171717` 墨黑 + `#0F6B62` 墨绿；无阴影、无外链字体，编辑式大标题 + 细线分隔。
- **阅读**：桌面左侧 sticky 目录 + 顶部阅读进度；≤980px 切换为移动端顶栏与横向章节条。
- **公式**：KaTeX 本地渲染；`$$...$$` / `\(...\)` / `\[...\]` 均可。
- **无后端**：所有交互在浏览器内完成；清单用 `localStorage` 保存，刷新不丢。
- **可访问性**：skip link、语义化 section、`aria-live`、键盘可操作的 range / checkbox / radio、`prefers-reduced-motion`。
- **打印**：隐藏侧栏和交互控件，保留正文、公式、表格与图片。

## 内容口径

与 PPT / 补充手册一致：

- 47 列 → 44 维；8000 / 1000 / 1000；训练集正样本 50.06%；缺失 5595。
- 44 = 40 原始数值 + 4 编码列；batch 125 / 16 / 16（末批 40）；参数 45。
- 验证 / 测试 Accuracy 0.6550 / 0.6350；测试 ROC-AUC 0.6897。
- 官方 10 分细则：环境与数据 3 + 模型 4 + 训练与评估 3。
- 阈值滑块的 1000 条概率来自 `logreg_lab/outputs/test_predictions.csv`；阈值 0.50 时复核为 TP 307 / FP 182 / FN 183 / TN 328。

## 验证记录

- Chromium（Edge headless）1440px / 390px 双端渲染，`scrollWidth == innerWidth`，无横向溢出。
- 13 个 KaTeX 公式渲染；2 张结果图加载成功。
- 阈值 0.50：0.6350 / 0.6278 / 0.6265 / 0.6272；矩阵 307 / 182 / 183 / 328。
- 阈值 0.70：Precision 上升、Recall 下降，交互符合预期。
- batch 计算：1000/64 → 16 批 / 末批 40；8000/64 → 125 批 / 末批 64。
- 5 题 quiz 全对 → 5/5；10 项清单 → 10/10，进度 100%。
- `file://` 直接打开：公式、图片、交互正常，无 console error。

## 注意

- 页面里的 PPT/PDF 是教学材料的副本；如更新源文件，重新复制到 `downloads/` 即可。
- Markdown 手册中的 `> [!NOTE]` 等提示块在 GitHub/GitLab 上显示为 alert；普通 Markdown 查看器会显示为引用块。
- 外部链接（Anthropic、arXiv、OpenAI、DeepSeek）需要联网；其余内容离线可用。
- 打包分发：`../teaching-site.zip`（解压后双击 `index.html`）。
