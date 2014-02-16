from schematics.models import Model
from schematics.types import IntType, StringType
from marshmallow import Serializer, fields

from hyp.responder import Responder


class CommentSerializer(Serializer):
    id = fields.Integer()
    content = fields.String()


class PersonSerializer(Model):
    id = IntType()
    name = StringType()


class PostSerializer(Model):
    id = IntType()
    title = StringType()


class CommentResponder(Responder):
    TYPE = 'comment'
    SERIALIZER = CommentSerializer


class PersonResponder(Responder):
    TYPE = 'person'
    SERIALIZER = PersonSerializer


class PostResponder(Responder):
    TYPE = 'post'
    SERIALIZER = PostSerializer
    LINKS = {
        'comments': {
            'responder': CommentResponder(),
            'href': 'http://example.com/comments/{posts.comments}',
        },
        'author': {
            'responder': PersonResponder(),
            'href': 'http://example.com/people/{posts.author}',
        },
    }
