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

__all__ = ['KeyController']


class KeyController(Controller):
    def get(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs

        lst = self.filter(*kargs, **kwargs)

        if len(lst) == 0:
            return

        hdr = {'key_id': 'key_id', 'key': 'key'}

        for key in lst:
            print '%(key)s %(key_id)s' % {'key_id': key.key_name, 'key': key.key_value}

    def list(self, *kargs, **kwargs):
        args = kargs
        opts = kwargs
        lenvalue = 25

        lst = self.filter(*kargs, **kwargs)

        if len(lst) == 0:
            return

        hdr = {'key_id': 'key_id', 'key': 'key'}

        nl = {}
        for key in lst:
            nl['key_id'] = max(nl.get('key_id', len(hdr['key_id'])), len(key.key_name))
            nl['key'] = max(nl.get('key', len(hdr['key'])), lenvalue + 3)

        fmt = '%%(key_id)-%(key_id)is %%(key)-%(key)is' % nl
        n = sum(nl.values()) + 1

        print fmt % hdr
        print '-' * n

        for key in lst:
            print fmt % {'key_id': key.key_name, 'key': '...' + key.key_value[-lenvalue:]}

    def filter(self, *kargs, **kwargs):
        if len(kargs) > 0:
            return None

        opts = kwargs
        keylist = Key.query.filter(None)

        if 'key' in opts:
            keylist = keylist.filter_by(key_name=opts['key'])

        if 'type' in opts:
            keytype = KeyType.get_by(key_type=opts['type'])
            if keytype is None:
                return None
            keylist = keylist.filter_by(key_type=keytype)

        if 'user' in opts:
            user = User.get_by(user=opts['user'])
            if user is None:
                return None
            keylist = keylist.filter_by(user=user)

        return keylist.all()

    def set(self, *kargs, **kwargs):
        if len(kargs) != 3:
            raise SyntaxError()

        args = kargs

        username = args[0]
        cmd = args[1]
        cmdarg = args[2]

        if cmd not in ('keystring', 'keyfile'):
            return False

        user = User.get_by(user=username)

        if user is None:
            return False

        if cmd == 'keyfile':
            self.setkeyfile(user, cmdarg)
        if cmd == 'keystring':
            self.setkeystring(user, cmdarg)

        session.flush()
        session.commit()

        return True

    def setkeystring(self, user, keystring):
        items = keystring.split(' ', 2)

        keyname = items[2]
        ii = 0
        key = Key.get_by(key_name=keyname, user=user)

        while key is not None:
            keyname = items[2] + '.' + str(ii)
            key = Key.get_by(key_name=keyname, user=user)
            ii = ii + 1

        keytype = KeyType.get_by(key_type=items[0])

        if keytype is None:
            keytype = KeyType(key_type=items[0])

        key = Key(key_name=keyname, key_value=' '.join(items[0:2]), key_type=keytype, user=user)

        session.flush()
        session.commit()

        return True

    def setkeyfile(self, user, keyfile):
        keystring = file(keyfile).read().strip()
        return self.setkeystring(user, keystring)

    def remove(self, *kargs, **kwargs):
        keylist = self.filter(*kargs, **kwargs)
        n = len(keylist)

        if n > 2:
            ch = raw_input('Warning: remove all %i keys (Y/n)? ' % n)
            if ch != 'Y':
                print 'Cancelled.'
                sys.exit(1)

        for key in keylist:
            key.delete()

        session.flush()
        session.commit()

    get.usage = {
        'shortdesc': 'Manage keys',
        'usage': ['%(exec)s key get [--user=<user>] [--key=<key>] [--type=<type>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'user=': 'filter by user',
            'key=': 'filter by key',
            'type=': 'filter by type',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    list.usage = {
        'shortdesc': 'Manage keys',
        'usage': ['%(exec)s key list [--user=<user>] [--key=<key>] [--type=<type>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'user=': 'filter by user',
            'key=': 'filter by key',
            'type=': 'filter by type',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    set.usage = {
        'shortdesc': 'Manage keys',
        'usage': [
            '%(exec)s key set <user> keystring "<string>"',
            '%(exec)s key set <user> keyfile <keyfile>'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    remove.usage = {
        'shortdesc': 'Manage keys',
        'usage': ['%(exec)s key remove [--user=<user>] [--key=<key>]'],
        'options': {
            'help': 'displays the current help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
            'user=': 'filter by user',
            'key=': 'filter by key',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

    usage = {
        'command': ['key'],
        'shortdesc': 'Manage keys',
    }

KeyController()

if __name__ == '__main__':
    c = KeyController()
    c.list()
