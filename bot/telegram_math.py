"""Приведение ответов с формулами к виду, читаемому в Telegram (без LaTeX)."""

import re

_SUP = str.maketrans("0123456789+-=()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾")


def plain_math_for_telegram(text: str) -> str:
    """Убрать LaTeX-обёртки и заменить простые степени на Unicode, где это уместно."""
    t = text

    t = re.sub(r"\$\$", "\n", t)
    t = re.sub(r"\$([^$]*)\$", r"\1", t)

    t = re.sub(r"\\\(\s*", "", t)
    t = re.sub(r"\s*\\\)", "", t)
    t = re.sub(r"\\\[\s*", "\n", t)
    t = re.sub(r"\s*\\\]", "\n", t)

    t = re.sub(r"\^\{2\}", "²", t)
    t = re.sub(r"\^\{3\}", "³", t)
    t = re.sub(r"([a-zA-Z])\^\{2\}", r"\1²", t)
    t = re.sub(r"([a-zA-Z])\^\{3\}", r"\1³", t)

    t = re.sub(r"(\d+)\^\{(\d+)\}", _replace_braced_numeric_power, t)

    t = re.sub(r"(\d+)\^2(?!\d)", r"\1²", t)
    t = re.sub(r"(\d+)\^3(?!\d)", r"\1³", t)

    for _ in range(24):
        nt = re.sub(r"([a-zA-Z])\^2(?!\d)", r"\1²", t)
        if nt == t:
            break
        t = nt
    for _ in range(24):
        nt = re.sub(r"([a-zA-Z])\^3(?!\d)", r"\1³", t)
        if nt == t:
            break
        t = nt

    t = re.sub(r"\\sqrt\{([^}]+)\}", r"√(\1)", t)
    t = re.sub(r"\\cdot", "·", t)
    t = re.sub(r"\\times", "×", t)
    t = re.sub(r"\\pm", "±", t)

    t = re.sub(r"\n{3,}", "\n\n", t)
    return t.strip()


def _replace_braced_numeric_power(match: re.Match[str]) -> str:
    base, exp = match.group(1), match.group(2)
    if len(exp) == 1 and exp.isdigit():
        return base + exp.translate(_SUP)
    return f"{base}^{{{exp}}}"
