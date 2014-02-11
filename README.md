hy
==
JSON-API responses in Python.

About
-----
Hy is a library implementing the _must_ parts of the [JSON-API](http://jsonapi.org) response specification. This means that you can use Hy to serialize your models into responses that contain links and linked compound documents. It works really good in combination with some micro web framework of choice, preferably [Flask](http://flask.pocoo.org).

It is built on top of [Schematics](https://schematics.readthedocs.org/en/latest/) in the sense that Schematics is used for data serialization and that Hy handles the rest. To add support for other data serialization libraries such as [Colander](http://docs.pylonsproject.org/projects/colander/en/latest/) should be trivial though.

The only requirements that Hy has on your models is that it should conform to the Python `dict` interface.

Tutorial
--------

First let's define some serializers for your models:

```python
from schematics.models import Model
from schematics.types import IntType, StringType


class CommentSerializer(Model):
    id = IntType()
    content = StringType()


class PersonSerializer(Model):
    id = IntType()
    name = StringType()


class PostSerializer(Model):
    id = IntType()
    title = StringType()
```

We can then create our own responders using the `hy.Responders` class:

```python
from hy.responder import Responder


class CommentResponder(Responder):
    TYPE = 'comment'
    SERIALIZER = CommentSerializer


class PersonResponder(Responder):
    TYPE = 'person'
    SERIALIZER = PersonSerializer


class PostResponder(Responder):
    TYPE = 'post'
    SERIALIZER = PostSerializer
    LINKS = {
        'comments': {
            'responder': CommentResponder(),
            'href': 'http://example.com/comments/{posts.comments}',
        },
        'author': {
            'responder': PersonResponder(),
            'href': 'http://example.com/people/{posts.author}',
        },
    }
```

Finally we can use our responders for creating responses conforming to the JSON-API specification. The only requirement for our models is that they respond to the standard Python `dict` interface. These responses goes perfectly into any Flask application out there:

```python
post = {
    'id': 1,
    'title': 'My post',
    'comments': [
        {'id': 1, 'content': 'A comment'},
        {'id': 2, 'content': 'Another comment'},
    ]
}

json = PostResponder().respond(post, linked={'comments': comments})

```

The `json` variable will now contain some freshly squeezed json ready for sending back to the client:

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
