import json

from fixtures import PostResponder, PostSerializer


def test_single(post):
    responder = PostResponder.schematics(PostSerializer)

    data = responder.respond(post)

    assert json.loads(data) == {'posts': [{'id': 1, 'title': 'My title'}]}


def test_multiple(post_factory):
    post = post_factory(id=1, title='A title')
    another_post = post_factory(id=2, title='Another title')

    responder = PostResponder.schematics(PostSerializer)
    data = responder.respond([post, another_post])

    assert json.loads(data) == {
        'posts': [
            {'id': 1, 'title': 'A title'},
            {'id': 2, 'title': 'Another title'},
        ]
    }


def test_meta(post):
    responder = PostResponder.schematics(PostSerializer)
    data = responder.respond(post, meta={'key': 'value'})

    assert json.loads(data)['meta']['key'] == 'value'


# def test_links(post, author):
#     pass
    # data = PostSerializer().to_json(post, author=author)

    # assert data
