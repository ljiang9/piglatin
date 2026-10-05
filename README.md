# piglatin 猪拉丁语翻译器

终端里的语言小玩具: 把英文转成猪拉丁语(Pig Latin)。

```bash
python -m piglatin "hello world"      # ellohay orldway
echo "String cheese" | python -m piglatin   # Ingstray eesechay
python -m piglatin --decode "ellohay"  # hello (尽力而为)
```

## 规则

| 情况 | 规则 | 例子 |
|---|---|---|
| 元音开头 | 原词 + `way` | apple → appleway |
| 辅音串开头 | 辅音串移到词尾 + `ay` | string → ingstray |
| 首字母大写 | 保持大写 | String → Ingstray |
| 尾部标点 | 原样保留 | hello! → ellohay! |

## 已知局限

- 只处理 ASCII 英文单词, 中文原样透传。
- `--decode` 是**尽力猜测**: 编码是信息丢失的(`orldway` 既可能是 world
  也可能是 orld)。实现列出所有合理解码候选(元音式 + 各种辅音串切分),
  优先选落在内置常见词表里的, 否则取第一个候选。常见英文 round-trip
  (hello/world/apple/string…) 可精确还原, 生僻词可能猜错。
- `y` 永远按辅音处理; `qu` 组合不做特殊处理。

## 许可

MIT, Copyright (c) 2026 ljiang9
