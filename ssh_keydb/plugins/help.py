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

from skeletool.controller import *

__all__ = ['HelpController']


class HelpController(Controller):
    def default(self, *kargs, **kwargs):
        return self.help(*kargs, **kwargs)

    def help(self, *kargs, **kwargs):
        if 'intro' in kwargs:
            print(self.intro())
        elif len(kargs) == 0:
            print(self._global_usage())
        else:
            print(self._command_usage(*kargs, **kwargs))

    def _global_usage(self):
        s = 'Usage: %s [command] [options] [args]\n\n' % self.app
        s = s + 'Available commands:\n'

        lst = {}
        n = 0
        for controllerid in Controllers().all():
            controller = Controllers().get(controllerid)

            if 'usage' not in dir(controller):
                continue

            cmdlst = controller.usage['command']
            shortdesc = controller.usage['shortdesc']

            cmd = '  %s' % cmdlst[0]
            if len(cmdlst) > 1:
                cmd = cmd + ' ('
                for alt in cmdlst[1:]:
                    cmd = cmd + alt
                    if alt != cmdlst[-1]:
                        cmd = cmd + ', '
                cmd = cmd + ')'

            lst[cmd] = shortdesc
            if len(cmd) > n:
                n = len(cmd)

        for cmd in lst:
            fmt = '%-' + str(n) + 's : %s\n'
            s = s + fmt % (cmd, lst[cmd])

        s = s + '\nBy default the command help is used.'

        return s

    def _command_usage(self, *kargs, **kwargs):
        commandid = kargs[0]
        controller = Controllers().command(commandid)
        shortdesc = controller.usage['shortdesc']
        longdesc = '\n  '.join(controller.usage.get('longdesc', ''))

        commandids = controller.usage['command']
        line = commandids[0]

        if len(commandids) > 1:
            line = line + ' ('
            for cmd in commandids[1:]:
                line = line + cmd
                if cmd != commandids[-1]:
                    line = line + ', '
            line = line + ')'

        s = '%s: %s\n\n' % (line, shortdesc)
        hdr = 'Usage: '
        n = len(hdr)

        for method in controller.actions():
            if 'usage' not in dir(method):
                continue
            fmt = '%' + str(n) + 's%s\n'
            for usage in method.usage['usage']:
                line = fmt % (hdr, usage)
                s = s + line % {'exec': self.app}
                hdr = ''

        if longdesc != '':
            s = s + '\n  ' + longdesc + '\n'
        s = s + '\nValid options:\n'

        options = {}
        n = 0

        for command in controller.actions():
            if 'usage' not in dir(command):
                continue
            for longoptitem in command.usage['options']:
                longopt = longoptitem.strip('=')
                line = '--' + longopt
                if longopt in command.usage['shortopts']:
                    line = '-' + command.usage['shortopts'][longopt].rstrip(':') + ' [--' + longopt + ']'
                    options[longopt] = (line, command.usage['options'][longoptitem])
                else:
                    options[longopt] = (line, command.usage['options'][longoptitem])
                n = max(len(line) + 1, n)

        for longopt in options:
            fmt = '  %-' + str(n) + 's: %s\n'
            s = s + fmt % options[longopt]

        return s

    def intro(self, *kargs, **kwargs):
        return 'intro'

    app = 'ssh-keydb'

    usage = {
        'command': ['help'],
        'shortdesc': 'Help',
    }

    help.usage = {
        'shortdesc': 'Help',
        'usage': ['%(exec)s help [<options>]'],
        'options': {
            'intro': 'displays short introduction',
            'help': 'displays help on help',
            'dbpath=': 'database path (~/.ssh-keydb.db by default)',
        },
        'shortopts': {'help': 'h', 'dbpath': 'd:', }
    }

HelpController()

if __name__ == '__main__':
    c = HelpController()
    c.help()
