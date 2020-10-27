from unifi.objects.base import UnifiBaseObject

from unifi.helper import find_by_attr, json_print


class UnifiDeviceObject(UnifiBaseObject):
    def get_port_profile(self, **filter_kwargs):
        port = find_by_attr(self.port_table, **filter_kwargs)
        port_override = find_by_attr(self.port_overrides, port_idx=port['port_idx'])
        portconf_id = port_override['portconf_id'] if port_override and 'portconf_id' in port_override else port['portconf_id']
        portconf = find_by_attr(self.controller.portconf(), _id=portconf_id)
        return portconf

    def set_port_profile(self, portconf, **filter_kwargs):
        port = find_by_attr(self.port_table, **filter_kwargs)
        port_override = find_by_attr(self.port_overrides, port_idx=port['port_idx'])
        if port_override:
            port_override['portconf_id'] = portconf['_id']
        else:
            port_override = {
                'port_idx': port['port_idx'],
                'portconf_id': portconf['_id']
            }
            self.port_overrides.append(port_override)
