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

import os
import os.path
import sys
from model import *
from skeletool.controller import Controller

__all__ = ['GeneratorController']


class OpenSSHGenerator(object):
    def run(self):
#        opts = self.__opts
#
#        srvlst, role, login = OptsFilter().filter(opts)
#        scplist = {}
#
#        for srv in srvlst:
#            srvgrp = srv.server_group
#            if login is not None:
#                perms = Permission.query.filter_by(login = login, server = srv)
#            else:
#                perms = Permission.query.filter_by(role = role, server = srv)
#            for p in perms:
#                filename = 'authorized_keys_%s_%s' % (p.login, srv.server)
#                if os.path.exists(filename): os.remove(filename)
#                if filename not in scplist: scplist[filename] = (p.login, srv.fqdn)
#            for p in perms:
#                f = file('authorized_keys_%s_%s' % (p.login, srv.server), 'a')
#                membs = p.role.memberships
#                for m in membs:
#                    if srvgrp == m.server_group:
#                        print >>f, ('%s %s %s' % (p.command % eval(m.args), m.key.key_value, m.key.key_name)).strip()
#            if 'scp' in opts:
#                for filename, items in scplist.iteritems():
#                    print 'Transfer of %s on %s@%s' % (filename, items[0], items[1])
#                    os.system('scp -q %s %s@%s:.ssh/' % (filename, items[0], items[1]))
#
        return True


class ScpDispatcher(object):
    def process(self, perm, memb):
        args = eval((memb.args in (None, '')) and '{}' or memb.args)
        f = file('authorized_keys_%s_%s' % (perm.login % args, perm.server.server))
        if perm.command is None:
            print ('%s %s' % (memb.key.key_value, memb.key.key_name)).strip()
        else:
            print ('%s %s %s' % (perm.command % args, memb.key.key_value, memb.key.key_name)).strip()


class StdoutDispatcher(object):
    def process(self, perm, memb):
        if perm.command is None:
            print ('%s %s' % (memb.key.key_value, memb.key.key_name)).strip()
        else:
            args = eval((memb.args in (None, '')) and '{}' or memb.args)
            print ('%s %s %s' % (perm.command % args, memb.key.key_value, memb.key.key_name)).strip()

    def reset(self):
        pass


class GeneratorController(Controller):
    def parse(self, *args, **opts):
        rolelist = []
        srvlst = None

        if 'group' in opts:
            grp = ServerGroup.get_by(server_group=opts['group'])
            if grp is None:
                return False
            srvlst = grp.servers

        if 'server' in opts:
            srv = Server.get_by(server=opts['server'])
            if srv is None:
                return False
            srvlst = [srv]
            grp = srv.server_group

        if srvlst is None:
            print 'Error: specify either group or server argument.'
            return False

        if 'login' not in opts and 'role' not in opts:
            print 'Error: specify either login or role argument.'
            return False

        if 'role' in opts:
            role = Role.get_by(role=opts['role'])
            lst = Permission.query.filter_by(role=role).all()
            loginlist = []
            for perm in lst:
                if perm.login not in loginlist:
                    loginlist.append(perm.login)
        else:
            loginlist = [opts['login']]

        permlist = []
        memblist = []
        for login in loginlist:
            lst = Permission.query.filter_by(login=login).all()

            for perm in lst:
                if perm.server in srvlst:
                    permlist.append(perm)
                    if perm.role not in rolelist:
                        rolelist.append(perm.role)

        lst = Membership.query.filter_by(server_group=grp)
        for memb in lst:
            if memb.role in rolelist:
                memblist.append(memb)

        self._memblist = memblist
        self._permlist = permlist
        self._group = grp
        self._loginlist = loginlist
        self._serverlist = srvlst

        return True

    def openssh(self, *args, **opts):
        if len(args) > 0:
            return False

        output = StdoutDispatcher()

        if not self.parse(*args, **opts):
            sys.exit(1)

        if 'output' in opts:
            output = FileOutput(opts['output'])

        output.reset()

        outputsrvlst = []
        for srv in self._serverlist:
            for perm in self._permlist:
                if perm.server != srv:
                    continue
                for memb in self._memblist:
                    args = eval((memb.args in (None, '')) and '{}' or memb.args)
                    login = perm.login % args
                    if memb.role == perm.role and memb.user.location == perm.location:
                        if (login, perm.server.server) not in outputsrvlst:
                            outputsrvlst.append((login, perm.server.server))
                        output.process(perm, memb)

        return outputsrvlst

    openssh.usage = {
        'shortdesc': 'Generate authorization file',
        'usage': ['%(exec)s generate openssh [--server=<server>] [--group=<group>] [--role=<role>] [--login=<login>] [--output=<filepath_prefix>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'server=': 'filters by server name (SHOULD DISAPPEAR)',
            'group=': 'filters by server group name',
            'role=': 'filters by role name',
            'login=': 'filters by login name',
            #'scp': 'transfers authorized_keys files to the appropriate login/server',
            'output=': 'outputs to file instead of standard output',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:'}
    }

    usage = {
        'command': ['generate', 'gen'],
        'shortdesc': 'Generate authorization file',
    }


class FileOutput(object):
    def __init__(self, prefix=None):
        self._prefix = prefix

    def reset(self):
        self._filelist = []

    def process(self, perm, memb):
        args = eval((memb.args in (None, '')) and '{}' or memb.args)
        filename = self._prefix + '_%s_%s' % (perm.login % args, perm.server.server)
        if filename not in self._filelist:
            self._filelist.append(filename)
            if os.path.exists(filename):
                os.remove(filename)

        f = file(filename, 'a')

        try:
            if perm.command is None:
                print >>f, ('%s %s' % (memb.key.key_value, memb.key.key_name)).strip()
            else:
                print >>f, ('%s %s %s' % (perm.command % args, memb.key.key_value, memb.key.key_name)).strip()

        except:
            print "ERROR with: ", perm, memb
            print repr(perm.command)
            print repr(args)
            print repr(memb.key.key_value)
            print repr(memb.key.key_name)

GeneratorController()

if __name__ == '__main__':
    c = GeneratorController()
    c.list()
