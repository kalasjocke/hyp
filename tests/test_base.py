import pytest
from hyp.base import BaseResponder, BaseAdapter

from fixtures import CommentSerializer

class TestBaseResponder(object):

    def test_error_raised_if_adapter_not_specified(self):
        # No Adapter specified
        class BadResponder(BaseResponder):
            TYPE = 'comments'
            SERIALIZER = CommentSerializer
        with pytest.raises(NotImplementedError) as excinfo:
            BadResponder()
        msg = 'Responder must define ADAPTER class variable'
        assert msg in str(excinfo)


class TestBaseAdapter(object):

    def test_error_raised_if_call_not_implemented(self):
        # __call__ not implemented
        class BadAdapter(BaseAdapter):
            pass
        bad_adapter = BadAdapter()
        with pytest.raises(NotImplementedError) as excinfo:
            bad_adapter({'id': 1})
        msg = 'Adapter class must define __call__'
        assert msg in str(excinfo)
