#!/usr/bin/env python

class NetworkApiMixin(object):
    def __crud_request(self, path, site, id, data, proxy='network'):
        if id is None:
            path = f'/api/s/{site}{path}'
            method = 'GET' if data is None else 'POST'
        else:
            path = f'/api/s/{site}{path}/{id}'
            method = 'DELETE' if data is None else 'PUT'

        r = self._request(path, proxy=proxy, method=method, json=data)
        return r.json()


    def networkconf(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/networkconf', site, id, data)

    def firewallrule(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/firewallrule', site, id, data)

    def portconf(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/portconf', site, id, data)

    def device(self, site='default', id=None, data=None):
        path = '/rest/device' if id or data else '/stat/device'
        return self.__crud_request(path, site, id, data)

