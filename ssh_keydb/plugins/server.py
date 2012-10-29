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
from group import *

__all__ = ['ServerController']


class ServerController(Controller):
    def filter(self, *args, **opts):
        if len(args) > 0:
            return None

        serverlist = Server.query.filter(None)

        if 'server' in opts:
            serverlist = Server.query.filter_by(server=opts['server'])

        return serverlist.all()

    def list(self, *args, **opts):
        if len(args) > 0:
            raise SyntaxError()

        lst = self.filter(*args, **opts)
        for item in lst:
            print item

    def key(self, *args, **opts):
        if len(args) < 4:
            raise SyntaxError()

        srvname = args[0]
        filename = args[1]
        keytype = args[2]
        keystring = args[3]

        srv = Server.get_by(server=srvname)

        if srv is None:
            return False

        srvhostkey = None
        for hostkey in srv.hostkeys:
            if hostkey.filename == filename:
                srvhostkey = hostkey

        if srvhostkey is None:
            srvhostkey = ServerHostKey(filename=filename, server=srv)

        if keytype == 'pubkey':
            srvhostkey.public_key = keystring
        elif keytype == 'privkey':
            srvhostkey.private_key = keystring

        session.flush()
        session.commit()

        return True

    def set(self, *args, **opts):
        if len(args) < 1:
            raise SyntaxError()

        srvname = args[0]
        fqdn = None
        grp = None

        if len(args) > 1:
            fqdn = args[1]
        if len(args) > 2:
            grpname = args[2]
            grps = ServerGroupController().filter(group=grpname)

            if len(grps) > 0:
                grp = grps[0]
            else:
                print >>sys.stderr, 'Aborted: Group %s does not exist.' % grpname
                return True

        srvlst = self.filter()

        for srv in srvlst:
            if srv.server == srvname:
                if fqdn is not None:
                    srv.fqdn = fqdn
                if grp is not None:
                    srv.server_group = grp
                return True

        srv = Server(server=srvname, fqdn=fqdn, server_group=grp)
        session.flush()
        session.commit()

        return True

    def remove(self, *args, **opts):
        serverlst = self.filter(*args, **opts)
        n = len(serverlst)

        if n > 2:
            ch = raw_input('Warning: remove all %i servers (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for server in serverlst:
            for h in server.hostkeys:
                h.delete()
            server.delete()

        session.flush()
        session.commit()

    set.usage = {
        'shortdesc': 'Manage servers',
        'usage': ['%(exec)s server set <server> [<fqdn> [<servergroup>] ]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    key.usage = {
        'shortdesc': 'Manage server keys',
        'usage': [
            '%(exec)s server key <server> <filename> privkey <keystring>',
            '%(exec)s server key <server> <filename> pubkey <keystring>',
        ],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    remove.usage = {
        'shortdesc': 'Manage servers',
        'usage': ['%(exec)s server remove [--server=<server>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'server=': 'filter by server name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage servers',
        'usage': ['%(exec)s server list [--server=<server>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'server=': 'filter by server name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    usage = {
        'command': ['server'],
        'shortdesc': 'Manage servers',
    }

ServerController()

if __name__ == '__main__':
    c = ServerController()
    c.list()
