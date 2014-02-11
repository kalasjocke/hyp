import json

from schematics.models import Model
from schematics.transforms import to_primitive


class Serializer(Model):
        return json.dumps({self.KEY: to_primitive(self, instance)})
    def to_json(self, instances):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        key = self.KEY
        value = [to_primitive(self, instance) for instance in instances]

        return json.dumps({key: value})
