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
from user import UserController

__all__ = ['DiscoveryController']

class DiscoveryController(Controller):
    def parse(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        location = opts.get('location', None)

        if len(args) or None in (location, ):
            raise SyntaxError()

        usercount = 0

        for line in sys.stdin.readlines():
            items = line.split(' ')
            keyname = items[-1].strip()
            key = ' '.join(items[-3:-1]).strip()
            command = ' '.join(items[:-3])

            keylist = Key.query.filter_by(key_name=keyname)

            if len(keylist.all()) == 0:
                self._adduser(key, keyname, opts)
                usercount += 1

        print 'Added %i keys/users' % usercount

    def _adduser(self, key, keyname, opts):
        keystring = key + ' ' + keyname
        if 'verbose' in opts or 'long' in opts:
            if 'long' in opts:
                print 'Adding %s/%s => ...%s' % (keyname, str(location), key[-20:])
            else:
                print 'Adding %s' % keyname
        UserController().set(keyname, location, keystring = keystring)

    parse.usage = {
        'shortdesc': 'Parse an authorized_keys file for public keys from the standard input',
        'usage': ['%(exec)s discover parse --location=<location>'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'location=': 'location to assign (None by default)',
            'verbose': 'shows what is being added',
            'long': 'shows what is being added with the public keys',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', 'verbose': 'v', 'long': 'l', }
    }

    usage = {
        'command': ['discover'],
        'shortdesc': 'Public key discovery',
    }

DiscoveryController()

if __name__ == '__main__':
    c = DiscoveryController()
    c.list()
