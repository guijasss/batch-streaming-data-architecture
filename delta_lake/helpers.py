from re import sub

def camel_to_snake(camel_str: str) -> str:
    return sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()
