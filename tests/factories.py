import pytest
import factory


class Model(object):
    def __getitem__(self, key):
        return getattr(self, key)


class Post(Model):
    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title


class Comment(Model):
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content


@pytest.fixture
def post_factory():
    class Factory(factory.Factory):
        FACTORY_FOR = Post

        id = 1
        title = 'My title'

    return Factory


@pytest.fixture
def post(post_factory):
    return post_factory()


@pytest.fixture
def comment_factory():
    class Factory(factory.Factory):
        FACTORY_FOR = Comment

        id = 1
        content = 'My content'

    return Factory


@pytest.fixture
def comment(post_factory):
    return comment_factory()
