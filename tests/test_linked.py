import json

from fixtures import PostResponder


def test_linked(post, comment_factory):
    comments = [
        comment_factory(id=1, content='My comment'),
        comment_factory(id=2, content='Another comment'),
    ]

    post.comments = comments

    data = PostResponder().respond(post, linked={'comments': comments})

    assert json.loads(data) == {
        'posts': [
            {
                'id': 1,
                'title': 'My title',
                'links': {
                    'comments': [1, 2],
                }
            },
        ],
        'links': {
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
        }
    }
