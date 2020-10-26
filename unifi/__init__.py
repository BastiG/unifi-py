#!/usr/bin/env python

from .lowlevel import LowLevelApi
from .mixins import *

class UnifiApi(LowLevelApi, NetworkApiMixin):
    def login(self, username, password):
        r = self._request('/api/auth/login',
                           anonymous=True,
                           json={'username': username, 'password': password},
                           throw_unless=[])
        self._logged_in = r.status_code == 200
        return self._logged_in

    def logout(self):
        r = self._request('/api/auth/logout',
                           method='POST',
                           throw_unless=[])
        if r.status_code == 200:
            self._logged_in = False
            return True
        return False

    def user(self, user='self'):
        r = self._request('/api/users/{user}',
                           method='GET',
                           path_params={'user': user})
        return r.json()

    def site(self):
        r = self._request('/api/self/sites',
                           method='GET',
                           proxy='network')
        return r.json()
