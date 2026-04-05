---
name: customer-analysis-pack
description: Turn a customer investigation or company-intelligence brief into a banker-ready analysis pack in Chinese. Use when the user wants customer analysis, an internal banking memo, a follow-on pack after investigation, or a structured bridge from lead discovery into financial-services deliverables.
---

# 客户分析包

把前序客户调查结果转成一版银行内部分析包。默认中文输出，强调“从信息收集走到客户分析”。

## 适用场景

- 已经有客户调查稿，需要形成分析材料
- 需要把 `lead-discovery` 的结果转成内部分析包
- 客户经理需要一版内部讨论稿
- 授信前、覆盖前、首次拜访前的分析整理

## 推荐输入

优先接收以下任一输入：

- `customer-investigation` 产出的 Markdown 调查稿
- `client-initial-screening` / `key-account-briefing` 的结果
- 用户直接提供的企业信息、财务假设、风险点

如果没有完整输入，也可以先基于现有事实生成 first-pass 分析包，但必须在输出里标注哪些地方仍需核验。

## 工作流程

### Step 1: 吸收前序调查结果

从输入中提取至少这些字段：

- 企业身份
- 主营业务 / 产品
- 银行切入点
- 风险清单
- 财务事实或财务假设
- 下一步动作

### Step 2: 形成分析框架

默认应整理成这几部分：

1. 客户概况
2. 财务快照
3. 银行产品匹配
4. 风险判断
5. 行业与竞争观察
6. 行动建议

### Step 3: 调用下游技能

优先顺序：

1. `datapack-builder`
   - 生成 workbook 和基础 markdown
2. 按需补充：
   - `competitive-analysis`
   - `comps-analysis`
   - `dcf-model`（仅当用户明确需要估值）

### Step 4: 升级最终 Markdown

不要只交基础 datapack 摘要，要把它升级成 banker-readable 内部分析稿。

## 默认输出

### 1. Markdown 分析包

最低结构：

```markdown
# [企业名称]客户分析包

## 一、客户概况
## 二、财务快照
## 三、银行产品匹配矩阵
## 四、风险判断
## 五、行业与竞争观察
## 六、客户经理下一步动作
```

### 2. Excel 工作簿

至少应包含：

- 执行摘要
- 历史财务
- 经营指标
- 市场与银行切入
- 关键风险
- 银行行动建议

## 质量要求

- 默认中文
- 明确写出哪些数字来自已验证披露，哪些只是 first-pass 假设
- 至少给出一张“银行产品匹配矩阵”表
- 至少给出一张“下一步行动”表
- 如用户要求正式对外版本，必须提示需要进一步核验财报和公开披露

## 推荐表格

### 银行产品匹配矩阵

| 产品 | 匹配度 | 理由 | 触发条件 |
|------|--------|------|----------|
| 现金管理 | 高/中/低 | | |
| 供应链金融 | 高/中/低 | | |
| 项目融资 | 高/中/低 | | |
| 授信 | 高/中/低 | | |
| 投行服务 | 高/中/低 | | |

### 下一步行动表

| 动作 | 负责人 | 优先级 | 说明 |
|------|--------|--------|------|
| 获取审计财报 | RM | 高 | |

## 与两个插件的默认协同

推荐默认链路：

1. `aigroup-lead-discovery-openclaw/customer-investigation`
2. `aigroup-financial-services-openclaw/customer-analysis-pack`
3. 如需进一步建模，再进入 `datapack-builder` / `dcf-model`

这条链路的目标不是直接做交易材料，而是先形成客户经理可内部使用的客户调查 + 客户分析闭环。
