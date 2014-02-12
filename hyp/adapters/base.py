class SerializerAdapter(object):
    def to_primitive(self, instance):
        raise NotImplementedError()
