def write_to_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
