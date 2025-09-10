import re

def cut(cleaned_content):
    return cleaned_content.replace("(", "").replace(")", "").strip()
