class Adapter(object):
    def __init__(self, serializer_class):
        self.serializer_class = serializer_class

    def to_primitive(self, instance):
        return self.serializer_class(instance).data
