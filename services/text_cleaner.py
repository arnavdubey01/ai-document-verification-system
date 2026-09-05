import re

def clean_ocr_text(text):

    # Remove empty lines and extra spaces.
    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)