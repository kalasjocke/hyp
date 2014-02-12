from __future__ import absolute_import

from hy.adapters.base import SerializerAdapter


class SchematicsSerializerAdapter(SerializerAdapter):
    def __init__(self, serializer_class):
        self.model_class = serializer_class

    def to_primitive(self, instance):
        return self.instance_to_model(instance).to_primitive()

    def instance_to_model(self, instance):
        model = self.model_class()

        for name, field in self.model_class.fields.iteritems():
            setattr(model, name, self._pick_value(instance, name))

        return model

    def _pick_value(self, instance, name):
        attribute = getattr(instance, name, None)
        if attribute is None:
            attribute = instance[name]

        return attribute
