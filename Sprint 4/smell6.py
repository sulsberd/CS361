def process(row):
    if len(row) < 8:
        return False
    if not row[7] == "'image'":
        return False
    if not row[8] == "'gif'":
        return False
    return True