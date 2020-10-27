#!/usr/bin/env python

import requests

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class LowLevelApi(object):
    def __init__(self, base_url):
        self.__base_url = base_url
        self.__session = requests.session()
        self.__headers = {'Origin': '{}/'.format(self.__base_url)}

        self._logged_in = False


    def __prepare_request(self, path, proxy=None, path_params=None, json=None, method=None):
        if not method:
            method = 'POST' if json is not None else 'GET'
        url='{base_url}{path}'
        url_params = {
            'base_url': self.__base_url,
            'path': path
        }
        if proxy:
            url = '{base_url}/proxy/{proxy}{path}'
            url_params['proxy'] = proxy
        if path_params is None:
            path_params = {}

        url=url.format(**url_params).format(**path_params)
        request = requests.Request(
                method=method,
                url=url,
                headers=self.__headers,
                json=json
            )

        request = self.__session.prepare_request(request)
        return request


    def _request(self, path, throw_unless=[200], anonymous=False, proxy=None, path_params=None, json=None, method=None):
        if not anonymous and not self._logged_in:
            raise Exception('Not logged in')

        request = self.__prepare_request(path,
                                         proxy=proxy,
                                         path_params=path_params,
                                         json=json,
                                         method=method)
        response = self.__session.send(request, verify=False)
        return self.__handle_response(response, throw_unless)


    def __handle_response(self, response, throw_unless):
        if throw_unless and response.status_code not in throw_unless:
            raise Exception('Unexpected response code {status_code} is none of {expected} on {method} {url} - {headers} - {response}'.format(
                status_code=response.status_code, expected=throw_unless, method=response.request.method, url=response.request.url, headers=response.request.headers, response=response.text))
            
        if 'x-csrf-token' in response.headers:
            self.__headers['X-CSRF-Token'] = response.headers['x-csrf-token']
        self.__headers['Referer'] = response.url
        return response

