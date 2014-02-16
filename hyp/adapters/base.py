from __future__ import absolute_import

from schematics.models import Model as SchematicsSerializer
from marshmallow import Serializer as MarshmallowSerializer

from hyp.adapters.schematics import SchematicsSerializerAdapter
from hyp.adapters.marshmallow import MarshmallowSerializerAdapter


def adapter_for(serializer):
    if isinstance(serializer(), SchematicsSerializer):
        return SchematicsSerializerAdapter
    elif isinstance(serializer(), MarshmallowSerializer):
        return MarshmallowSerializerAdapter
    else:
        raise NotImplementedError()
