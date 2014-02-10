import pytest
import factory


class Model(object):
    def __getitem__(self, key):
        return getattr(self, key)


class Post(Model):
    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title
@pytest.fixture
def post_factory():
    class Factory(factory.Factory):
        FACTORY_FOR = Post

        id = factory.Sequence(lambda n: n)
        title = 'My post'

    return Factory
