from schematics.models import Model
from schematics.types import IntType

from hyp.adapters.schematics import SchematicsSerializerAdapter


class Post(object):
    def __init__(self):
        self.id = 1


class Simple(Model):
    id = IntType()


def test_object_conversion():
    adapter = SchematicsSerializerAdapter(Simple)
    assert adapter.to_primitive(Post())['id'] == 1


def test_dict_conversion():
    adapter = SchematicsSerializerAdapter(Simple)
    assert adapter.to_primitive({'id': 1})['id'] == 1
