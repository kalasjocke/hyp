import json

from fixtures import PostResponder


class TestBuild(object):
    def test_single(self):
        data = PostResponder.build({'id': 1, 'title': 'My title'})

        assert data == {'posts': {'id': 1, 'title': 'My title'}}

    def test_multiple(self):
        data = PostResponder.build([
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ])

        assert data == {
            'posts': [
                {'id': 1, 'title': 'A title'},
                {'id': 2, 'title': 'Another title'},
            ]
        }


class TestRespond(object):
    def test_single(self):
        data = PostResponder.respond(
            {'id': 1, 'title': 'A title'}
        )

        assert json.loads(data) == {
            'posts': {'id': 1, 'title': 'A title'}
        }


def test_meta():
    data = PostResponder.build(
        {'id': 1, 'title': 'Yeah'},
        meta={'key': 'value'},
    )

    assert data['meta']['key'] == 'value'
