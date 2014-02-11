import json

from inflection import pluralize
from schematics.models import Model
from schematics.transforms import to_primitive


class Serializer(Model):
    def build_resource(self, document, instances):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        key = pluralize(self.TYPE)
        value = [to_primitive(self, instance) for instance in instances]

        document[key] = value

    def to_json(self, instances):
        document = {}

        self.build_resource(document, instances)

        return json.dumps(document)
