#!/usr/bin/env python

import textfsm
import yaml

def search (input,template):
    tmpl = textfsm.TextFSM(open(template))
    return tmpl.ParseText(input)

run = open("sh_run.txt").read()
print search(run,"access.template")
