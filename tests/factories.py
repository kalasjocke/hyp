import pytest
import factory


class Post(object):
    def __init__(self, id=None, title=None):
        self.id = id
        self.title = title


class Comment(object):
    def __init__(self, id=None, content=None):
        self.id = id
        self.content = content


class Person(object):
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name


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


@pytest.fixture
def person_factory():
    class Factory(factory.Factory):
        FACTORY_FOR = Person

        id = 1
        name = 'Joe'

    return Factory


@pytest.fixture
def person(person_factory):
    return person_factory()
