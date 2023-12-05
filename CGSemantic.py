semantic_types = {
        "INT": lambda x: x.isdigit() or x == "",
        "FLOAT": lambda x: x.replace('.', '', 1).isdigit(),
        "STR": lambda x: x.isidentifier() or x == "",
        "CHAR": lambda x: x.isidentifier() or x == "",
        "BOOL": lambda x: x in ['True', 'False'] or x == "",
}
