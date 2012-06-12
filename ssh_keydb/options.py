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
import getopt
from plugins.help import HelpController
from plugins.controller import *

class OptionsController(Controller):
    _g_shortopts = ''
    _g_longopts = ''

    def options(self, *kargs, **kwargs):
        commandids = []
        shortopts = set()
        longopts = set()
        mapping = {}

        shortopts.add(self._g_shortopts)
        longopts.add(self._g_longopts)

        commands = Controllers().all()

        if len(kargs) > 0:
            commands = [ kargs[0].__class__ ]

        for controllerid in commands:
            controller = Controllers().get(controllerid)

            if 'usage' not in dir(controller):
                continue

            commandids.extend(controller.usage['command'])

            for method in controller.actions():
                if 'usage' not in dir(method):
                    continue

                for longopt in method.usage['shortopts']:
                    shortopt = method.usage['shortopts'][longopt]
                    shortopts.add(shortopt)
                    mapping[shortopt] = longopt

                for longopt in method.usage['options']:
                    longopts.add(longopt)

        return (longopts, shortopts, mapping)

    def parse(self, argv):
        longopts, shortopts, mapping = self.options()

        try:
            opts, args = getopt.gnu_getopt(argv[1:], ''.join(shortopts), longopts)
        except getopt.GetoptError, err:
            print(str(err))
            print
            HelpController().help()
            sys.exit(2)

        dictopts = {}
        for k, v in opts:
            if k.startswith('--'):
                dictopts[k.lstrip('-')] = v
            else:
                kk = k.lstrip('-')
                if kk in mapping:
                    dictopts[mapping[kk]] = v
                else:
                    dictopts[mapping[kk + ':']] = v

        return (dictopts, args)
        
    def action(self, args):
        if len(args) == 0:
            raise SyntaxError()

        controller = Controllers().command(args[0])

        if controller is None: 
            raise SyntaxError('command %s not recognized' % args[0])

        if len(args) > 1:
            action = None
            for method in controller.actions():
                if args[1] == method.__name__: action = method
            if action is None:
                raise SyntaxError('Argument %s does not exist.' % args[1])
        else:
             action = controller.default

        return action

OptionsController()

if __name__ == '__main__':
    oc = OptionsController()
    print(oc.options())

