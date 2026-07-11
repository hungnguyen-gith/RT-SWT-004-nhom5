def normalize_path(path, base=None, strict=False, allow_empty=False):
    if path is None:
        if allow_empty:
            return ""
        raise ValueError("path is required")
    if base:
        if not path.startswith("/"):
            path = base.rstrip("/") + "/" + path
    parts = path.split("/")
    cleaned = []
    for part in parts:
        if part == "" or part == ".":
            continue
        if part == "..":
            if cleaned and strict:
                cleaned.pop()
            elif not strict:
                cleaned.append(part)
        else:
            cleaned.append(part)
    return "/" + "/".join(cleaned)