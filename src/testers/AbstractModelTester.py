from abc import ABC, abstractmethod


class AbstractModelTester(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self) -> any:
        pass

    @staticmethod
    def _extract_function_body(model_response: str) -> str:
        return model_response[model_response.index("def"): len(model_response):]

    @staticmethod
    def _extract_function_name(function_body: str) -> str:
        # function_name = regex.findall("\s*(def)\s(.*?)\([a-zA-z]*\)", extracted_function)
        return function_body[function_body.index("def ") + len("def "): function_body.index("(")]