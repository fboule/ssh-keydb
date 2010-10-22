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

from new import instancemethod
from container import Container

class Controllers(Container):
    def command(self, commandid):
        for controller in self._items:
            if 'usage' not in dir(controller):
                continue

            if commandid in controller.usage['command']:
                return self._items[controller]

        return None

class Controller(object):
    @staticmethod
    def __new__(cls):
        if cls is Controller:
            raise TypeError('Cannot directly instanciate ' + repr(cls))

        if '_instance' not in dir(cls):
            cls._instance = super(Controller, cls).__new__(cls)
            Controllers().set(cls._instance)
        
        return cls._instance

    def actions(self):
        lst = []
        for methodname in dir(self):
            method = eval('self.' + methodname)
            if isinstance(method, instancemethod) and not methodname.startswith('_'):
                lst.append(method)
        return lst

    def default(self, *kargs, **kwargs):
        return None
