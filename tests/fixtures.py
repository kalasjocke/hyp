from schematics.models import Model
from schematics.types import IntType, StringType

from hy.responder import Responder


class CommentSerializer(Model):
    id = IntType()
    content = StringType()


class PostSerializer(Model):
    id = IntType()
    title = StringType()


class CommentResponder(Responder):
    TYPE = 'comment'
    SERIALIZER = CommentSerializer


class PostResponder(Responder):
    TYPE = 'post'
    SERIALIZER = PostSerializer
    LINKS = {
        'comments': {
            'responder': CommentResponder(),
            'href': 'http://example.com/comments/{posts.comments}',
        }
    }
