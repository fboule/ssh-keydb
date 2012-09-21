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

__all__ = ['PermissionController']


class PermissionController(Controller):
    def filter(self, *args, **opts):
        if len(args) > 0:
            return None

        permlist = Permission.query.filter(None)

        if 'login' in opts:
            permlist = permlist.filter_by(login=opts['login'])

        if 'location' in opts:
            location = Location.get_by(location=opts['location'])
            if location is not None:
                permlist = permlist.filter_by(location=location)

        if 'role' in opts:
            role = Role.get_by(role=opts['role'])
            if role is None:
                return None
            permlist = permlist.filter_by(role=role)

        if 'server' in opts:
            srv = Server.get_by(server=opts['server'])
            if srv is None:
                return None
            permlist = permlist.filter_by(server=srv)
        elif 'group' in opts:
            grp = ServerGroup.get_by(server_group=opts['group'])
            if grp is None:
                return None
            oldpermlist = permlist
            permlist = []
            for perm in oldpermlist:
                if perm.server in grp.servers:
                    permlist.append(perm)

        return permlist.all()

    def set(self, *args, **opts):
        if len(args) < 4:
            raise SyntaxError()

        rolename = args[0]
        login = args[1]
        location = args[2]
        servername = args[3]
        cmd = None

        if len(args) > 4:
            cmd = args[4]

        role = Role.get_by(role=rolename)
        location = Location.get_by(location=location)
        srv = Server.get_by(server=servername)

        if role is None:
            print 'Role not defined.'
            sys.exit(1)

        if srv is None:
            print 'Server not found.'
            sys.exit(1)

        perm = Permission.get_by(role=role, server=srv, login=login, location=location)

        if perm is not None:
            print 'Already exists.'
            sys.exit(1)

        Permission(role=role, server=srv, login=login, command=cmd, location=location)

        session.flush()
        session.commit()

        return True

    def remove(self, *args, **opts):
        permlist = self.filter(*args, **opts)
        n = len(permlist)

        if n > 2:
            ch = raw_input('Warning: remove all %i permissions (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for perm in permlist:
            perm.delete()

        session.flush()
        session.commit()

        return True

    def list(self, *args, **opts):
        lst = self.filter(*args, **opts)

        if len(lst) == 0:
            return

        hdr = {'role': 'role', 'server': 'server', 'login': 'login', 'command': 'command', 'location': 'location'}

        nl = {}
        for perm in lst:
            nl['role'] = max(nl.get('role', len(hdr['role'])), len(perm.role.role))
            nl['server'] = max(nl.get('server', len(hdr['server'])), len(perm.server.server))
            nl['login'] = max(nl.get('login', len(hdr['login'])), len(perm.login))
            nl['command'] = max(nl.get('command', len(hdr['command'])), len(perm.command))
            nl['location'] = max(nl.get('location', len(hdr['location'])), len(perm.location.location))

        fmt = '%%(role)-%(role)is %%(server)-%(server)is %%(login)-%(login)is %%(location)-%(location)is' % nl
        n = sum(nl.values()) - nl['command'] + len(nl) - 2

        if 'long' in opts:
            fmt = '%%(role)-%(role)is %%(server)-%(server)is %%(login)-%(login)is %%(location)-%(location)is %%(command)-%(command)is' % nl
            n = sum(nl.values()) + len(nl) - 1

        print fmt % hdr
        print '-' * n

        for perm in lst:
            print fmt % {'role': perm.role.role, 'server': perm.server.server, 'login': perm.login, 'command': perm.command, 'location': perm.location.location}

    set.usage = {
        'shortdesc': 'Manage permission',
        'usage': ['%(exec)s permission set <role> <login> <location> <server> [<command>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    remove.usage = {
        'shortdesc': 'Manage permission',
        'usage': ['%(exec)s permission remove [--server=<server>] [--role=<role>] [--login=<login>] [--group=<group>] [--location=<location>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role',
            'group=': 'filter by server group',
            'location=': 'filter by location',
            'server=': 'filter by server name',
            'login=': 'filter by login name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage permission',
        'usage': ['%(exec)s permission list [--server=<server>] [--role=<role>] [--login=<login>] [--group=<group>] [--location=<location>] [--long]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role',
            'group=': 'filter by server group',
            'server=': 'filter by server name',
            'login=': 'filter by login name',
            'location=': 'filter by location',
            'long': 'display all columns',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'long': 'l'}
    }

    usage = {
        'command': ['permission', 'perm'],
        'shortdesc': 'Manage permission',
    }

PermissionController()

if __name__ == '__main__':
    c = PermissionController()
    c.list()
