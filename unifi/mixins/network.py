#!/usr/bin/env python

from unifi.objects import UnifiDeviceObject

class NetworkApiMixin(object):
    def __crud_request(self, path, site, id, data, proxy='network', map_to=None):
        kwargs = {
            'json': data
        }
        if id is None:
            path = '/api/s/{site}{path}'.format(site=site, path=path)
            kwargs['method'] = 'GET' if data is None else 'POST'
        else:
            path = '/api/s/{site}{path}/{id}'.format(site=site, path=path, id=id)
            kwargs['method'] = 'DELETE' if data is None else 'PUT'

        if self.is_unifi_os:
            kwargs['proxy'] = proxy

        r = self._request(path, **kwargs)

        if map_to:
            result = []
            for item in r.json().get('data', []):
                result.append(map_to(self, item))
            return result
        else:
            return r.json()


    def networkconf(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/networkconf', site, id, data)

    def firewallrule(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/firewallrule', site, id, data)

    def portconf(self, site='default', id=None, data=None):
        return self.__crud_request('/rest/portconf', site, id, data)

    def device(self, site='default', id=None, data=None):
        path = '/rest/device' if id or data else '/stat/device'
        return self.__crud_request(path, site, id, data, map_to=UnifiDeviceObject)

    def status(self):
        r = self._request('/status',
                          proxy='network' if self.is_unifi_os else None,
                          anonymous=True)
        return r.json()

    def site(self):
        r = self._request('/api/self/sites',
                          proxy='network' if self.is_unifi_os else None)
        return r.json()
