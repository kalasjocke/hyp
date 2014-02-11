import json

from inflection import pluralize

from hy.adapters.schematics import SchematicsSerializerAdapter


class Responder(object):
    def __init__(self):
        self.root = self.pluralized_type()
        self.serializer = SchematicsSerializerAdapter(self.SERIALIZER)

    def build_meta(self, meta):
        if meta is None:
            return

        return meta

    def build_resources(self, instances, links=None):
        rv = []

        for instance in instances:
            resource = self.serializer.to_primitive(instance)

            if links is not None:
                resource_links = {}

                for link in links:
                    # TODO Should be able to pick from where to get the related instances
                    related = getattr(instance, link)
                    if hasattr(related, "__iter__"):
                        resource_links[link] = [r.id for r in related]
                    else:
                        resource_links[link] = related.id

                resource['links'] = resource_links

            rv.append(resource)

        return rv

    def build_links(self, links):
        if links is None:
            return

        rv = {}

        for link in links:
            key = "%s.%s" % (self.pluralized_type(), link)
            value = {
                'type': self.LINKS[link]['responder'].pluralized_type(),
                'href': self.LINKS[link]['href'],
            }
            rv[key] = value

        return rv

        rv = {}

    def respond(self, instances, meta=None, links=None):
        if not hasattr(instances, "__iter__"):
            instances = [instances]

        document = {}

        document['meta'] = self.build_meta(meta)
        document['links'] = self.build_links(links)
        document[self.root] = self.build_resources(instances, links)

        [document.pop(key) for key in document.keys() if document[key] is None]

        return json.dumps(document)

    def pluralized_type(self):
        return pluralize(self.TYPE)
