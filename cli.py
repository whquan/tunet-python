# -*- coding: UTF-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import getpass
import sys
import tunet


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                        description='TUNet Command-Line Interface')
    parser.add_argument('target',
                        help='Select target: auth4 / auth6 / net')
    parser.add_argument('action',
                        help='Select action: login / logout / checklogin')
    parser.add_argument('-u', '--user', '--username',
                        help='Login username', required=False)
    parser.add_argument('-n', '--net', action='store_true',
                        help='Also login net.tsinghua.edu.cn', required=False)
    args = parser.parse_args()

    def error(s):
        print(s)
        exit(1)

    if args.target not in ('auth4', 'auth6', 'net'):
        error('tunet: no such target')
    if args.action not in ('login', 'logout', 'checklogin'):
        error('tunet: no such action')
    target = getattr(tunet, args.target)
    action = getattr(target, args.action)
    if args.action == 'login':
        if not args.user:
            error('login: username required')
        if sys.stdin.isatty():
            password = getpass.getpass()
        else:
            password = sys.stdin.readline()
        try:
            if args.target == 'net':
                res = action(args.user, password)
            else:
                res = action(args.user, password, bool(args.net))
        except:
            error('connection error: unreachable or timeout')
    else:
        try:
            res = action()
        except Exception as e:
            if isinstance(e, tunet.NotLoginError):
                print('not log in')
                exit(0)
            else:
                error('connection error: unreachable or timeout')

    if args.target == 'net':
        if args.action == 'checklogin':
            if not res.get('username'):
                print('not login')
                exit(1)
            else:
                print('Username:', res['username'])
                print('Time online:', res['time_query'] - res['time_login'])
                print('Session traffic incoming:', res['session_incoming'])
                print('Session traffic outgoing:', res['session_outgoing'])
                print('Cumulative traffic:', res['cumulative_incoming'])
                print('Cumulative online time', res['cumulative_time'])
                print('IPv4 address:', res['ipv4_address'])
                print('Balance:', res['balance'])
                exit(0)
        else:
            print('message:', res['msg'])
            if 'is successful' in res['msg'] or \
                    'has been online' in res['msg'] or \
                    'are not online' in res['msg']:
                exit(0)
            else:
                exit(1)
    else:
        if args.action == 'checklogin':
            if not res.get('username'):
                print('not login')
                exit(1)
            else:
                print('username:', res['username'])
                exit(0)
        else:
            print('return:', res.get('error'))
            print('result:', res.get('res'))
            print('message:', res.get('error_msg'))
            if res.get('error') == 'ok' or \
                    res.get('error') == 'ip_already_online_error':
                exit(0)
            else:
                exit(1)
