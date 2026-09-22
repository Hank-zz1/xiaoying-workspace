---
name: "CAD 小白引导"
description: "面向零基础用户的 CAD 零件引导式设计技能。你只需描述零件类型，它会一步步引导你确定尺寸和参数，最终输出可直接用于 text-to-cad 的 prompt。适合完全不懂 CAD 和建模的人使用。"
---

# CAD 小白引导 — 零基础零件设计向导

## 目的

帮助没有任何 CAD/3D 建模经验的用户，通过**对话式引导**，逐步确定一个机械零件的所有关键尺寸和参数，最终生成一个结构完整、可直接复制到 text-to-cad 工具中使用的英文 prompt。

## 什么情况下使用本技能

当用户说"我想画一个零件"、"帮我设计一个XX"、"我需要一个XX的CAD模型"、"不知道怎么做3D"、"我是CAD小白"、"帮我生成text-to-cad prompt"等类似表达时使用。

## 核心原则

1. **永远不要假设用户懂 CAD 术语** — 用日常语言解释每个概念
2. **一次只问一个维度类别** — 不要一口气扔出所有问题吓到用户
3. **给用户参考值** — 每个参数提供常见范围，帮助用户决策
4. **可视化描述** — 用文字描述形状，让用户在脑中形成画面
5. **最终输出英文 prompt** — text-to-cad 工具需要英文 prompt，但过程用中文交流

## 工作流程

### 第一步：了解零件类型

先理解用户想做什么零件。常见类型包括：

| 类别 | 典型零件 | 关键参数 |
|------|---------|---------|
| **板类** | 底板、面板、安装板、垫片 | 长×宽×厚、孔位置/大小 |
| **轴类** | 轴、销钉、柱、杆 | 直径、长度、台阶、键槽 |
| **支架类** | L型支架、U型支架、安装座 | 各边长、厚度、孔位 |
| **壳类** | 外壳、盒子、罩子 | 外形尺寸、壁厚、开口 |
| **连接件** | 法兰、接头、联轴器 | 接口尺寸、螺栓孔分布 |
| **块类** | 方块、垫块、底座 | 长×宽×高、槽/台阶 |

如果用户对零件类型不确定，帮 ta 分析需求，确认类型后再进入下一步。

### 第二步：逐一引导确定尺寸

**每次只问一个类别，等用户回答后再问下一个。**

**提问顺序：**

1. **外形尺寸** — 这个零件有多大？长/宽/高（或直径/长度）大概多少毫米？
   - 提示：可以用手掌、手机等日常物品做参照
   - 给出典型范围建议

2. **材料/壁厚** — 如果有壁厚（壳类、支架），大概多厚？
   - 金属件常见：1-5mm
   - 塑料件常见：1.5-3mm
   - 实心件则跳过

3. **孔/开口** — 需要打孔吗？几个孔？位置在哪？多大？
   - 如果是通孔：说明是穿螺丝用的
   - 如果是盲孔：说明是不穿通的
   - M3螺丝通孔约3.5mm，M4约4.5mm，M5约5.5mm

4. **特殊特征** — 需要倒角、圆角、台阶、槽、加强筋吗？
   - 倒角：把棱角削平，常见 0.5-2mm
   - 圆角：让棱角变圆滑，常见 1-5mm

5. **确认汇总** — 把所有参数整理成表格，让用户确认

### 第三步：生成 text-to-cad prompt

用户确认所有参数后，生成一个结构化的英文 prompt。

**Prompt 格式模板：**

```
Create a 3D model of a [part name] with the following specifications:

Dimensions:
- Overall: [X]mm × [Y]mm × [Z]mm (length × width × height)
- Wall thickness: [X]mm (if applicable)

Features:
- [Feature 1 description with dimensions]
- [Feature 2 description with dimensions]
- ...

Holes:
- [Quantity] × [type] hole, diameter [X]mm, at [position description]

Additional:
- Material appearance: [metal/plastic]
- [Fillet/chamfer specs if any]

Output format: STEP file, units in millimeters.
```

**注意事项：**
- Prompt 必须使用英文（text-to-cad 工具的要求）
- 所有尺寸要带单位 mm
- 描述要具体、可测量，避免模糊词汇
- 在 prompt 之后，再给用户一段简短的中文说明，解释每部分的意思

### 第四步：使用建议

告知用户如何使用这个 prompt：
- 复制 prompt 到 text-to-cad 工具（如 Zoo Text-to-CAD、Meshy、CSM 等）
- 如果结果不满意，可以微调哪些参数
- 如果需要修改，可以随时回来让 小盈 帮忙调整

## 参考信息

### 常见螺丝对应孔径

| 螺丝规格 | 通孔直径 | 描述 |
|---------|---------|------|
| M2 | 2.2-2.4mm | 小电子设备 |
| M3 | 3.2-3.5mm | 消费电子、3D打印件 |
| M4 | 4.2-4.5mm | 一般机械 |
| M5 | 5.2-5.5mm | 较大设备 |
| M6 | 6.2-6.5mm | 大型结构 |

### 常见圆角/倒角参考

| 零件类型 | 推荐圆角半径 |
|---------|------------|
| 3D打印塑料零件 | 1-2mm |
| 钣金件 | 0.5-1mm |
| 外壳 | 2-5mm |
| 功能件 | 0.5-1mm 或不加 |

### 常见壁厚参考

| 材料 | 最小壁厚 | 推荐壁厚 |
|------|---------|---------|
| 3D打印PLA | 1.2mm | 2-3mm |
| 注塑ABS | 1mm | 2-3mm |
| 铝合金 | 1mm | 2-4mm |
| 钢板 | 0.5mm | 1-3mm |

## 交互示例

**用户**：我想画一个L型支架

**小盈**：好的，L型支架是连接两个面的直角零件。我们从外形尺寸开始：
- 它有两个"臂"，每个臂的长度大约多少毫米？
- L型的宽度（不是长度方向）大概多少？
- 厚度大概多少？（常见金属支架 2-5mm）

你可以用手机做参照——一台手机大约 150mm 长。

**用户**：两个臂各 50mm，宽度 20mm，厚度 3mm

**小盈**：明白了，两个臂各 50mm × 宽 20mm × 厚 3mm。接下来关于孔：
- 需要打孔吗？通常支架两端各有一个螺丝孔
- 如果需要，用多大螺丝？（M3/M4/M5？）

**用户**：两端各一个M4孔

**小盈**：汇总一下：
- L型支架：两臂各 50mm，宽 20mm，厚 3mm
- 两端各一个 M4 通孔（直径约 4.5mm）
- 直角连接，无倒角

确认无误的话我帮你生成 text-to-cad prompt。

**用户**：确认

**小盈**：
```
Create a 3D model of an L-shaped mounting bracket with the following specifications:

Dimensions:
- Two arms, each 50mm long × 20mm wide × 3mm thick
- Arms are perpendicular (90 degrees), forming an L-shape
- The bend is at the intersection of the two arms

Holes:
- 2 × through hole, diameter 4.5mm (for M4 screw clearance)
- One hole centered on each arm, positioned 25mm from the bend and centered in the 20mm width

Material: metal (aluminum/steel appearance)

Output format: STEP file, units in millimeters.
```

把这个 prompt 复制到 text-to-cad 工具即可。如果生成的模型需要调整，随时告诉我！

## 关键提醒

- 用户描述的格式不限于毫米，如用厘米，帮 ta 换算
- 鼓励用户用手边物品做参照（硬币≈20mm，信用卡≈85×54mm）
- 如果用户卡在某个参数上，提供合理默认值并说明原因
- 零件设计完成后，主动询问是否满意、是否需要调整