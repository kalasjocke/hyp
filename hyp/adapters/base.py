from __future__ import absolute_import

from schematics.models import Model as SchematicsSerializer
from marshmallow import Schema as MarshmallowSerializer

from hyp.adapters.schematics import Adapter as SchematicsAdapter
from hyp.adapters.marshmallow import Adapter as MarshmallowAdapter


def adapter_for(serializer):
    if issubclass(serializer, SchematicsSerializer):
        return SchematicsAdapter
    elif issubclass(serializer, MarshmallowSerializer):
        return MarshmallowAdapter
    else:
        raise NotImplementedError()
