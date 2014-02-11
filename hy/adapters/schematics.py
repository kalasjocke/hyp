from __future__ import absolute_import

from schematics.transforms import to_primitive

from hy.adapters.base import SerializerAdapter


class SchematicsSerializerAdapter(SerializerAdapter):
    def __init__(self, serializer_class):
        self.serializer_class = serializer_class

    def to_primitive(self, instance):
        return to_primitive(self.serializer_class, instance)
