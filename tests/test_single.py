import json

from fixtures import PostSerializer


def test_single(post):
    data = PostSerializer().to_json(post)

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}
