import json

from serverdensity.wrapper.jsonobject import JsonObject
from serverdensity import Response


class Metrics(JsonObject):

    PATHS = {
        'available': '/metrics/v3/metrics/{}',
        'get': '/metrics/v3/query/{}'
    }

    def _validation(self, value):
        """Not needed"""
        pass

    def available(self, start, end, **kwargs):
        kwargs.setdefault('params', {})['start'] = start.isoformat()
        kwargs['params']['end'] = end.isoformat()
        result = self.api.get(url=self.PATHS['available'], **kwargs)
        return [Response(item) for item in result]

    def get(self, start, end, filtering, **kwargs):
        kwargs.setdefault('params', {})['start'] = start.isoformat()
        kwargs['params']['end'] = end.isoformat()
        kwargs['params']['filter'] = json.dumps(filtering)
        result = self.api.get(url=self.PATHS['get'], **kwargs)
        return [Response(item) for item in result]
