class FunctionDefinition(object):

    def __init__(self, name: str, description: str):
        pass

    @property
    def name() -> str:
        return ""

    @property
    def description() -> str:
        return ""

    @property
    def options():
        return []
    
    def find_option(name: str):
        return None
    
    @property
    def details():
        return []
    
    @property
    def kernels():
        return []
    
    @property
    def properties():
        return 
    
class FunctionBuilder(object):

    def __init__(self, name: str): 
        self.name = name
        self.description: str = None

    def set_description(self, description: str):
        self.description = description

    def try_set_description(self, description: str):
        if self.description is None:
            self.description = description

    def finish(self) -> FunctionDefinition:
        if self.description is None:
            self.description = "Description is missing and would go here"
        return FunctionDefinition(self.name, self.description)