import json

from fixtures import PostResponder


def test_single_object():
    data = PostResponder().respond({'id': 1, 'title': 'My title'})

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}


def test_multiple():
    data = PostResponder().respond([
        {'id': 1, 'title': 'A title'},
        {'id': 2, 'title': 'Another title'},
    ])

    assert json.loads(data) == {
        'posts': [
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ]
    }


def test_meta():
    data = PostResponder().respond(
        {'id': 1, 'title': 'Yeah'},
        meta={'key': 'value'},
    )

    assert json.loads(data)['meta']['key'] == 'value'
