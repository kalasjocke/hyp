import pytest
from schematics.models import Model
from schematics.types import IntType

from hyp.adapters.schematics import Adapter as SchematicsAdapter


class Post(object):
    def __init__(self):
        self.id = 1


class Simple(Model):
    id = IntType()


@pytest.fixture
def adapter():
    return SchematicsAdapter(Simple)


def test_object_conversion(adapter):
    assert adapter.to_primitive(Post())['id'] == 1


def test_dict_conversion(adapter):
    adapter = SchematicsAdapter(Simple)
    assert adapter.to_primitive({'id': 1})['id'] == 1


def test_object_none_attribute(adapter):
    post = Post()
    post.id = None

    assert adapter.to_primitive({'id': None})['id'] is None
    assert adapter.to_primitive(post)['id'] is None
