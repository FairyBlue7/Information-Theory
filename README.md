# McEliece 公钥密码系统 - 信息论课程项目

## 项目简介

本项目实现了基于编码理论的 McEliece 公钥密码系统，对比了两种不同纠错码的实现方案：
- **方案一**：基于 Hamming(15, 11) 码的 McEliece 密码系统
- **方案二**：基于 BCH(15, 7) 码的 McEliece 密码系统

## 运行说明

### 依赖项

本项目需要以下 Python 库：
- `numpy` - 数值计算
- `galois` - 有限域运算

安装依赖：
```bash
pip install -r requirements.txt
```

### 运行环境

- Python 版本：Python 3.8+
- 操作系统：Windows / Linux / macOS

### 如何复现实验

#### 1. 运行 Hamming 码 McEliece 演示
```bash
python run_hamming_demo.py
```

#### 2. 运行 BCH 码 McEliece 演示
```bash
python run_bch_demo.py
```

#### 3. 运行性能基准测试（对比两种方案）
```bash
python run_benchmark.py
```

### 示例命令及输出

```bash
# 运行 Hamming 码演示
$ python run_hamming_demo.py

============================================================
Hamming-based McEliece Cryptosystem Demo
============================================================

Parameters:
  Number of blocks (L): 5
  Hamming code: (15, 11)
  Message length: 55 bits
  Ciphertext length: 75 bits

[1] Generating keys...
  Public key size: (55, 75)
  Error correction capability: 5 errors (1 per block)
  Key generation complete!

[2] Original message (55 bits):
  [1 0 1 1 0 ...]... (showing first 20 bits)

[3] Encrypting message...
  Ciphertext (75 bits):
  [0 1 1 0 1 ...]... (showing first 20 bits)
  Encryption complete!

[4] Decrypting ciphertext...
  Decrypted message (55 bits):
  [1 0 1 1 0 ...]... (showing first 20 bits)

[5] Verification:
  ✓ SUCCESS: Decrypted message matches original!
```

## 关键参数说明

### Hamming(15, 11) 变体

| 参数 | 值 | 说明 |
|------|-----|------|
| n | 15 | 码字长度 |
| k | 11 | 信息位长度 |
| t | 1 | 每块纠错能力 |
| L | 可配置 | 块数（默认 5, 10, 20） |
| 消息扩展率 | 15/11 ≈ 1.36 | 密文/明文比率 |

### BCH(15, 7) 变体

| 参数 | 值 | 说明 |
|------|-----|------|
| n | 15 | 码字长度 |
| k | 7 | 信息位长度 |
| t | 2 | 每块纠错能力 |
| L | 可配置 | 块数（默认 5, 10, 20） |
| 消息扩展率 | 15/7 ≈ 2.14 | 密文/明文比率 |

## 随机种子固定方法（保障可复现性）

若需要固定随机种子以保证实验可复现性，请在运行脚本前添加以下代码：

```python
import numpy as np
np.random.seed(42)  # 可替换为任意固定值
```

或在命令行中设置环境变量：
```bash
PYTHONHASHSEED=42 python run_benchmark.py
```

## 项目结构

```
Information-Theory/
├── README.md                     # 项目说明文件
├── requirements.txt              # 依赖列表
├── run_hamming_demo.py           # Hamming 码演示脚本
├── run_bch_demo.py               # BCH 码演示脚本
├── run_benchmark.py              # 性能对比测试脚本
├── code/
│   ├── __init__.py
│   ├── utils.py                  # 公用工具函数
│   ├── hamming_mceliece/         # Hamming 码实现
│   │   ├── __init__.py
│   │   ├── keygen.py             # 密钥生成
│   │   ├── encrypt.py            # 加密
│   │   ├── decrypt.py            # 解密
│   │   └── hamming_code.py       # Hamming 码核心
│   └── bch_mceliece/             # BCH 码实现
│       ├── __init__.py
│       ├── keygen.py             # 密钥生成
│       ├── encrypt.py            # 加密
│       ├── decrypt.py            # 解密
│       └── bch_code.py           # BCH 码核心
└── McEliece_PKE_Comparison_Paper.md  # 论文草稿
```

## 性能基准测试参数

基准测试使用以下参数配置：

| 参数 | 值 |
|------|-----|
| L 值范围 | [5, 10, 20] |
| 测试轮数 | 3（取平均值） |
| 测量指标 | 密钥生成时间、加密时间、解密时间、消息扩展率、公钥大小 |

---

**作业题目**：McEliece 公钥密码系统比较研究  
**课程名称**：信息论与编码理论  
**提交日期**：2025-12-18