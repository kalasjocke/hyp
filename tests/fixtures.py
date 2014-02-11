from schematics.models import Model
from schematics.types import IntType, StringType

from hy.responder import Responder



class PostSerializer(Model):
    id = IntType()
    title = StringType()


class PostResponder(Responder):
    TYPE = 'post'
