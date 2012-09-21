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

from elixir import *
import os.path


def dbinit(**opts):
    DATABASEPATH = opts.get('dbpath', os.path.expanduser('~/.ssh-keydb.db'))
    if os.path.isdir(DATABASEPATH):
        DATABASEPATH = DATABASEPATH + os.sep + '.ssh-keydb.db'
    db = opts.get('db', DATABASEPATH)
    metadata.bind = "sqlite:///" + db
    #print metadata.bind
    #metadata.bind.echo = True
    setup_all(True)


class Location(Entity):
    using_options(tablename='location')

    location = Field(Text, primary_key=True)
    users = OneToMany('User')
    permissions = OneToMany('Permission')

    def __repr__(self):
        return "<location>%s</location>" % self.location

    def __str__(self):
        return self.location


class User(Entity):
    using_options(tablename='user')

    user = Field(Text, primary_key=True)
    location = ManyToOne('Location')
    keys = OneToMany('Key')
    memberships = OneToMany('Membership')

    def __repr__(self):
        location = ''
        if self.location is not None:
            location = " location='%s'" % str(self.location)
        s = "<user%s>%s</user>" % (location, self.user)
        return s

    def __str__(self):
        return self.user


class Key(Entity):
    using_options(tablename='key')

    key_name = Field(Text, primary_key=True)
    user = ManyToOne('User', column_kwargs={'primary_key': True})
    key_type = ManyToOne('KeyType')
    key_value = Field(Text)
    memberships = OneToMany('Membership')

    def __repr__(self):
        s = "<key>"
        s += '<name>%s</name>' % self.key_name
        if self.key_type is not None:
            s += repr(self.key_type)
        if self.key_value is not None:
            s += '<public>%s</public>' % self.key_value
        return s + "</key>"

    def __str__(self):
        return self.key_name


class KeyType(Entity):
    using_options(tablename='keytype')

    key_type = Field(Text, primary_key=True)
    keys = OneToMany('Key')

    def __repr__(self):
        return "<type>%s</type>" % self.key_type

    def __str__(self):
        return self.key_type


class Server(Entity):
    using_options(tablename='server')

    server = Field(Text, primary_key=True)
    fqdn = Field(Text)
    server_group = ManyToOne('ServerGroup')
    permissions = OneToMany('Permission')
    hostkeys = OneToMany('ServerHostKey')

    def __repr__(self):
        if len(self.hostkeys) > 0:
            s = "<server name='%s'>" % self.server
            s += ''.join([repr(key) for key in self.hostkeys])
            s += "</server>"
        else:
            s = "<server name='%s' />" % self.server
        return s

    def __str__(self):
        return self.server


class ServerHostKey(Entity):
    using_options(tablename='serverhostkey')

    filename = Field(Text, primary_key=True)
    server = ManyToOne('Server', column_kwargs={'primary_key': True})
    private_key = Field(Text)
    public_key = Field(Text)

    def __repr__(self):
        s = "<key name='%s'>" % self.filename
        if self.private_key is not None:
            s += '<private>%s</private>' % self.private_key
        if self.public_key is not None:
            s += '<public>%s</public>' % self.public_key
        return s + "</key>"

    def __str__(self):
        return self.filename


class ServerGroup(Entity):
    using_options(tablename='servergroup')

    server_group = Field(Text, primary_key=True)
    servers = OneToMany('Server')
    memberships = OneToMany('Membership')

    def __repr__(self):
        if len(self.servers) > 0:
            s = "<servergroup name='%s'>" % self.server_group
            s += ''.join([repr(server) for server in self.servers])
            s += "</servergroup>"
        return s

    def __str__(self):
        return self.server_group


class Role(Entity):
    using_options(tablename='role')

    role = Field(Text, primary_key=True)
    memberships = OneToMany('Membership')
    permissions = OneToMany('Permission')

    def __repr__(self):
        return "<role>%s</role>" % self.role

    def __str__(self):
        return self.role


class Membership(Entity):
    using_options(tablename='membership')

    user = ManyToOne('User', column_kwargs={'primary_key': True})
    key = ManyToOne('Key', column_kwargs={'primary_key': True})
    server_group = ManyToOne('ServerGroup', column_kwargs={'primary_key': True})
    role = ManyToOne('Role', column_kwargs={'primary_key': True})
    args = Field(Text)

    def __repr__(self):
        s = "<membership>"
        s += repr(self.user) + repr(self.key) + repr(self.server_group) + repr(self.role)
        s += '<args>%s</args>' % self.args
        s += "</membership>"
        return s


class Permission(Entity):
    using_options(tablename='permission')

    role = ManyToOne('Role', column_kwargs={'primary_key': True})
    server = ManyToOne('Server', column_kwargs={'primary_key': True})
    location = ManyToOne('Location', column_kwargs={'primary_key': True})
    login = Field(Text, primary_key=True)
    command = Field(Text)

    def __repr__(self):
        s = "<permission>"
        s += repr(self.role) + repr(self.server) + repr(self.location)
        s += '<login>%s</login>' % self.login
        s += '<command>%s</command>' % self.command
        s += "</permission>"
        return s
