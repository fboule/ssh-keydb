#!/usr/bin/env python

import sys, os, os.path
import cgi
import cgitb

from subprocess import Popen, PIPE, STDOUT

try:
    from sshkeydb import *
except:
    os.chdir(os.pardir)
    sys.path.append(os.getcwd())
    from sshkeydb import *

class MainApp(object):
    def run(self):
        cgitb.enable()
        form = cgi.FieldStorage()

        self.page = 'main'
        if form.has_key('page'):
            self.page = form['page'].value

        chars = self.__getattribute__(self.page)(form)

        contentsxml = ''
        for node in chars:
            if isinstance(chars[node], Entity):
                contentsxml += '    %s' % repr(chars[node])
            elif isinstance(chars[node], str):
                contentsxml += '    %s' % chars[node]
            elif chars[node] is None:
                contentsxml += '    <%s>None</%s>' % (node, node)
            else:
                contentsxml += '<%s>' % node
                contentsxml += ''.join([ repr(item) for item in chars[node] ])
                contentsxml += '</%s>' % node

        contents = file('www/' + self.page + '.xml').read()
        contents = contents.replace('__CONTENTS__', contentsxml)

        print 'Content-Type: text/xml\n'
        print contents

    def main(self, form):
        return {}

    def users(self, form):
        if form.has_key('submit'):
            name = form.has_key('addname') and form['addname'].value or None
            location = form.has_key('addlocation') and form['addlocation'].value or None
            section = form.has_key('addsection') and form['addsection'].value or None
            UserController().set(name, location, section)

        for k in form.keys():
            if k.startswith('del_user'):
                v = k.split('_')[2:]
                UserController().remove(user = v[0], location = v[1])

        chars = {}
        chars['location'] = None
        chars['section'] = None

        flt = {}

        if form.has_key('location'): 
            chars['location'] = form['location'].value
            flt['location'] = chars['location']
        if form.has_key('section'): 
            chars['section'] = form['section'].value
            flt['section'] = chars['section']

        users = UserController().filter(**flt)

        chars['all_locations'] = LocationController().filter()
        chars['users'] = users

        return chars

    def user(self, form):
        chars = {}
        errors = []
        formkeys = form.keys()
        if 'add_key' in formkeys:
            KeyController().set(form['user'].value, 'keystring', form['keystring'].value)

        if 'add_membership' in formkeys:
            args = ''
            if form.has_key('args'): args = form['args'].value
            MembershipController().grant(
                    form['user'].value, form['key'].value, form['role'].value, 
                    form['group'].value, args)

        for k in formkeys:
            if k.startswith('del_membership'):
                v = k.split('_')[2:]
                MembershipController().revoke(user = form['user'].value, key = v[2], role = v[1], group = v[0])
            if k.startswith('del_key'):
                v = k.split('_')[2:]
                membdata = MembershipController().filter(user = form['user'].value, key = v[0])
                if len(membdata) > 0:
                    for m in membdata:
                        errors.append((m.server_group.server_group, m.role.role, v[0]))
                else:
                    KeyController().remove(user = form['user'].value, key = v[0])

        chars = ProfileController().get(user = form['user'].value)
        user = chars['userlist'][0]
        del chars['userlist']
        chars['errors'] = errors
        chars['all_groups'] = ServerGroupController().filter()
        chars['all_roles'] = RoleController().filter()
        chars['all_keys'] = user.keys
        chars['user'] = repr(user)
        chars['keys'] = user.keys
        chars['memberships'] = user.memberships
        chars['permissions'] = chars['users'][user]['permissions']
        chars['groups'] = chars['users'][user]['groups']

        return chars

    def servers(self, form):
        formkeys = form.keys()
        if 'add_group' in formkeys:
            ServerGroupController().set(form['group'].value, *form['servers'].value.split(' '))
        if 'add_role' in formkeys:
            RoleController().set(form['role'].value)
        if 'add_permission' in formkeys:
            PermissionController().set(form['role'].value, form['login'].value, form['location'].value, 
                    form['server'].value, form['command'].value)
        for k in formkeys:
            if k.startswith('del_role'):
                v = k.split('_')[2:]
                RoleController().remove(role = v[0])
            if k.startswith('del_group'):
                v = k.split('_')[2:]
                ServerGroupController().remove(group = v[0])
            if k.startswith('del_perm'):
                v = k.split('_')[2:]
                PermissionController().remove(server = v[1], role = v[2], login = v[0], location = v[3])
        chars = {}
        chars['all_groups'] = ServerGroupController().filter()
        chars['all_servers'] = ServerController().filter()
        chars['all_roles'] = RoleController().filter()
        chars['all_permissions'] = PermissionController().filter()
        chars['all_locations'] = LocationController().filter()
        return chars

    def hostkey(self, form):
        chars = {}
        chars['updated'] = []
        chars['error'] = []
        if 'hostkey_push' in form.keys():
            servername = form['server'].value
            srv = Server.get_by(server = servername)
            fqdn = srv.fqdn
            for h in srv.hostkeys:
                cmd = 'ssh root@%(fqdn)s "echo \'%(key)s\' >%(name)s"' % { 'fqdn': fqdn, 'key': h.privkey, 'name': h.filename }
                try:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                except:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                cmd = 'ssh root@%(fqdn)s "echo \'%(key)s\' >%(name)s.pub"' % { 'fqdn': fqdn, 'key': h.pubkey, 'name': h.filename }
                try:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                except:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                chars['updated'].append((srv.server, h.filename))
            if len(srv.hostkeys) == 0:
                chars['error'].append(('Error on %s' % srv.server, "Nothing to update."))
        if 'hostkey_pull' in form.keys():
            servername = form['server'].value
            srv = Server.get_by(server = servername)
            fqdn = srv.fqdn
            for privkeyfile in [ 'ssh_host_key', 'ssh_host_rsa_key', 'ssh_host_dsa_key' ]:
                pubkeyfile = privkeyfile + '.pub'
                if os.path.exists(privkeyfile): os.remove(privkeyfile)
                if os.path.exists(pubkeyfile): os.remove(pubkeyfile)

                cmd = 'scp root@%(fqdn)s:/etc/%(name)s .' % { 'fqdn': fqdn, 'name': privkeyfile }
                try:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                except:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                res = p.stdout.read()
                chars['error'].append(('Error on server %(server)s file %(name)s' % { 'server': servername, 'name': privkeyfile }, 
                            res.strip()))

                cmd = 'scp root@%(fqdn)s:/etc/%(name)s .' % { 'fqdn': fqdn, 'name': pubkeyfile }
                try:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
                except:
                    p = Popen(cmd, shell=True, bufsize=512, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                res = p.stdout.read()
                chars['error'].append(('Error on server %(server)s file %(name)s' % { 'server': servername, 'name': pubkeyfile }, 
                            res.strip()))

                if os.path.exists(privkeyfile):
                    privkey = file(privkeyfile).read()
                    ServerController().key(servername, privkeyfile, 'privkey', privkey)
                    chars['updated'].append(privkeyfile)

                if os.path.exists(pubkeyfile):
                    pubkey = file(pubkeyfile).read()
                    ServerController().key(servername, privkeyfile, 'pubkey', pubkey)
                    chars['updated'].append(pubkeyfile)
        chars['all_servers'] = ServerController().filter()
        return chars

    def apply(self, form):
        chars = {}
        chars['updated'] = []
        if 'apply' in form.keys():
            lst = GeneratorController().openssh(group = form['group'].value, role = form['role'].value, output = 'keys/new')
            chars['updated'] = lst
            for item in lst:
                server = Server.get_by(server = item[1])
                data = { 'login': item[0], 'server': server.server, 'fqdn': server.fqdn }
                data['filename'] = 'new_%s_%s' % (data['login'], data['server'])
                cmd = 'scp keys/new_%(login)s_%(server)s root@%(fqdn)s:' % data
                res = os.popen(cmd)
                cmd = []
                cmd.append('mv ~%(login)s/.ssh/authorized_keys ~%(login)s/.ssh/authorized_keys.old' % data)
                cmd.append('mv %(filename)s ~%(login)s/.ssh/authorized_keys' % data)
                cmd.append('chmod 644 ~%(login)s/.ssh/authorized_keys' % data)
                cmd.append('chown %(login)s ~%(login)s/.ssh/authorized_keys' % data)
                cmd = ('ssh root@%(fqdn)s "' % data) + '\n'.join(cmd) + '"'
                res = os.popen(cmd)
        chars['all_groups'] = ServerGroupController().filter()
        chars['all_servers'] = ServerController().filter()
        chars['all_roles'] = RoleController().filter()
        return chars

if __name__ == '__main__':
    MainApp().run()

