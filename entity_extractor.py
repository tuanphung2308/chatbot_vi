from rasa.nlu.components import Component


class EntityExtractor(Component):
    name = "entity_extractor"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["vi"]

    def __init__(self, component_config=None):
        super(EntityExtractor, self).__init__(component_config)

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "test",
                  "extractor": "entity_extractor"}

        return entity

    def process(self, message, **kwargs):
        key, confidence = 'investment', 0.9
        entity = self.convert_to_rasa(key, confidence)
        message.set("entities", [entity], add_to_output=True)
