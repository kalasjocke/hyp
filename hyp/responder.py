import json

from inflection import pluralize

from hyp.adapters.base import adapter_for


class Responder(object):
    def __init__(self):
        # TODO Add a way to override the pluralized type
        self.root = self.pluralized_type()
        self.adapter = adapter_for(self.SERIALIZER)(self.SERIALIZER)

    def build_meta(self, meta):
        return meta

    def build_links(self, links):
        rv = {}

        for link in links:
            properties = self.LINKS[link]
            key = "%s.%s" % (self.pluralized_type(), link)
            value = {
                'type': properties['responder'].pluralized_type(),
            }
            if 'href' in properties:
                value['href'] = properties['href']

            rv[key] = value

        return rv

    def build_linked(self, linked):
        rv = {}

        for key, instances in linked.iteritems():
            responder = self.LINKS[key]['responder']
            rv[key] = responder.build_resources(instances)

        return rv

    def build_resources(self, instances, links=None):
        return [self.build_resource(instance, links) for instance in instances]

    def build_resource(self, instance, links):
        resource = self.adapter(instance)
        if links is not None:
            resource['links'] = self.build_resource_links(instance, links)
        return resource

    def build_resource_links(self, instance, links):
        resource_links = {}

        for link in links:
            # TODO Should be able to pick from where to get the related instances
            related = self.pick(instance, link)
            if isinstance(related, list):
                resource_links[link] = [self.pick(r, 'id') for r in related]
            else:
                resource_links[link] = self.pick(related, 'id')
        return resource_links

    @classmethod
    def build(cls, *args, **kwargs):

        return cls().get(*args, **kwargs)

    @classmethod
    def dumps(cls, *args, **kwargs):

        return cls().respond(*args, **kwargs)

    def respond(self, *args, **kwargs):
        document = self.get(*args, **kwargs)

        return json.dumps(document)

    def get(self, instances, meta=None, links=None, linked=None):
        if not isinstance(instances, list):
            instances = [instances]

        if linked is not None:
            links = linked.keys()

        document = {}

        if meta is not None:
            document['meta'] = self.build_meta(meta)
        if links is not None:
            document['links'] = self.build_links(links)
        if linked is not None:
            document['linked'] = self.build_linked(linked)
        document[self.root] = self.build_resources(instances, links)

        return document

    def pluralized_type(self):
        return pluralize(self.TYPE)

    def pick(self, instance, key):
        try:
            return getattr(instance, key)
        except AttributeError:
            return instance[key]
