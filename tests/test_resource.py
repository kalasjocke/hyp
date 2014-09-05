import json

from fixtures import PostResponder


class TestBuild(object):
    def test_single(self):
        response = PostResponder.build({'id': 1, 'title': 'My title'})

        assert response == {'posts': {'id': 1, 'title': 'My title'}}

    def test_multiple(self):
        response = PostResponder.build([
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ])

        assert response == {
            'posts': [
                {'id': 1, 'title': 'A title'},
                {'id': 2, 'title': 'Another title'},
            ]
        }


class TestRespond(object):
    def test_single(self):
        response = PostResponder.respond(
            {'id': 1, 'title': 'A title'}
        )

        assert json.loads(response) == {
            'posts': {'id': 1, 'title': 'A title'}
        }


def test_meta():
    response = PostResponder.build(
        {'id': 1, 'title': 'Yeah'},
        meta={'key': 'value'},
    )

    assert response['meta']['key'] == 'value'
