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

__all__ = ['RoleController']


class RoleController(Controller):
    def list(self, *kargs, **kwargs):
        if len(kargs) > 0:
            raise SyntaxError()

        lst = self.filter(*kargs, **kwargs)

        for item in lst:
            print item

    def filter(self, *args, **opts):
        if len(args) > 0:
            return None

        rolelist = Role.query.filter(None)

        if 'role' in opts:
            rolelist = rolelist.filter_by(role=opts['role'])

        return rolelist.all()

    def set(self, *args, **opts):
        if len(args) != 1:
            raise SyntaxError()

        rolename = args[0]

        role = Role.get_by(role=rolename)

        if role is None:
            role = Role(role=rolename)

        session.flush()
        session.commit()

        return True

    def remove(self, *kargs, **kwargs):
        rolelist = self.filter(*kargs, **kwargs)
        n = len(rolelist)

        if n > 2:
            print 'Warning: remove all %i roles?' % n
            sys.exit(1)

        for role in rolelist:
            role.delete()

        session.flush()
        session.commit()

        return True

    set.usage = {
        'shortdesc': 'Manage role',
        'usage': ['%(exec)s role set <role>'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    remove.usage = {
        'shortdesc': 'Manage role',
        'usage': ['%(exec)s role remove [--role=<role>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage role',
        'usage': ['%(exec)s role list [--role=<role>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'role=': 'filter by role name',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    usage = {
        'command': ['role'],
        'shortdesc': 'Manage role',
    }

RoleController()

if __name__ == '__main__':
    c = RoleController()
    c.list()
