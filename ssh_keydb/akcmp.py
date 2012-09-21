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


def cmpline(line1, line2, i1, i2):
    items1 = line1.strip().rsplit(' ', 3)
    items2 = line2.strip().rsplit(' ', 3)

    if items1[-2] != items2[-2]:
        return False
    if line1 == line2:
        return True

    if items1[-1] != items2[-1]:
        print('L#%i/%i ' % (i1 + 1, i2 + 1) + items1[-1] + ' differ on label (%s vs %s)' % (items1[-1], items2[-1]))
    else:
        print('L#%i/%i ' % (i1 + 1, i2 + 1) + items1[-1] + ' differ on command')

    return True


def akcmp(file1, file2):
    txt1 = file(file1).readlines()
    txt2 = file(file2).readlines()

    print "\nLeft: %s, Right: %s" % (file1, file2)

    for i1 in range(len(txt1)):
        line1 = txt1[i1]
        items1 = line1.strip().rsplit(' ', 3)
        found = False
        for i2 in range(len(txt2)):
            line2 = txt2[i2]
            found |= cmpline(line1, line2, i1, i2)
        if not found:
            print('L#%i %s cannot be found' % (i1 + 1, items1[-1]))

file1 = sys.argv[1]
file2 = sys.argv[2]

if len(sys.argv) > 3:
    if sys.argv[3] == '-l':
        akcmp(file1, file2)
    else:
        akcmp(file2, file1)
else:
    akcmp(file1, file2)
    akcmp(file2, file1)
