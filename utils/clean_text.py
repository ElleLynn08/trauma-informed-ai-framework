import re

def strip_non_ascii_but_keep_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F900-\U0001F9FF]+"
    )
    emojis = emoji_pattern.findall(text)
    text_no_non_ascii = ''.join(ch if ord(ch) < 128 else ' ' for ch in text)
    for e in emojis:
        text_no_non_ascii += " " + e
    return text_no_non_ascii

