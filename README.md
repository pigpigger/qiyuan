# qiyuan
s
https://arxiv.org/pdf/2304.06364
https://github.com/open-compass/opencompass/blob/main/opencompass/datasets/agieval/agieval.py

## AGIEval介绍

AGIEval 是一个面向 **高水平学术与专业考试** 的基准数据集，涵盖了法律、逻辑、医学、历史、伦理等多个领域。  
其中的 **JEC-QA（司法考试题）** 子集，尤其体现了模型在 **法律推理与伦理判断** 上的能力。  

在这一类评测中，标准答案来源于 **真实考试题库**，题目往往涉及：

- 对法律条文的理解与适用  
- 对社会伦理与公共政策的判断  
- 多选题下复杂推理的完整性  

因此，评测指标通常使用 **准确率（Accuracy）**：  
模型的预测选项与标准答案完全一致，才计为正确。  

这种严格标准的意义在于：  

1. **检验模型的专业可靠性** —— 能否在敏感领域（如法律、公共治理）给出符合事实与规范的解答。  
2. **衡量模型的社会责任感** —— 防止模型输出在伦理上存在偏差或风险。  
3. **促进可控性与安全性研究** —— 让模型不仅会“答题”，还必须答对、答稳，符合社会价值。  

相比于一般的常识问答，AGIEval 的准确率更能反映模型在 **安全、合规、伦理约束场景** 下的实际可用性。

## 评测实现

本项目提供了一个轻量化脚本，用于在 **AGIEval 数据集**（如 `jec-qa-kd.jsonl`）上测试多个大语言模型的表现。  
无需安装 [OpenCompass](https://github.com/open-compass/opencompass)，直接调用 API 进行推理并计算准确率。  

---

## 📂 项目结构

.
├── jec-qa-kd.jsonl # 数据集文件（AGIEval子集，JSONL格式）
├── eval.py # 主评测脚本
└── README.md # 项目说明


---

## 📦 环境依赖

- Python >= 3.8  
- 依赖库：
  ```bash
  pip install requests

⚙️ 配置

在 eval.py 中修改 API 配置：

API_BASE = ""  # 你的API服务地址
API_KEY = ""                                      # 你的API key

MODELS = ["gemini-2.5-pro", "gemini-1.5"]                   # 要测试的模型

📑 数据集格式

输入数据为 JSONL 格式，每行一个样本，例如：

```json
{"passage": null, "question": "中国商务部决定对原产于马来西亚等八国的橡胶制品展开反补贴调查。根据我国《反补贴条例》以及相关法律法规，下列关于此次反补贴调查的哪项判断是正确的?", "options": ["(A)我国商务部在确定进口橡胶制品是否存在补贴时必须证明出国(地区)政府直接向出口商提供了现金形式的财政资助", "(B)在反补贴调查期间，该八国政府或橡胶制品的出口经营者，可以向中国商务部作出承诺，取消、限制补贴或改变价格", "(C)如果我国商务部终局裁定决定对该八国进口橡胶制品征收反补贴税，该反补贴税的征收期限不得超过10年", "(D)如果中国橡胶制品进口商对商务部征收反补贴税的终局裁定不服，必须首先向商务部请求行政复审，对行政复审决定还不服，才能向中国有管辖权的法院起诉"], "label": ["B"]}
{"passage": null, "question": "唐朝御史台下设有。", "options": ["(A)台院", "(B)殿院", "(C)察院", "(D)郡院"], "label": ["A", "B", "C"]}
```



    question: 题目
    
    options: 选项列表，包含 (A) ... 格式
    
    label: 正确答案（支持多选，如 ["A","B","C"]）

🚀 运行

python eval.py

运行完成后，会在 res.txt 中保存结果。
📊 输出示例

结果文件 res.txt 示例：

```txt
=== Model: gemini-2.5-pro ===
1/200 | Question: ... | Pred: ['B'] | Label: ['B']
2/200 | Question: ... | Pred: ['A', 'C'] | Label: ['A', 'B', 'C']
...
Accuracy: 0.7520
```



## 测试结果

| 模型名称                                    | 准确率  |
|---------------------------------------------|---------|
| gemini-2.5-pro                              | 0.6200  |
| Qwen/Qwen3-235B-A22B-Instruct-2507-FP8      | 0.5800  |
| gpt-5                                       | 0.5600  |
| Qwen/Qwen2.5-VL-72B-Instruct                | 0.5600  |
| Kimi-K2-Instruct                            | 0.5200  |
| claude-sonnet-4-20250514                    | 0.4400  |
| gpt-4o                                      | 0.4200  |
| gemini-2.5-flash                            | 0.3800  |
| qwen-vl-plus                                | 0.3000  |
