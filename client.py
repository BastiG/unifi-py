#!/usr/bin/env python

from unifi import UnifiApi
from config import USERNAME, PASSWORD, BASE_URL

from json import dumps as json_dumps

def json_print(json, indent=2):
    print(json_dumps(json, indent=indent, sort_keys=True))

def find_by_attr(data, _as_list=False, _path='data', **attrs):
    if _path:
        for el in _path.split('.'):
            if el in data:
                data = data[el]
            else:
                return None

    results = list(filter(lambda x: all([key in x and x[key] in [value, str(value)] for key, value in attrs.items()]), data))
    if _as_list:
        return results
    return results[0] if results else None


networkconf = {
    'name': 'Test208',
    'vlan': 208,
    'vlan_enabled': True,
    'ip_subnet': '172.16.101.10/24',
    'dhcpd_enabled': False,
    'dhcp_relay_enabled': False,
    'networkgroup': 'LAN',
    'purpose': 'corporate'
}

id_rfc1918 = '5f6da85bac870f0778fe1715'
id_vlan300 = 'NETv4_br300'
id_net300 = '5f69abb388451604b25efc90'
id_resolver_v6 = '5f6da5ebac870f0778fe16da'

firewallrule = {
    'action': 'drop',
    'dst_address': '',
    'dst_firewallgroup_ids': [ id_rfc1918 ],
    'dst_networkconf_id': '',
    'dst_networkconf_type': 'NETv4',
    'enabled': False,
    'icmp_typename': '',
    'ipsec': '',
    'logging': False,
    'name': 'Test ACL',
    'protocol': 'all',
    'protocol_match_excepted': False,
    'rule_index': 4002,
    'ruleset': 'LAN_IN',
    'src_address': '',
    'src_firewallgroup_ids': [ ],
    'src_mac_address': '',
    'src_networkconf_id': id_net300,
    'src_networkconf_type': 'NETv4',
    'state_established': False,
    'state_invalid': False,
    'state_new': False,
    'state_related': False
}
firewallrule = {
    'action': 'drop',
    'dst_firewallgroup_ids': [ id_resolver_v6 ],
    'enabled': False,
    'icmpv6_typename': '',
    'logging': False,
    'name': 'Test v6',
    'protocol_v6': 'all',
    'rule_index': 2500,
    'ruleset': 'LANv6_IN',
    'src_firewallgroup_ids': [ ],
    'src_networkconf_id': id_net300
}

unifi = UnifiApi(BASE_URL)
if unifi.login(USERNAME, PASSWORD):
    print('Login successful')

    #networks = unifi.networkconf()
    #json_print(networks)
    #networks = unifi.networkconf(data=networkconf)
    #json_print(networks)
    # json_print(find_by_attr(networks, vlan_enabled=False))
    # json_print(unifi.network(id='5f7ae5511883e6099a8fa75b',data=network))
    # udm.sites()

    portconfs = unifi.portconf()
    portconf_disabled = find_by_attr(portconfs, name='Disabled')
    portconf_all = find_by_attr(portconfs, name='All')
    # json_print(portconf_disabled)

    device = find_by_attr(unifi.device(), name='udmpro1')
    # json_print(device)
    port6 = find_by_attr(device, _path='port_table', name="Port 6")
    port_overrides = device['port_overrides']

    # print(f'Device {device["_id"]} Port 6 index: {port6["port_idx"]}')
    port6_override = find_by_attr(port_overrides, _path=None, port_idx=port6['port_idx'])
    if port6_override['portconf_id'] != portconf_disabled['_id']:
        print('Port 6 is NOT disabled => will disable now')
        port6_override['portconf_id'] = portconf_disabled['_id']
    else:
        print('Port 6 is already disabled => will enable now')
        port6_override['portconf_id'] = portconf_all['_id']

    unifi.device(id=device['_id'], data={'port_overrides': port_overrides})

    #json_print(port6)
    #json_print(port_overrides)

#   List
#   firewall_rules = unifi.firewallrule()
#   Create
#    firewall_rules = unifi.firewallrule(data=firewallrule)
#    json_print(firewall_rules)

    print('Logging out')
    unifi.logout()

else:
    print('Login failed')
