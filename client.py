#!/usr/bin/env python

from unifi import UnifiController
from config import USERNAME, PASSWORD, BASE_URL

from unifi.helper import find_by_attr, json_print


new_network = {
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

new_firewallrule = {
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
new_firewallrule_v6 = {
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

unifi = UnifiController(BASE_URL)

# status of Unifi Network Controller
#json_print(unifi.status())

if unifi.login(USERNAME, PASSWORD):
    print('Login successful')

    # current user info
    #json_print(unifi.user())
    # list of configured sites
    #json_print(unifi.site())
    # list of known devices
    #json_print(unifi.device())

    # list of networks
    #json_print(unifi.networkconf())
    # create new network from new_network
    #networks = unifi.networkconf(data=new_network)
    #json_print(networks)

    # list switch port profiles
    portconfs = unifi.portconf()
    portconf_disabled = find_by_attr(portconfs, name='Disabled')
    portconf_enabled = find_by_attr(portconfs, name='All')
    #json_print(portconf_disabled)
    #json_print(portconf_enabled)

    # get device 'udmpro1'
    device = find_by_attr(unifi.device(), name='udmpro1')
    port_profile = device.get_port_profile(name='Port 6')
    if port_profile['_id'] == portconf_disabled['_id']:
        print('Port is already disabled -> will enable now')
        device.set_port_profile(portconf_enabled, name='Port 6')
    else:
        print('Port is NOT disabled -> will disable now')
        device.set_port_profile(portconf_disabled, name='Port 6')

    # json_print(device.port_overrides)
    unifi.device(id=device._id, data={'port_overrides': device.port_overrides})

    # list firewall rules
    #json_print(unifi.firewallrule())
    # add firewall rule from new_firewallrule
    #firewallrules = unifi.firewallrule(data=new_firewallrule)
    #json_print(firewallrules)

    print('Logging out')
    if not unifi.logout():
        print('Logout failed')

else:
    print('Login failed')
