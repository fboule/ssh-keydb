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

metadata.bind = "sqlite:///db/db.db"
#metadata.bind.echo = True

class Location(Entity):
    location = Field(Text, primary_key = True)
    users = OneToMany('User')
    permissions = OneToMany('Permission')

    def __repr__(self):
        return "<Location '%s'>" % self.location

class User(Entity):
    user = Field(Text, primary_key = True)
    section = Field(Text)
    location = ManyToOne('Location')
    keys = OneToMany('Key')
    memberships = OneToMany('Membership')

    def __repr__(self):
        s = "<User '%s'" % self.user
        if self.section is not None:
            s = s + " '%s'" % self.section
        if self.location is not None:
            s = s + " %s" % repr(self.location)
        return s + '>'

class Key(Entity):
    key_name = Field(Text, primary_key = True)
    user = ManyToOne('User', column_kwargs={'primary_key': True})
    key_type = ManyToOne('KeyType')
    key_value = Field(Text)
    memberships = OneToMany('Membership')

    def __repr__(self):
        return "<Key '%s'>" % self.key_name

class KeyType(Entity):
    key_type = Field(Text, primary_key = True)
    keys = OneToMany('Key')

    def __repr__(self):
        return "<Type '%s'>" % self.key_type

class Server(Entity):
    server = Field(Text, primary_key = True)
    fqdn = Field(Text)
    server_group = ManyToOne('ServerGroup')
    permissions = OneToMany('Permission')
    hostkeys = OneToMany('ServerHostKey')

    def __repr__(self):
        if len(self.hostkeys) > 0:
            return "<Server '%s' %s>" % (self.server, ' '.join([ repr(h) for h in self.hostkeys]))
        else:
            return "<Server '%s'>" % self.server

class ServerHostKey(Entity):
    filename = Field(Text, primary_key = True)
    server = ManyToOne('Server', column_kwargs={'primary_key': True})
    private_key = Field(Text)
    public_key = Field(Text)

    def __repr__(self):
        s = "<ServerKey %s" % self.filename
        if self.private_key is not None: s += ', privkey'
        if self.public_key is not None: s += ', pubkey'
        return s + ">"

class ServerGroup(Entity):
    server_group = Field(Text, primary_key = True)
    servers = OneToMany('Server')
    memberships = OneToMany('Membership')

    def __repr__(self):
        return "<Group '%s' %s>" % (self.server_group, repr(self.servers))

class Role(Entity):
    role = Field(Text, primary_key = True)
    memberships = OneToMany('Membership')
    permissions = OneToMany('Permission')

    def __repr__(self):
        return "<Role '%s'>" % self.role

class Membership(Entity):
    user = ManyToOne('User', column_kwargs={'primary_key': True})
    key = ManyToOne('Key', column_kwargs={'primary_key': True})
    server_group = ManyToOne('ServerGroup', column_kwargs={'primary_key': True})
    role = ManyToOne('Role', column_kwargs={'primary_key': True})
    args = Field(Text)

    def __repr__(self):
        return "<Membership %s %s %s %s args='%s'>" % (repr(self.user), repr(self.key), repr(self.server_group), repr(self.role), self.args)

class Permission(Entity):
    role = ManyToOne('Role', column_kwargs={'primary_key': True})
    server = ManyToOne('Server', column_kwargs={'primary_key': True})
    location = ManyToOne('Location', column_kwargs={'primary_key': True})
    login = Field(Text, primary_key = True)
    command = Field(Text)

    def __repr__(self):
        return "<Permission %s %s login='%s' %s command='%s'>" % (repr(self.role), repr(self.server), self.login, repr(self.location), self.command)

setup_all(True)
