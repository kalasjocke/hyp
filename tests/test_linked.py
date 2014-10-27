from hyp.schematics import Responder as SchematicsResponder

from fixtures import (
    PostResponder,
    PersonResponder,
    PostSerializer,
)


class TestLinked(object):
    def test_single(self):
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

    def test_multiple_same_type(self):
        class MultipleAuthorsResponder(SchematicsResponder):
            TYPE = 'posts'
            SERIALIZER = PostSerializer
            LINKS = {
                'author': {
                    'responder': PersonResponder,
                    'href': 'http://example.com/people/{posts.author}',
                },
                'coauthor': {
                    'responder': PersonResponder,
                    'href': 'http://example.com/people/{posts.author}',
                },
            }

        author = {'id': 1, 'name': 'John'}
        coauthor = {'id': 2, 'name': 'Lisa'}
        post = {'id': 1, 'title': 'My title', 'author': author, 'coauthor': coauthor}

        response = MultipleAuthorsResponder.build(post, linked={
            'author': [author], 'coauthor': [coauthor]
        })

        assert len(response['linked']['people']) == 2
        ids = [person['id'] for person in response['linked']['people']]
        assert 1 in ids
        assert 2 in ids

    def test_custom_linked_key(self):
        class CustomPostResponder(SchematicsResponder):
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
