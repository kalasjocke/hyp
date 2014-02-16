from __future__ import absolute_import

from hyp.adapters.base import SerializerAdapter


class MarshmallowSerializerAdapter(SerializerAdapter):
    def __init__(self, serializer_class):
        self.serializer_class = serializer_class

    def to_primitive(self, instance):
        return self.serializer_class(instance).data
