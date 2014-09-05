Hyp
===
JSON-API responses in Python.

About
-----
Hyp is a library implementing the _must_ parts of the [JSON-API](http://jsonapi.org) response specification. This means that you can use Hyp to serialize your models into responses that contain links and linked compound documents. It works really good in combination with your micro web framework of choice, preferably [Flask](http://flask.pocoo.org).

It has built in support for both [Schematics](https://schematics.readthedocs.org/) and [Marshmallow](http://marshmallow.readthedocs.org) in the sense that you can use any of them for serializing your models (or primitives) into JSON that Hyp creates responses from. To add support for more data serialization libraries such as [Colander](http://docs.pylonsproject.org/projects/colander/en/latest/) should be trivial though.

Tutorial
--------
First let's define some serializers for your models:

```python
from marshmallow import Serializer, fields


class CommentSerializer(Serializer):
    id = fields.Integer()
    content = fields.String()


class PersonSerializer(Serializer):
    id = fields.Integer()
    name = fields.String()


class PostSerializer(Serializer):
    id = fields.Integer()
    title = fields.String()
```

We can then create our own responders using the `hyp.Responders` class:

```python
from hyp.responder import Responder


class CommentResponder(Responder):
    TYPE = 'comments'
    SERIALIZER = CommentSerializer


class PersonResponder(Responder):
    TYPE = 'people'
    SERIALIZER = PersonSerializer


class PostResponder(Responder):
    TYPE = 'posts'
    SERIALIZER = PostSerializer
    LINKS = {
        'comments': {
            'responder': CommentResponder,
            'href': 'http://example.com/comments/{posts.comments}',
        },
        'author': {
            'responder': PersonResponder,
            'href': 'http://example.com/people/{posts.author}',
        },
    }
```

Finally we can use our responders for creating responses. These responses goes perfectly into any Flask application out there:

```python
post = {
    'id': 1,
    'title': 'My post',
    'comments': [
        {'id': 1, 'content': 'A comment'},
        {'id': 2, 'content': 'Another comment'},
    ]
}

json = PostResponder.respond(post, linked={'comments': post['comments']})

```

The `json` variable will now contain some freshly squeezed JSON ready for sending back to the client:

```json
{
    "posts": [
        {
            "id": 1,
            "title": "My title",
            "links": {
                "comments": [1, 2]
            }
        }
    ],
    "linked": {
        "comments": [
            {
                "id": 1,
                "content": "My comment"
            },
            {
                "id": 2,
                "content": "Another comment"
            }
        ]
    },
    "links": {
        "posts.comments": {
            "type": "comments",
            "href": "http://example.com/comments/{posts.comments}"
        }
    }
}
```

If you'd like to get have dict returned instead of json, for example if you want to use flask's [jsonify](http://flask.pocoo.org/docs/api/#flask.json.jsonify), then you can use the `build` method instead:

```python
post = {
    'id': 1,
    'title': 'My post',
    'comments': [
        {'id': 1, 'content': 'A comment'},
        {'id': 2, 'content': 'Another comment'},
    ]
}

response = PostResponder.build(post, linked={'comments': post['comments']})
json = flask.jsonify(response)
```
