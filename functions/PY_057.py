def parse_csv_line(line, delimiter=",", quote_char='"', trim_whitespace=False, skip_empty=False):
    fields = []
    current = ""
    in_quotes = False
    i = 0
    while i < len(line):
        ch = line[i]
        if in_quotes:
            if ch == quote_char:
                if i + 1 < len(line) and line[i + 1] == quote_char:
                    current += quote_char
                    i += 1
                else:
                    in_quotes = False
            else:
                current += ch
        else:
            if ch == quote_char:
                in_quotes = True
            elif ch == delimiter:
                if trim_whitespace:
                    current = current.strip()
                if not (skip_empty and current == ""):
                    fields.append(current)
                current = ""
            else:
                current += ch
        i += 1
    if trim_whitespace:
        current = current.strip()
    if not (skip_empty and current == ""):
        fields.append(current)
    return fields