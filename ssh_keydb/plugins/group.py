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

__all__ = ['ServerGroupController']


class ServerGroupController(Controller):
    def filter(self, *args, **opts):
        if len(args) > 0:
            return None

        grouplist = ServerGroup.query.filter(None)

        if 'group' in opts:
            grouplist = grouplist.filter_by(server_group=opts['group'])

        if 'server' in opts:
            srv = Server.get_by(server=opts['server'])
            if srv is None:
                return None
            grouplist = grouplist.filter(ServerGroup.servers.any(server=opts['server']))

        return grouplist.all()

    def list(self, *args, **opts):
        if len(args) > 0:
            raise SyntaxError()

        lst = self.filter(*args, **opts)
        for item in lst:
            print item

    def set(self, *args, **opts):
        if len(args) < 2:
            raise SyntaxError()

        groupname = args[0]
        srvnames = args[1:]

        grp = ServerGroup.get_by(server_group=groupname)

        if grp is None:
            grp = ServerGroup(server_group=groupname)

        srvlst = grp.servers[:]

        for servername in args[1:]:
            srv = Server.get_by(server=servername)

            if srv is None:
                srv = Server(server=servername)

            if srv not in grp.servers:
                grp.servers.append(srv)

        if not 'append' in opts:
            for srv in srvlst:
                if srv.server not in srvnames:
                    grp.servers.remove(srv)
                    permlist = Permission.query.filter_by(server=srv).all()
                    if len(permlist) > 0:
                        print 'Server %s has %i permission elements.' % (srv.server, len(permlist))
                        print permlist
                        sys.exit(1)
                    srv.delete()

        session.flush()
        session.commit()

        return True

    def remove(self, *args, **opts):
        grouplist = self.filter(*args, **opts)
        n = len(grouplist)

        if n > 2:
            ch = raw_input('Warning: remove all %i groups (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for group in grouplist:
            group.delete()

        session.flush()
        session.commit()

    set.usage = {
        'shortdesc': 'Manage server groups',
        'usage': ['%(exec)s group set [--append] <group> <server1> [<server2>...]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (/.ssh-keydb.db by default)',
            'append': 'append servers to the group',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'dbpath': 'd:', }
    }

    remove.usage = {
        'shortdesc': 'Manage server groups',
        'usage': ['%(exec)s group remove [--group=<group>] [--server=<server>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (/.ssh-keydb.db by default)',
            'group=': 'filter by server group name',
            'server=': 'filter by server name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage server groups',
        'usage': ['%(exec)s group list [--group=<group>] [--server=<server>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (/.ssh-keydb.db by default)',
            'group=': 'filter by server group name',
            'server=': 'filter by server name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    usage = {
        'command': ['group'],
        'shortdesc': 'Manage server groups',
    }

ServerGroupController()

if __name__ == '__main__':
    c = ServerGroupController()
    c.list()
