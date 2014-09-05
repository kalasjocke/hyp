from hyp.responder import Responder

from fixtures import (
    PostResponder,
    PersonResponder,
    PostSerializer,
)


def test_single():
    author = {'id': 1, 'name': 'John'}
    comments = [
        {'id': 1, 'content': 'My comment'},
        {'id': 2, 'content': 'Another comment'},
    ]
    post = {'id': 1, 'title': 'My title', 'comments': comments, 'author': author}

    response = PostResponder.build(post, linked={
        'comments': comments, 'author': [author]
    })

    assert response == {
        'posts': {
            'id': 1,
            'title': 'My title',
            'links': {
                'author': 1,
                'comments': [1, 2],
            }
        },
        'links': {
            'posts.author': {
                'href': 'http://example.com/people/{posts.author}',
                'type': 'people',
            },
            'posts.comments': {
                'href': 'http://example.com/comments/{posts.comments}',
                'type': 'comments',
            }
        },
        'linked': {
            'comments': [
                {'id': 1, 'content': 'My comment'},
                {'id': 2, 'content': 'Another comment'},
            ],
            'people': [
                {'id': 1, 'name': 'John'},
            ]
        }
    }


def test_custom_linked_key():
    class CustomPostResponder(Responder):
        TYPE = 'posts'
        SERIALIZER = PostSerializer
        LINKS = {
            'author': {
                'responder': PersonResponder,
                'href': 'http://example.com/people/{posts.author}',
                'key': 'writer',
            },
        }

    author = {'id': 1, 'name': 'John'}
    post = {'id': 1, 'title': 'My title', 'writer': author}

    response = CustomPostResponder.build(post, linked={
        'author': [author],
    })

    assert response == {
        'posts': {
            'id': 1,
            'title': 'My title',
            'links': {
                'author': 1,
            }
        },
        'links': {
            'posts.author': {
                'href': 'http://example.com/people/{posts.author}',
                'type': 'people',
            }
        },
        'linked': {
            'people': [
                {'id': 1, 'name': 'John'},
            ],
        }
    }
