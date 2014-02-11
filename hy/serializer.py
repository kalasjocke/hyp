import json

from inflection import pluralize
from schematics.models import Model
from schematics.transforms import to_primitive


class Serializer(Model):
    def to_json(self, instances):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        key = pluralize(self.TYPE)
        value = [to_primitive(self, instance) for instance in instances]

        return json.dumps({key: value})
