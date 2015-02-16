from hyp.schematics import Responder as SchematicsResponder
from hyp.collector import Collector

from fixtures import PostResponder, PostSerializer, CommentResponder


class TestCollectorInternal(object):
    def test_collect_gather_links_unique(self):
        c = Collector()
        c.include_link(CommentResponder(), 'author')
        c.include_link(CommentResponder(), 'author')

        assert c.get_links_dict() == {
            'comments.author': {
                'href': 'http://example.com/people/{comments.author}',
                'type': 'people',
            },
        }

    def test_linked_items_get_sorted(self):
        c = Collector()
        c.add_linked('people', 1, {'id': 1})
        c.add_linked('people', 3, {'id': 3})
        c.add_linked('people', 2, {'id': 2})

        assert c.get_linked_dict() == {
            'people': [
                {'id': 1},
                {'id': 2},
                {'id': 3},
            ],
        }

    def test_duplicates_get_removed(self):
        c = Collector()
        c.add_linked('people', 1, {'id': 1})
        c.add_linked('people', 1, {'id': 1})
        c.add_linked('people', 2, {'id': 2})

        assert c.get_linked_dict() == {
            'people': [
                {'id': 1},
                {'id': 2},
            ],
        }


class TestCollect(object):
    def test_one_to_one_with_collect(self):
        author = {'id': 1}
        post = {'id': 1, 'title': 'My title', 'author': author}

        response = PostResponder.build(post, collect=True)

        assert response == {
            'posts': {
                'id': 1,
                'title': 'My title',
                'links': {
                    'author': 1,
                }
            },
            'linked': {
                'people': [author],
            },
            'links': {
                'posts.author': {
                    'href': 'http://example.com/people/{posts.author}',
                    'type': 'people',
                },
            }
        }

    def test_nested_collection(self):
        author = {'id': 1}
        flamer = {'id': 2}
        comment = {'id': 1, 'content': '<redacted>', 'author': flamer}
        post = {
            'id': 1,
            'title': 'My title',
            'author': author,
            'comments': [comment],
        }

        response = PostResponder.build(post, collect=True)

        assert response == {
            'posts': {
                'id': 1,
                'title': 'My title',
                'links': {
                    'author': 1,
                    'comments': [1],
                }
            },
            'linked': {
                'people': [author, flamer],
                'comments': [
                    {
                        'id': 1,
                        'content': '<redacted>',
                        'links': {
                            'author': 2
                        }
                    }
                ],
            },
            'links': {
                'comments.author': {
                    'href': 'http://example.com/people/{comments.author}',
                    'type': 'people',
                },
                'posts.author': {
                    'href': 'http://example.com/people/{posts.author}',
                    'type': 'people',
                },
                'posts.comments': {
                    'href': 'http://example.com/comments/{posts.comments}',
                    'type': 'comments',
                },
            }
        }


