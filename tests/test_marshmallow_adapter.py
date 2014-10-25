import pytest
from marshmallow import Schema, fields

from hyp.marshmallow import Adapter as MarshmallowAdapter


class Post(object):
    def __init__(self):
        self.id = 1


class Simple(Schema):
    id = fields.Integer(default=None)


@pytest.fixture
def marshmallow_adapter():
    return MarshmallowAdapter(Simple)


def test_object_conversion(marshmallow_adapter):
    assert marshmallow_adapter(Post())['id'] == 1


def test_dict_conversion(marshmallow_adapter):
    assert marshmallow_adapter({'id': 1})['id'] == 1


def test_object_none_attribute(marshmallow_adapter):
    post = Post()
    post.id = None

    assert marshmallow_adapter({'id': None})['id'] is None
    assert marshmallow_adapter(post)['id'] is None
