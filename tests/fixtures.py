from schematics.types import IntType, StringType

from hy.serializer import Serializer


class PostSerializer(Serializer):
    KEY = 'posts'

    id = IntType()
    title = StringType()
