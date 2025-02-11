def cleanup_text(text: str) -> str:
    if not text:
        return text

    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        if "[指示]" in line:
            continue
        if "修正案:" in line:
            continue
        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines).strip()
    return cleaned_text
