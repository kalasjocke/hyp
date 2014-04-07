class Adapter(object):
    def __init__(self, serializer_class):
        self.serializer_class = serializer_class

    def __call__(self, instance):
        return self.serializer_class(instance).data
