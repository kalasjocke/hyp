from hyp.schematics import Responder as SchematicsResponder

from fixtures import PostResponder, PostSerializer, CommentResponder


class TestLinks(object):
    def test_one_to_many(self):
        comments = [
            {'id': 1, 'content': 'My comment'},
            {'id': 2, 'content': 'Another comment'},
        ]
        post = {'id': 1, 'title': 'My title', 'comments': comments}

        response = PostResponder.build(post, links=['comments'])

        assert response == {
            'posts': {
                'id': 1,
                'title': 'My title',
                'links': {
                    'comments': [1, 2],
                }
            },
            'links': {
                'posts.comments': {
                    'href': 'http://example.com/comments/{posts.comments}',
                    'type': 'comments',
                }
            }
        }

    def test_one_to_one(self):
        author = {'id': 1}
        post = {'id': 1, 'title': 'My title', 'author': author}

        response = PostResponder.build(post, links=['author'])

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
            }
        }


class TestLinksWithMissingValues(object):
    def test_one_to_one_with_missing_value(self):
        author = {'id': 1}
        p1 = {'id': 1, 'title': 'My title', 'author': author}
        p2 = {'id': 2, 'title': 'My other title', 'author': None}

        response = PostResponder.build([p1, p2], links=['author'])

        assert response == {
            'posts': [{
                'id': 1,
                'title': 'My title',
                'links': {
                    'author': 1,
                },
            }, {
                'id': 2,
                'title': 'My other title',
                'links': {},
            }],
            'links': {
                'posts.author': {
                    'href': 'http://example.com/people/{posts.author}',
                    'type': 'people',
                }
            }
        }

    def test_one_to_many_with_missing_values(self):
        comments = [None, None]
        post = {'id': 1, 'title': 'My title', 'comments': comments}

        response = PostResponder.build(post, links=['comments'])

        assert response == {
            'posts': {
                'id': 1,
                'title': 'My title',
                'links': {},
            },
            'links': {
                'posts.comments': {
                    'href': 'http://example.com/comments/{posts.comments}',
                    'type': 'comments',
                }
            }
        }


class TestHref(object):
    def test_without_href(self):
        class MyPostResponder(SchematicsResponder):
            TYPE = 'posts'
            SERIALIZER = PostSerializer
            LINKS = {
                'comments': {'responder': CommentResponder},
            }

        comments = [
            {'id': 1, 'content': 'My comment'},
            {'id': 2, 'content': 'Another comment'},
        ]
        post = {'id': 1, 'title': 'My title', 'comments': comments}

        response = MyPostResponder.build(post, links=['comments'])

        assert response == {
            'posts': {
                'id': 1,
                'title': 'My title',
                'links': {
                    'comments': [1, 2],
                }
            },
            'links': {
                'posts.comments': {
                    'type': 'comments',
                }
            }
        }
