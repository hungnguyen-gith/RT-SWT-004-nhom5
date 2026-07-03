def build_query_string(params, sort_keys=True, exclude_none=True, encode_spaces=True):
    items = list(params.items())
    if sort_keys:
        items.sort(key=lambda kv: kv[0])
    parts = []
    for key, value in items:
        if value is None:
            if exclude_none:
                continue
            value = ""
        if isinstance(value, bool):
            value = "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            for v in value:
                encoded_v = str(v).replace(" ", "+") if encode_spaces else str(v)
                parts.append(f"{key}={encoded_v}")
            continue
        encoded_value = str(value).replace(" ", "+") if encode_spaces else str(value)
        parts.append(f"{key}={encoded_value}")
    return "&".join(parts)