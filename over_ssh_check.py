#!/usr/bin/env python

# -*- coding: utf-8 -*-
'''
Perform nagios check over ssh with password.

.. code-block:: bash
over_ssh_check.py -H example.com -l userslogin -p passw0rd -c '/home/userlogin/check_disk -w 15% -c 10% -W 15% -K 10% -p /dev/sda1'

:codeauthor: Jiri Kotlin <jirka@poslouchej.net>

modifed by Dave Holland <dave@biff.org.uk> to optionally check for a
string in the returned output

'''
import sys
import pexpect
import argparse

parser = argparse.ArgumentParser(description='Execute script via ssh.')

required = parser.add_argument_group('required arguments')

required.add_argument('-H', type=str, help="hostname or ip address", required=True, dest="hostname")
required.add_argument('-l', type=str, help="login to ssh on host", required=True, dest="login")
required.add_argument('-p', type=str, help="password to ssh", required=True, dest="password")
required.add_argument('-c', type=str, help="command to execute", required=True, dest="command")

required.add_argument('-s', type=str, help="string to expect", required=False, dest="string")

args = parser.parse_args()

try:
    try:
        child = pexpect.spawn("ssh {0}@{1} {2}".format(args.login, args.hostname, args.command))
        i = child.expect(['assword:'])
        child.sendline(args.password)
    except pexpect.EOF:
        ret =  "CRITICAL - unable to login to ssh at {0}".format(args.hostname)
        print ret
        sys.exit(2)

    i = child.expect([pexpect.EOF])
    if i == 0:
        ret = child.before.strip()
        if not args.string:
            #print ret
            print "OK connected by SSH"
            sys.exit(0)
        else:
            if not args.string in ret:
                print "CRITICAL - connected but expected output '" + args.string + "' not found"
                #print ret
                sys.exit(2)
            else:
                print "OK connected by SSH and found '" + args.string + "'"
                #print ret
                sys.exit(0)
    else:
        print "CRITICAL - unable to read output."
        sys.exit(2)
except pexpect.TIMEOUT:
    print "CRITICAL - request timed out"
    sys.exit(2)

