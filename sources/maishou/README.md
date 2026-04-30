# 买手 (maishou) — 全网比价技能

商品价格全网对比，获取中国在线购物平台商品价格、优惠券。

## 支持平台

| 编号 | 平台 |
|------|------|
| 0 | 全部 |
| 1 | 淘宝/天猫 |
| 2 | 京东 |
| 3 | 拼多多 |
| 4 | 苏宁 |
| 5 | 唯品会 |
| 6 | 考拉 |
| 7 | 抖音 |
| 8 | 快手 |
| 10 | 1688 |

## 使用方式

```bash
# 搜索商品
uv run scripts/main.py search --source=0 --keyword='iPhone 16'

# 商品详情及购买链接
uv run scripts/main.py detail --source=2 --id={goodsId}
```

## 依赖

- Python ≥ 3.11
- aiohttp, argparse, PyYAML

> 来源: https://skills.sh/aahl/skills/maishou
