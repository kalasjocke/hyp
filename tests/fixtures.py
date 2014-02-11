from schematics.types import IntType, StringType

from hy.serializer import Serializer


class PostSerializer(Serializer):
    TYPE = 'post'

    id = IntType()
    title = StringType()
