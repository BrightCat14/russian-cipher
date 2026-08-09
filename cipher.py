#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Русский текст <-> «месиво» из юникод-символов.

Детерминированная обратимая подстановка: каждая русская буква и знак
пунктуации заменяется на уникальный символ. Пробелы, переносы строк и
символы вне таблицы (латиница, цифры и т.п.) остаются как есть.

Замечание: не используй в исходном тексте сами символы-шифры (например «§»
или «!») — они принадлежат алфавиту шифра и будут декодироваться как буквы.

Использование:
    python cipher.py encode "Привет, мир!"
    python cipher.py decode "≪⦅⦆⟨..."
    python cipher.py table          # показать таблицу замен
    python cipher.py check          # самопроверка round-trip
    python cipher.py                # интерактивный режим
"""

import sys

# Символы из примера автора сохранены: С->!, ъ->(, е->:, ш->?, ь->%, ж->*,
# щ->—, ё->{, т->>, и-><, х->&, г->^, я->;, э->". Остальное добито новыми.
LOWER = {
    "а": "§", "б": "©", "в": "¥", "г": "^", "д": "®", "е": ":", "ё": "{",
    "ж": "*", "з": "¶", "и": "<", "й": "±", "к": "¢", "л": "¦", "м": "¤",
    "н": "£", "о": "€", "п": "₽", "р": "Δ", "с": "Ω", "т": ">", "у": "≈",
    "ф": "Φ", "х": "&", "ц": "∇", "ч": "Ψ", "ш": "?", "щ": "—", "ъ": "(",
    "ы": "Ξ", "ь": "%", "э": '"', "ю": "∑", "я": ";",
}

UPPER = {
    "А": "≪", "Б": "≫", "В": "⦅", "Г": "⦆", "Д": "⟨", "Е": "⟩", "Ё": "⊆",
    "Ж": "⊇", "З": "⋀", "И": "⋁", "Й": "⋂", "К": "⋃", "Л": "⋄", "М": "⋅",
    "Н": "⋆", "О": "≅", "П": "≡", "Р": "⊕", "С": "!", "Т": "⊗", "У": "⊥",
    "Ф": "⊤", "Х": "⌒", "Ц": "⌣", "Ч": "∘", "Ш": "∴", "Щ": "∵", "Ъ": "∷",
    "Ы": "∓", "Ь": "‽", "Э": "‰", "Ю": "∂", "Я": "∉",
}

PUNCT = {
    ",": "~", ".": "#", "!": "$", "?": "'", ":": ")", ";": "+", "(": "=",
    ")": "@", '"': "[", "'": "]", "«": "}", "»": "\\", "—": "`", "–": "_",
    "…": "|", "-": "/", "+": ".", "=": ",", "%": "┐", "^": "└", "&": "┘",
    "*": "├", "№": "┤", "#": "╔", "$": "╗", "@": "╚", "`": "╝", "~": "┴",
}

ENCODE = {}
ENCODE.update(LOWER)
ENCODE.update(UPPER)
ENCODE.update(PUNCT)

DECODE = {code: plain for plain, code in ENCODE.items()}


def _check():
    assert " " not in ENCODE and "\n" not in ENCODE and "\t" not in ENCODE, \
        "пробельные символы не должны кодироваться"
    assert len(ENCODE) == len(DECODE), "конфликт: разные буквы -> один символ"
    assert len(set(ENCODE.values())) == len(ENCODE), "дубликаты кодов"


def encode(text: str) -> str:
    return "".join(ENCODE.get(ch, ch) for ch in text)


def decode(text: str) -> str:
    return "".join(DECODE.get(ch, ch) for ch in text)


def print_table() -> None:
    width = max(len(k) for k in ENCODE)
    for name, table in (("строчные", LOWER), ("заглавные", UPPER), ("пунктуация", PUNCT)):
        print(f"-- {name} --")
        for k in table:
            print(f"{k!r:<4} {k:^{width}} -> {table[k]!r}  ({table[k]})")


def check_all() -> None:
    _check()
    all_chars = "".join(ENCODE)
    assert decode(encode(all_chars)) == all_chars, "round-trip сломан"
    pangram = "Съешь же ещё этих мягких французских булок, да выпей чаю"
    assert decode(encode(pangram)) == pangram, "round-trip панграммы сломан"
    print("OK: таблица уникальна, round-trip сходится")
    print(encode(pangram))


def has_cyrillic(text: str) -> bool:
    return any("\u0400" <= ch <= "\u04FF" for ch in text)


def repl() -> None:
    print("Режим: введи русский текст -> зашифрую, введи шифр -> расшифрую. Пустая строка — выход.")
    while True:
        try:
            line = input("> ").rstrip("\n")
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        print(encode(line) if has_cyrillic(line) else decode(line))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        repl()
        return
    cmd, rest = args[0], args[1:]
    if cmd in ("encode", "-e"):
        print(encode(" ".join(rest)))
    elif cmd in ("decode", "-d"):
        print(decode(" ".join(rest)))
    elif cmd in ("table", "-t"):
        print_table()
    elif cmd in ("check", "--check", "-c"):
        check_all()
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    _check()
    main()
