# ssh-keydb - http://ssh-keydb.googlecode.com/
#
# Copyright (C) 2010 Fabien Bouleau
#
# This file is part of ssh-keydb.
#
# ssh-keydb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ssh-keydb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ssh-keydb.  If not, see <http://www.gnu.org/licenses/>.

import sys
from model import *
from skeletool.controller import Controller

__all__ = ['MembershipController']


class MembershipController(Controller):
    def filter(self, *args, **opts):
        if len(args) > 0:
            return None

        memblist = Membership.query.filter(None)

        if 'user' in opts:
            user = User.get_by(user=opts['user'])
            if user is None:
                return None
            memblist = memblist.filter_by(user=user)

        if 'role' in opts:
            role = Role.get_by(role=opts['role'])
            if role is None:
                return None
            memblist = memblist.filter_by(role=role)

        if 'key' in opts:
            key = Key.get_by(key_name=opts['key'])
            if key is None:
                return None
            memblist = memblist.filter_by(key=key)

        if 'group' in opts:
            group = ServerGroup.get_by(server_group=opts['group'])
            if group is None:
                return None
            memblist = memblist.filter_by(server_group=group)

        return memblist.all()

    def grant(self, *args, **opts):
        if len(args) < 4:
            raise SyntaxError()

        username = args[0]
        keyname = args[1]
        rolename = args[2]
        groupname = args[3]

        cmdargs = ''
        if len(args) > 4:
            cmdargs = args[4]

        user = User.get_by(user=username)
        key = Key.get_by(key_name=keyname, user=user)
        grp = ServerGroup.get_by(server_group=groupname)
        role = Role.get_by(role=rolename)

        if None in (user, key, grp, role):
            return False

        memb = Membership.get_by(user=user, key=key, server_group=grp, role=role)

        if memb is None:
            Membership(user=user, key=key, server_group=grp, role=role, args=cmdargs)
        else:
            memb.args = cmdargs

        session.flush()
        session.commit()

        return True

    def revoke(self, *args, **opts):
        memblist = self.filter(*args, **opts)
        n = len(memblist)

        if n > 2:
            ch = raw_input('Warning: remove all %i memberships (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for memb in memblist:
            s = '(%s, %s, %s, %s, %s)' % (memb.server_group.server_group, memb.role.role, memb.user.user,
                    memb.key.key_name, memb.args)
            memb.delete()

        session.flush()
        session.commit()

        return True

    def list(self, *args, **opts):
        lst = self.filter(*args, **opts)

        if len(lst) == 0:
            return

        hdr = {'group': 'group', 'user': 'user', 'key': 'key', 'role': 'role', 'args': 'arguments'}

        nl = {}
        for memb in lst:
            nl['group'] = max(nl.get('group', len(hdr['group'])), len(memb.server_group.server_group))
            nl['user'] = max(nl.get('user', len(hdr['user'])), len(memb.user.user))
            nl['key'] = max(nl.get('key', len(hdr['key'])), len(memb.key.key_name))
            nl['role'] = max(nl.get('role', len(hdr['role'])), len(memb.role.role))
            nl['args'] = max(nl.get('args', len(hdr['args'])), len(memb.args or ''))

        fmt = '%%(group)-%(group)is %%(user)-%(user)is %%(key)-%(key)is %%(role)-%(role)is' % nl
        n = sum(nl.values()) - nl['args'] + len(nl) - 2

        if 'long' in opts:
            fmt = '%%(group)-%(group)is %%(user)-%(user)is %%(key)-%(key)is %%(role)-%(role)is %%(args)-%(args)is' % nl
            n = sum(nl.values()) + len(nl) - 1

        print fmt % hdr
        print '-' * n

        for memb in lst:
            print fmt % {'group': memb.server_group.server_group, 'user': memb.user.user, 'key': memb.key.key_name, 'role': memb.role.role, 'args': memb.args}

    grant.usage = {
        'shortdesc': 'Manage membership',
        'usage': ['%(exec)s membership grant <user> <key> <role> <group> [<args>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    revoke.usage = {
        'shortdesc': 'Manage membership',
        'usage': ['%(exec)s membership revoke [--group=<group>] [--role=<role>] [--key=<key>] [--user=<user>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role',
            'group=': 'filter by server group',
            'key=': 'filter by key name',
            'user=': 'filter by user name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage membership',
        'usage': ['%(exec)s membership list [--group=<group>] [--role=<role>] [--key=<key>] [--user=<user>] [--long]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role',
            'group=': 'filter by server group',
            'key=': 'filter by key name',
            'user=': 'filter by user name',
            'long': 'display all columns',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'long': 'l'}
    }

    usage = {
        'command': ['membership', 'memb'],
        'shortdesc': 'Manage membership',
    }

MembershipController()

if __name__ == '__main__':
    c = MembershipController()
    c.list()
