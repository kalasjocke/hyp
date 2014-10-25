from hyp.base import BaseAdapter, BaseResponder

class Adapter(BaseAdapter):
    def __init__(self, serializer_class):
        self.schema_class = serializer_class
        self.schema = self.schema_class()

    def __call__(self, instance):
        result = self.schema.dump(instance)
        return result.data


class Responder(BaseResponder):
    """Responder that uses a marshmallow :class:`Schema` for serialization."""
    ADAPTER = Adapter
