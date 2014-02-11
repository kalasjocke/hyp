import json

from inflection import pluralize

from hy.adapters.schematics import SchematicsSerializerAdapter


class Responder(object):
    def __init__(self):
        self.root = self.pluralized_type()
        self.serializer = SchematicsSerializerAdapter(self.SERIALIZER)

    def build_meta(self, document, meta):
        if meta is not None:
            document['meta'] = meta

    def build_resources(self, document, instances, links):
        resources = []

        for instance in instances:
            resource = self.serializer.to_primitive(instance)

            if links is not None:
                resource_links = {}

                for link in links:
                    # TODO Should be able to pick from where to get the related instances
                    related_instances = getattr(instance, link)
                    resource_links[link] = [ri.id for ri in related_instances]

                resource['links'] = resource_links

            resources.append(resource)

        document[self.root] = resources

    def build_root_links(self, document, links):
        if links is None:
            return

        root_links = {}

        for link in links:
            key = "%s.%s" % (self.pluralized_type(), link)
            value = {
                'type': self.LINKS[link]['responder'].pluralized_type(),
                'href': self.LINKS[link]['href'],
            }
            root_links[key] = value

        document['links'] = root_links

    def respond(self, instances, meta=None, links=None):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        document = {}

        self.build_meta(document, meta)
        self.build_resources(document, instances, links)
        self.build_root_links(document, links)

        return json.dumps(document)

    def pluralized_type(self):
        return pluralize(self.TYPE)
