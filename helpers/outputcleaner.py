def strip_markdown_fences(code: str) -> str:
    code = code.strip()

    if code.startswith("```"):
        code = code.split("```")[1]

    if code.endswith("```"):
        code = code.rsplit("```", 1)[0]

    return code.strip()
