def rreplace(s, old, new, occurrence):
    if isinstance(s, list):
        result = []
        for item in s:
            result.append(rreplace(item, old, new, occurrence))
        return result
    if isinstance(s, dict):
        result = {}
        for key, value in s.items():
            result[key] = rreplace(value, old, new, occurrence)
        return result

    li = s.rsplit(old, occurrence)
    return new.join(li)
