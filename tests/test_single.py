import json

from fixtures import PostResponder


def test_single_object(post):
    data = PostResponder().respond(post)

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}


def test_single_dict(post):
    data = PostResponder().respond({'id': 1, 'title': 'My title'})

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}


def test_multiple(post_factory):
    post = post_factory(id=1, title='A title')
    another_post = post_factory(id=2, title='Another title')

    data = PostResponder().respond([post, another_post])

    assert json.loads(data) == {
        'posts': [
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ]
    }


def test_meta(post):
    data = PostResponder().respond(post, meta={'key': 'value'})

    assert json.loads(data)['meta']['key'] == 'value'
