from typing import Dict

POINT_CODE_LANG = "code"
POINT_YAML_TYPE = "yaml"
POINT_PARAGRAPH_CLASS = "paragraph_class"

class Plugin:
    def __init__(self):
        pass

plugins_code_lang: Dict[str,Plugin]
plugins_yaml_type: Dict[str,Plugin]
plugins_paragraph_class: Dict[str,Plugin]

def register_code_lang(lang: str):
    pass




