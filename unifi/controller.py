from unifi.lowlevel import LowLevelApi
from unifi.mixins import *

class UnifiController(LowLevelApi, NetworkApiMixin):
    def __init__(self, base_url):
        super(UnifiController, self).__init__(base_url)

        self.__is_unifi_os = self.__identify_unifi_os()


    def __identify_unifi_os(self):
        r = self._request('/api/system',
                          anonymous=True,
                          throw_unless=[])
        return r.status_code == 200


    def login(self, username, password):
        r = self._request('/api/auth/login' if self.__is_unifi_os else '/api/login',
                          anonymous=True,
                          json={'username': username, 'password': password}, #, 'strict': True, 'remember': False},
                          throw_unless=[])

        self._logged_in = r.status_code == 200
        return self._logged_in

    def logout(self):
        r = self._request('/api/auth/logout' if self.__is_unifi_os else '/api/logout',
                          json={},
                          throw_unless=[])
        if r.status_code == 200:
            self._logged_in = False
            return True
        return False

    @property
    def is_unifi_os(self):
        return self.__is_unifi_os


    def user(self, user='self', site='default'):
        r = self._request('/api/users/{user}' if self.__is_unifi_os else '/api/s/{site}/{user}',
                          path_params={'user': user, 'site': site})
        return r.json()
