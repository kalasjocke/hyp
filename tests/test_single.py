import json

from fixtures import PostSerializer


def test_single(post):
    data = PostSerializer().to_json(post)

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}


def test_multiple(post_factory):
    post = post_factory(id=1, title='A title')
    another_post = post_factory(id=2, title='Another title')

    data = PostSerializer().to_json([post, another_post])

    assert json.loads(data) == {
        'posts': [
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ]
    }


def test_meta(post):
    data = PostSerializer().to_json(post, meta={'key': 'value'})

    assert json.loads(data)['meta']['key'] == 'value'
