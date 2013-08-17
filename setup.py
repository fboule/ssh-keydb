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

from setuptools import setup, find_packages
setup(
    name="ssh-keydb-server",
    version="1.0",
    packages=find_packages(),

    # Dependencies
    install_requires=['SQLAlchemy==0.7.9', 'elixir>=0.7.1', 'pysqlite>=2.5', 'skeletool>=1.0'],

    package_data={
        '': ['GPL', 'COPYING', "*.txt", 'ssh-keydb-www', 'ssh-keydb.conf' ],
    },

    entry_points={
        'console_scripts': [
            'ssh-keydb = ssh_keydb.ssh_keydb:run',
        ],
    },

    # Metadata
    author='Fabien Bouleau',
    author_email='fabien.bouleau@gmail.com',
    description='OpenSSH public key management tool',
    license='GPLv3',
    keywords='openssh public key management tool',
    url='http://code.google.com/p/ssh-keydb/',
)
