#!/usr/bin/env python

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
from options import *
from plugins.model import *
from plugins import *

class MainApp(object):
    def run(self):
        helpctrl = HelpController()
        optsctrl = OptionsController()

        opts, args = optsctrl.parse(sys.argv)

        try:
            action = optsctrl.action(args)
        except SyntaxError, ex:
            if ex.msg is not None:
                print ex
                print
            action = None

        if action is None:
            helpctrl.help()
            sys.exit(2)
        elif 'h' in opts or 'help' in opts or len(args) < 2:
            helpctrl.help(args[0])
            sys.exit(2)

        dbinit(**opts)

        try:
            action(*args[2:], **opts)
        except SyntaxError, ex:
            helpctrl.help(args[0])
            sys.exit(2)

def run():
    MainApp().run()

if __name__ == '__main__':
    run()

