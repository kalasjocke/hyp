from schematics.models import Model
from schematics.types import IntType, StringType
from marshmallow import Schema, fields

from hyp.marshmallow import Responder as MarshmallowResponder
from hyp.schematics import Responder as SchematicsResponder


class CommentSerializer(Schema):
    id = fields.Integer()
    content = fields.String()


class PersonSerializer(Model):
    id = IntType()
    name = StringType()


class PostSerializer(Model):
    id = IntType()
    title = StringType()


class PersonResponder(SchematicsResponder):
    TYPE = 'people'
    SERIALIZER = PersonSerializer


class CommentResponder(MarshmallowResponder):
    TYPE = 'comments'
    SERIALIZER = CommentSerializer

    LINKS = {
        'author': {
            'responder': PersonResponder,
            'href': 'http://example.com/people/{comments.author}',
        },
    }


class PostResponder(SchematicsResponder):
    TYPE = 'posts'
    SERIALIZER = PostSerializer
    LINKS = {
        'comments': {
            'responder': CommentResponder,
            'href': 'http://example.com/comments/{posts.comments}',
        },
        'author': {
            'responder': PersonResponder,
            'href': 'http://example.com/people/{posts.author}',
        },
    }
