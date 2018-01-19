#!/usr/bin/env python
# coding: utf-8

from netmiko import ConnectHandler
#switchs access
iosv_l2_SOHO1 = {'device_type': 'cisco_ios','ip': '10.0.69.11','username': 'root','password': 'toor',}
iosv_l2_SOHO2 = {'device_type': 'cisco_ios','ip': '10.0.69.12','username': 'root','password': 'toor',}
iosv_l2_STACK = {'device_type': 'cisco_ios','ip': '10.0.69.13','username': 'root','password': 'toor',}
#switchs distribution
iosv_l2_SWL3_1 = {'device_type': 'cisco_ios','ip': '10.0.69.252','username': 'root','password': 'toor',}
iosv_l2_SWL3_2 = {'device_type': 'cisco_ios','ip': '10.0.69.253','username': 'root','password': 'toor',}

all_devices = [iosv_l2_SOHO1,iosv_l2_SOHO2,iosv_l2_STACK,iosv_l2_SWL3_1,iosv_l2_SWL3_2]
#all_devices = [iosv_l2_STACK,iosv_l2_SWL3_1,iosv_l2_SWL3_2]
for device in all_devices:
		net_connect = ConnectHandler(**device)
		print "\nEn attente sur " + device['ip']

		#Configuration vlan
		config_vlan_commands_10 = ['vlan 10','name VLAN_OFFICE_1'] 
		config_vlan_commands_20 = ['vlan 20','name VLAN_OFFICE_2'] 
		config_vlan_commands_60 = ['vlan 60','name VLAN_SRV'] 
		config_vlan_commands_all = ['vlan 40','name Quarantaine','vlan 69','name GESTION','vlan 666','name NATIVE'] 
		if device['ip'] == '10.0.69.11' or device['ip'] == '10.0.69.252' or device['ip'] == '10.0.69.253':
        		print(net_connect.send_config_set(config_vlan_commands_10))
		if device['ip'] == '10.0.69.12' or device['ip'] == '10.0.69.252' or device['ip'] == '10.0.69.253':
				print(net_connect.send_config_set(config_vlan_commands_20))
		if device['ip'] == '10.0.69.13' or device['ip'] == '10.0.69.252' or device['ip'] == '10.0.69.253': 
				print(net_connect.send_config_set(config_vlan_commands_60))
		print(net_connect.send_config_set(config_vlan_commands_all))
		

		#Configuration STP
		config_rpvst_commands = ['spanning-tree mode rapid-pvst']
		config_STP_SWL3_1_commands = ['spanning-tree vlan 10 root primary','spanning-tree vlan 20 root primary','spanning-tree vlan 60 root secondary'] 
		config_STP_SWL3_2_commands = ['spanning-tree vlan 60 root primary','spanning-tree vlan 10 root secondary',
		'spanning-tree vlan 20 root secondary'] 

		if device['ip'] == '10.0.69.252':
				print(net_connect.send_config_set(config_rpvst_commands + config_STP_SWL3_1_commands))

		if device['ip'] == '10.0.69.253':
				print(net_connect.send_config_set(config_rpvst_commands + config_STP_SWL3_2_commands))
		print(net_connect.send_config_set(config_rpvst_commands))

		#Configuration Trunks et Etherchannel
		config_interfaces_range_commands = ['interface range eth 3/2-3']
		config_trunk_commands = ['switchport trunk encapsulation dot1q','switchport mode trunk',
		'switchport trunk native vlan 666','switchport trunk allow vlan 10,20,60,666','exit'] 
		config_etherchannel_interfaces_chgrp1_commands = ['interface range eth 2/0-1','channel-group 1 mode active'] 
		config_etherchannel_interfaces_chgrp2_commands = ['interface range eth 2/2-3','channel-group 2 mode active'] 
		config_etherchannel_po1_commands = ['interface port-channel 1'] 
		config_etherchannel_po2_commands = ['interface port-channel 2'] 
		save_commands = ['do wr']

		if device['ip'] =='10.0.69.252' or device['ip'] =='10.0.69.13':
				print(net_connect.send_config_set(config_etherchannel_interfaces_chgrp1_commands + config_trunk_commands))
				print(net_connect.send_config_set(config_etherchannel_po1_commands + config_trunk_commands))
		if device['ip'] =='10.0.69.253' or device['ip'] =='10.0.69.13':
				print(net_connect.send_config_set(config_etherchannel_interfaces_chgrp2_commands + config_trunk_commands))
				print(net_connect.send_config_set(config_etherchannel_po2_commands + config_trunk_commands))

		print(net_connect.send_config_set(save_commands))
		print "Configuration sur terminer!\n"
		print "***************************\n"
print "########################################################"
print "##Configuration sur terminer sur tout les équipements!##"
print "########################################################"