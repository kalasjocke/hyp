"""Base classes for the ``Responders`` and ``Adapters``.
"""
import json

from six import iteritems


class BaseResponder(object):
    TYPE = None
    SERIALIZER = None
    LINKS = None
    ADAPTER = None

    def __init__(self):
        if not self.ADAPTER:
            raise NotImplementedError('Responder must define ADAPTER class variable')
        self.adapter = self.ADAPTER(self.SERIALIZER)

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

        document[self.TYPE] = self.build_resources(instance_or_instances, links)

        return document

    def links(self, links, linked):
        if linked is not None:
            links = linked.keys()

        return links

    def build_root_meta(self, meta):
        return meta

    def build_root_links(self, links):
        rv = {}

        for key in links:
            link = self.LINKS[key]
            association = "%s.%s" % (self.TYPE, key)

            rv[association] = {'type': link['responder'].TYPE}
            if 'href' in link:
                rv[association]['href'] = link['href']

        return rv

    def build_root_linked(self, linked):
        rv = {}

        for key, instances in iteritems(linked):
            link = self.LINKS[key]
            responder = link['responder']()

            if responder.TYPE not in rv:
                rv[responder.TYPE] = []

            [rv[responder.TYPE].append(responder.build_resource(instance))
                for instance in instances]

        return rv

    def build_resources(self, instance_or_instances, links=None):
        builder = lambda instance: self.build_resource(instance, links)
        return self.apply_to_object_or_list(builder, instance_or_instances)

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
            associated = self.pick(instance, key)

            if isinstance(associated, list):
                associated = [i for i in associated if i is not None]
                if len(associated) == 0:
                    continue
            else:
                if associated is None:
                    continue

            builder = lambda instance: self.pick(instance, 'id')
            resource_links[link] = self.apply_to_object_or_list(builder, associated)

        return resource_links

    def apply_to_object_or_list(self, func, object_or_list):
        if isinstance(object_or_list, list):
            return list(map(func, object_or_list))
        else:
            return func(object_or_list)

    def pick(self, instance, key):
        try:
            return getattr(instance, key)
        except AttributeError:
            return instance[key]


class BaseAdapter(object):
    """Base class from which all :class:`Adapter` classes inherit.
    """

    def __call__(self, instance):
        """Serialize ``instance`` to a dictionary of Python primitives."""
        raise NotImplementedError('Adapter class must define __call__')
