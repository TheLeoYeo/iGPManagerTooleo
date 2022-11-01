from igp.service.modifier.modifier import BaseModifier, Field


class SetupModifier(BaseModifier):
    def __init__(self, *fields: list[Field]):
        super().__init__(*fields)