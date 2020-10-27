from unifi.helper import find_by_attr, json_print

class UnifiDevice(object):
    def __init__(self, controller, raw):
        self.__controller = controller
        self.__raw = raw

    @property
    def id(self):
        return self.__raw['id']

    @property
    def name(self):
        return self.__raw['name']

    def get_port_profile(self, name):
        port = find_by_attr(self.__raw, _path='port_table', name=name)
        port_override = find_by_attr(self.__raw, path='port_overrides', port_idx=port['port_idx'])
        portconf_id = port_override['portconf_id'] if port_override and 'portconf_id' in port_override else port['portconf_id']
        portconf = find_by_attr(self.__controller.portconf(), _id=portconf_id)
        return portconf

