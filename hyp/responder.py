import json

from hyp.adapters.base import adapter_for


class Responder(object):
    TYPE = None
    SERIALIZER = None
    LINKS = None

    def __init__(self):
        self.adapter = adapter_for(self.SERIALIZER)(self.SERIALIZER)

    def build_root_meta(self, meta):
        return meta

    def build_root_links(self, links):
        rv = {}

        for link in links:
            properties = self.LINKS[link]
            key = "%s.%s" % (self.TYPE, link)
            value = {
                'type': properties['responder'].TYPE,
            }
            if 'href' in properties:
                value['href'] = properties['href']

            rv[key] = value

        return rv

    def build_root_linked(self, linked):
        rv = {}

        for key, instances in linked.iteritems():
            responder = self.LINKS[key]['responder']()
            rv[responder.TYPE] = [responder.build_resource(instance) for instance in instances]

        return rv

    def build_resources(self, instance_or_instances, links=None):
        builder = lambda instance: self.build_resource(instance, links)

        if isinstance(instance_or_instances, list):
            return map(builder, instance_or_instances)
        else:
            return builder(instance_or_instances)

    def build_resource(self, instance, links=None):
        resource = self.adapter(instance)
        if links is not None:
            resource['links'] = self.build_resource_links(instance, links)
        return resource

    def build_resource_links(self, instance, links):
        resource_links = {}

        for link in links:
            properties = self.LINKS[link]
            key = properties.get('key', link)
            instance_or_instances = self.pick(instance, key)
            builder = lambda instance: self.pick(instance, 'id')
            if isinstance(instance_or_instances, list):
                resource_links[link] = map(builder, instance_or_instances)
            else:
                resource_links[link] = builder(instance_or_instances)

        return resource_links

    def links(self, links, linked):
        if linked is not None:
            links = linked.keys()

        return links

    @classmethod
    def build(cls, *args, **kwargs):
        return cls()._respond(*args, **kwargs)

    @classmethod
    def respond(cls, *args, **kwargs):
        return json.dumps(cls()._respond(*args, **kwargs))

    def _respond(self, instance_or_instances, meta=None, links=None, linked=None):
        links = self.links(links, linked)

        document = {}

        if meta is not None:
            document['meta'] = self.build_root_meta(meta)

        if links is not None:
            document['links'] = self.build_root_links(links)

        if linked is not None:
            document['linked'] = self.build_root_linked(linked)

        document[self.TYPE] = self.build_resources(
            instance_or_instances, links)

        return document

    def pick(self, instance, key):
        try:
            return getattr(instance, key)
        except AttributeError:
            return instance[key]
