#!/usr/bin/env python3
"""piglatin - 终端猪拉丁语翻译器.

规则:
- 以元音开头: 原词 + "way"           (apple -> appleway)
- 以辅音串开头: 辅音串移到词尾 + "ay" (string -> ingstray)
- 保留首字母大写和尾部标点          (String -> Ingstray, hello! -> ellohay!)

这是一个语言玩具: 正向翻译是确定性的, 反向解码(--decode)是尽力而为,
因为辅音串边界在编码后是歧义的。
"""
import argparse
import re
import sys

VOWELS = set("aeiouAEIOU")

_WORD_RE = re.compile(r"([A-Za-z]+)([^A-Za-z]*)$")


def encode_word(word):
    """编码单个英文单词, 保留大小写和尾部标点."""
    m = _WORD_RE.match(word)
    if not m:
        return word
    core, tail = m.group(1), m.group(2)
    capitalized = core[0].isupper()
    lower = core.lower()
    if lower[0] in VOWELS:
        enc = lower + "way"
    else:
        i = 0
        while i < len(lower) and lower[i] not in VOWELS:
            i += 1
        enc = lower[i:] + lower[:i] + "ay" if i < len(lower) else lower + "ay"
    if capitalized:
        enc = enc[0].upper() + enc[1:]
    return enc + tail


# 常见词小词表: 只用于 --decode 出现歧义时的择优, 不影响正向编码。
COMMON_WORDS = set("""
i a an the and or of to in on is are was were be been have has had do does did
will would can could shall should may might must hello world apple string
this that these those with from they them their there here what when where
which who how why not no yes you we me my your our cat dog man men woman
women day time people way make like into over under more most very just
""".split())


def _trailing_cluster_len(s):
    i = len(s)
    while i > 0 and s[i - 1] not in VOWELS:
        i -= 1
    return len(s) - i


def decode_word(word):
    """尽力反向解码单个单词.

    编码是信息丢失的: "orldway" 既可能是 world 也可能是 orld。
    策略: 列出所有合理解码候选(元音式 + 各种辅音串切分), 优先选落在
    常见词表里的, 否则取第一个候选。歧义已在 README/--help 如实说明。
    """
    m = _WORD_RE.match(word)
    if not m:
        return word
    core, tail = m.group(1), m.group(2)
    capitalized = core[0].isupper()
    lower = core.lower()
    cands = []
    if lower.endswith("way") and len(lower) > 3:
        cands.append(lower[:-3])  # 元音开头式: X + way
    if lower.endswith("ay") and len(lower) > 2:
        stem = lower[:-2]
        run = _trailing_cluster_len(stem)
        for k in range(1, run + 1):  # 辅音串搬回式: 尝试各种切分
            cands.append(stem[-k:] + stem[:-k])
    dec = next((c for c in cands if c in COMMON_WORDS), cands[0] if cands else lower)
    if capitalized:
        dec = dec[0].upper() + dec[1:]
    return dec + tail


def translate(text, decode=False):
    fn = decode_word if decode else encode_word
    return " ".join(fn(tok) for tok in text.split(" "))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="piglatin",
        description="猪拉丁语翻译器: hello world -> ellohay orldway",
    )
    ap.add_argument("text", nargs="*", help="要翻译的文本(省略则从 stdin 读)")
    ap.add_argument("--decode", action="store_true", help="反向解码(尽力而为)")
    args = ap.parse_args(argv)
    if args.text:
        src = " ".join(args.text)
    elif not sys.stdin.isatty():
        src = sys.stdin.read()
    else:
        ap.print_help()
        return 0
    out = translate(src, decode=args.decode)
    sys.stdout.write(out + ("\n" if out and not out.endswith("\n") else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
