import json

from schematics.models import Model
from schematics.transforms import to_primitive


class Serializer(Model):
    def to_json(self, instance):
        return json.dumps({self.KEY: to_primitive(self, instance)})
