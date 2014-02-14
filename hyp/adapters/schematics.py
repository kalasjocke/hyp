from __future__ import absolute_import

from hyp.adapters.base import SerializerAdapter


class SchematicsSerializerAdapter(SerializerAdapter):
    def __init__(self, serializer_class):
        self.model_class = serializer_class

    def to_primitive(self, instance):
        return self.instance_to_model(instance).to_primitive()

    def instance_to_model(self, instance):
        model = self.model_class()

        for key, field in self.model_class.fields.iteritems():
            setattr(model, key, self._pick(instance, key))

        return model

    def _pick(self, instance, key):
        if hasattr(instance, key):
            return getattr(instance, key)
        else:
            return instance[key]
