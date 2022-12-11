# first things first
from netmiko import ConnectHandler
# define costume functions
def Replace_New_ACLs(master, backup):
    def convert(lst):
        return (lst.split())
    net_connect = ConnectHandler(**master)
    masteracl = net_connect.send_command('show run | include ip access-list')
    addacllist = masteracl.splitlines()
    if (addacllist[0] == ''):
        del addacllist[0]
    alladdacl = []
    for acl in  addacllist:
        ACLloopList = convert(acl)
        ACLloopListadd = net_connect.send_command("show ip access-list " + ACLloopList[-1])
        ACLloopEntery = ACLloopListadd.splitlines()
        if (ACLloopEntery[0] == ''):
            del ACLloopEntery[0]
        del ACLloopEntery[0]
        alladdacl.append('ip access-list extended ' + ACLloopList[-1])
        alladdacl.extend(ACLloopEntery)
    net_connect = ConnectHandler(**backup)
    deviceacl = net_connect.send_command('show run | include ip access-list')
    oldacls = deviceacl.splitlines()
    removeoldacls = []
    for rmacl in oldacls:
        removeoldacls.append('no ' + rmacl)
    replacecals = []
    replacecals.extend(removeoldacls)
    replacecals.extend(alladdacl)
    addedacls = net_connect.send_config_set(replacecals)
    wrmem = net_connect.send_command('wr')
def Replace_New_Configs(master, backup, costume_commands):
    net_connect = ConnectHandler(**master)
    newconfigurations = []
    for command in costume_commands:
        deviceconfig = net_connect.send_command('show run | section ' + command)
        deviceconfiglines = deviceconfig.splitlines()
        newconfigurations.extend(deviceconfiglines)
    net_connect = ConnectHandler(**backup)
    removeconfig = []
    for command in costume_commands:
        deviceoldconfig = net_connect.send_command('show run | include ' + command)
        removeoldconfig = deviceoldconfig.splitlines()
        for rmconfig in removeoldconfig:
            removeconfig.append('no ' + rmconfig)
    replaceconfigs = []
    replaceconfigs.extend(removeconfig)
    replaceconfigs.extend(newconfigurations)
    replacenewconfigs = net_connect.send_config_set(replaceconfigs)
    wrmem = net_connect.send_command('wr')
# device information
cisco1 = {'device_type': 'cisco_ios',
            'host':   '10.1.1.2',
            'username': 'kiavash',
            'password': '123'}
cisco2 = {'device_type': 'cisco_ios',
            'host':   '10.1.1.3',
            'username': 'kiavash',
            'password': '123'}
# let's use functions!
Replace_New_ACLs(cisco1, cisco2)
costume_commands =  ['interface Loopback','interface Tunnel', 'ip nat','ip route', 
                    'clock','ip sla', 'vrf definition', 'flow record', 'flow exporter',
                    'flow monitor', 'crypto isakmp', 'crypto ipsec', 'crypto map']
Replace_New_Configs(cisco1, cisco2, costume_commands)
