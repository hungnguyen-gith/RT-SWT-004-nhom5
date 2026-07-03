def tokenize_simple_expression(text):
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        elif ch.isdigit():
            j = i
            while j < n and (text[j].isdigit() or text[j] == "."):
                j += 1
            tokens.append(("NUMBER", text[i:j]))
            i = j
        elif ch.isalpha():
            j = i
            while j < n and text[j].isalnum():
                j += 1
            tokens.append(("IDENT", text[i:j]))
            i = j
        elif ch in "+-*/()":
            tokens.append(("OP", ch))
            i += 1
        elif ch == "." and i + 1 < n and text[i + 1].isdigit():
            tokens.append(("NUMBER", "."))
            i += 1
        else:
            raise ValueError(f"Unexpected character: {ch}")
    return tokens