#!/usr/bin/env python

import pexpect
import textfsm
import yaml
import multiprocessing

sw = yaml.load(open("sw.yaml"))
req = yaml.load(open("req.yaml"))

def search (input,template):
    tmpl = textfsm.TextFSM(open(template))
    return tmpl.ParseText(input)

def telnet (ip,user,passwd):
    """
    Connect to host by telnet.
    Connection timeout 5 seconds
    """
    try:
        t = pexpect.spawn('telnet {}'.format(ip))
        t.expect('User Name:', 5)
    except pexpect.TIMEOUT:
        return 1
    t.sendline(user)
    t.expect('Password:')
    t.sendline(passwd)
    t.expect('#')
    t.sendline('terminal datadump')
    t.expect('#')
    return t

def get_hostname_vlans (switches,user,passwd):

    result = dict()

    for i,ip in enumerate(switches):
        if i == 20: break
        t = telnet(ip,user,passwd)
        if t == 1: continue
        hostname = t.before.split('\n')[-1]
        t.sendline("show vlan")
        t.expect('#')
        vlans = list()
        for vlan in search(t.before,"vlans.template"):
            if int(vlan[0]) == 1: continue
            vlans.append(vlan)
        t.close()
        result[hostname.strip()] = vlans
    return result

def proccesses ():
    pass

print get_hostname_vlans(sw['switches'],req['user'],req['password'])

'''with open("vlans.yaml", "w") as v:
    res = get_hostname_vlans(sw['switches'],req['user'],req['password'])
    v.write(yaml.dump(res))'''
