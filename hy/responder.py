import json

from inflection import pluralize

from hy.adapters.schematics import SchematicsSerializerAdapter


class Responder(object):
    def __init__(self):
        self.serializer = SchematicsSerializerAdapter(self.SERIALIZER)

    def build_meta(self, document, meta):
        if meta is not None:
            document['meta'] = meta

    def build_resource(self, document, instances):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        key = pluralize(self.TYPE)
        value = [self.serializer.to_primitive(instance) for instance in instances]

        document[key] = value

    def respond(self, instances, meta=None):
        document = {}

        self.build_meta(document, meta)
        self.build_resource(document, instances)

        return json.dumps(document)
