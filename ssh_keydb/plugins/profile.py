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

from model import *
from skeletool.controller import Controller
from key import KeyController
from membership import MembershipController
from group import ServerGroupController
from permission import PermissionController

__all__ = ['ProfileController']


class ProfileController(Controller):
    def show(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        chars = self.get(*kargs, **kwargs)

        userlist = chars['userlist']

        if len(userlist) == 0:
            return

        for user in userlist:
            s = '%s/%s' % (user.user, user.location.location)
            print s

            self.showkeys(chars['users'][user])
            self.showmemb(chars['users'][user])
            self.showgroups(chars['users'][user])
            self.showperms(chars['users'][user])

    def get(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        res = {}
        userlist = self.filter(*kargs, **kwargs)
        res['userlist'] = userlist

        if len(res['userlist']) == 0:
            return

        res['users'] = {}

        for user in userlist:
            self._user = user

            res['users'][user] = {}

            res['users'][user]['keys'] = self.buildkeys(*kargs, **kwargs)
            res['users'][user]['memberships'] = self.buildmemb(*kargs, **kwargs)
            res['users'][user]['groups'] = self.buildgroups(*kargs, **kwargs)
            res['users'][user]['groupnames'] = self.buildgroupnames(*kargs, **kwargs)
            res['users'][user]['permissions'] = self.buildperms(*kargs, **kwargs)

        return res

    def buildgroupnames(self, *kargs, **kwargs):
        self._groupmap = {}

        for group in self._sglist:
            self._groupmap[group.server_group] = [server.server for server in group.servers]

        return self._groupmap

    def buildgroups(self, *kargs, **kwargs):
        self._sglist = []
        memblist = self._memblist
        sgctrl = ServerGroupController()

        for memb in memblist:
            sgname = memb.server_group.server_group
            sg = sgctrl.filter(group=sgname)[0]
            if sg not in self._sglist:
                self._sglist.append(sg)

        return self._sglist

    def buildperms(self, *kargs, **kwargs):
        memblist = self._memblist
        pctrl = PermissionController()
        user = self._user
        gperms = []

        for memb in memblist:
            permlist = Permission.query.filter_by(location=user.location, role=memb.role)
            for perm in permlist:
                if perm not in gperms and perm.server.server in self._groupmap[memb.server_group.server_group]:
                    gperms.append(perm)

        return gperms

    def buildmemb(self, *kargs, **kwargs):
        membctrl = MembershipController()
        memblist = membctrl.filter(*kargs, **kwargs)
        self._memblist = memblist
        return memblist

    def buildkeys(self, *kargs, **kwargs):
        keyctrl = KeyController()
        keylist = keyctrl.filter(*kargs, **kwargs)
        return keylist

    def showgroups(self, *kargs, **kwargs):
        print '\nGroups:'
        sglist = kargs[0]['groupnames']

        for sgname in sglist:
            srvs = ['    ' + x for x in sglist[sgname]]
            print '  ' + sgname + ': '
            print '\n'.join(srvs)

    def showperms(self, *kargs, **kwargs):
        print '\nPermissions:'
        gperms = kargs[0]['permissions']

        l1 = 0
        l2 = 0
        l3 = 0
        l4 = 0
        for perm in gperms:
            l1 = max(l1, len(perm.server.server))
            l2 = max(l2, len(perm.role.role))
            l3 = max(l3, len(perm.login))
            l4 = max(l4, len(perm.location.location))

        for perm in gperms:
            print ' ',
            print perm.server.server + ' ' * (l1 - len(perm.server.server)),
            print perm.role.role + ' ' * (l2 - len(perm.role.role)),
            print perm.login + ' ' * (l3 - len(perm.login)),
            print perm.location.location + ' ' * (l4 - len(perm.location.location)),
            if 'long' in kwargs:
                print perm.command,
            else:
                print perm.command[:80],
            print

    def showmemb(self, *kargs, **kwargs):
        print '\nMemberships:'
        memblist = kargs[0]['memberships']

        self._memblist = memblist

        l1 = 0
        l2 = 0
        l3 = 0
        for memb in memblist:
            l1 = max(l1, len(memb.key.key_name))
            l2 = max(l2, len(memb.server_group.server_group))
            l3 = max(l3, len(memb.role.role))

        prevsg = ''
        prevrole = ''
        for memb in memblist:
            sg = memb.server_group.server_group

            role = memb.role.role

            print ' ',
            print sg + ' ' * (l2 - len(sg)),
            print role + ' ' * (l3 - len(role)),
            print memb.key.key_name + ' ' * (l1 - len(memb.key.key_name)),
            print

    def showkeys(self, *kargs, **kwargs):
        print '\nKeys:'
        keylist = kargs[0]['keys']

        l = 0
        for key in keylist:
            l = max(l, len(key.key_name))

        for key in keylist:
            print '  ' + key.key_name, ' ' * (l - len(key.key_name)) + '...' + key.key_value[-80:]

    def filter(self, *kargs, **kwargs):
        if len(kargs) > 0:
            return None

        args = kargs
        opts = kwargs

        userlist = User.query.filter(None)

        if 'user' in opts:
            userlist = userlist.filter_by(user=opts['user'])

        return userlist.all()

    show.usage = {
        'shortdesc': 'Build reports',
        'usage': ['%(exec)s profile show [--user=<user>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'user=': 'filter by user',
            'long': 'long display',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'long': 'l'}
    }

    usage = {
        'command': ['profile'],
        'shortdesc': 'Show profile',
    }

ProfileController()

if __name__ == '__main__':
    c = ProfileController()
    c.build()
