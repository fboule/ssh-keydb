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

%define name ssh-keydb-client
%define version 1.0
%define unmangled_version 1.0
%define release 4

Summary:       Installation package for the client part of ssh-keydb.
Name:          %{name}
Version:       %{version}
Release:       %{release}

License:       GPLv3+
Group:         System Environment/Base

Source0:       %{name}-%{unmangled_version}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:        %{_prefix}

BuildArch:     noarch
Requires(pre): shadow-utils
Requires(pre): git

Vendor:        Fabien Bouleau <fabien.bouleau@gmail.com>
Url:           http://code.google.com/p/ssh-keydb/

%description
The ssh-keydb project goal is to provide a way to easily manage the
authorized_keys files containing the OpenSSH public keys used for key-pair
authentication. Assuming the keys are managed per-user, it is then possible to
define roles and memberships on groups of machines for each individual. 

Installation package for the client part of ssh-keydb.

%prep
%setup -n %{name}-%{unmangled_version}

%pre
getent passwd keymgr >/dev/null || \
    %_sbindir/useradd -m  -c "ssh-keydb key management account." keymgr
exit 0

%install
%{__rm} -rf %{buildroot}
[ ! -e $RPM_BUILD_ROOT/home/keymgr ] && mkdir -p $RPM_BUILD_ROOT/home/keymgr
install -pm 644 gitconfig $RPM_BUILD_ROOT/home/keymgr/.gitconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ssh/auth

MYDIR=$PWD
tempname="$RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config.new"

if ! grep "^AuthorizedKeysFile /etc/ssh/auth/authorized_keys_%u$" /etc/ssh/sshd_config >/dev/null; 
then
    sed "s/^AuthorizedKeysFile/#AuthorizedKeysFile/g" /etc/ssh/sshd_config >$tempname
    echo "AuthorizedKeysFile /etc/ssh/auth/authorized_keys_%u" >>$tempname
else
    cp /etc/ssh/sshd_config $tempname
fi
    
cd $RPM_BUILD_ROOT/home

ls -1 | while read d
do
    [ ! -e "$d/.ssh/authorized_keys" ] && continue
    cp -v "$d/.ssh/authorized_keys" $RPM_BUILD_ROOT%{_sysconfdir}/ssh/auth/authorized_keys_$d
done

HOMEDIR=$RPM_BUILD_ROOT/home/keymgr
cd $HOMEDIR
mkdir keystore.git
cd keystore.git
git init --bare
cd ..
getent passwd keymgr >/dev/null && \
    chown -R keymgr:users keystore.git

cd $RPM_BUILD_ROOT%{_sysconfdir}/ssh/auth
git init
git remote add origin /home/keymgr/keystore.git
touch .gitkeep
git add .
git commit -m 'Initial import'

git config branch.master.remote origin
git config branch.master.merge refs/heads/master

[ ! -e $RPM_BUILD_ROOT/usr/local/bin ] && mkdir -p $RPM_BUILD_ROOT/usr/local/bin
install -pm 755 $MYDIR/ssh-keydb-cron $RPM_BUILD_ROOT/usr/local/bin
install -pm 755 $MYDIR/ssh-keydb-add-relay $RPM_BUILD_ROOT/usr/local/bin
install -pm 755 $MYDIR/ssh-keydb-post-update-relay $RPM_BUILD_ROOT/usr/local/bin

if ! crontab -l | grep "/usr/local/bin/ssh-keydb-cron" >/dev/null; 
then
    tmpfile=$( mktemp )
    crontab -l >$tmpfile
    echo "* * * * *   /usr/local/bin/ssh-keydb-cron" >>$tmpfile
    crontab $tmpfile
    rm $tmpfile
fi

%post
cd %{_sysconfdir}/ssh/auth
git push origin master

exit 0

%triggerin -- openssh
mv /etc/ssh/sshd_config.new /etc/ssh/sshd_config
/sbin/service sshd reload

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL
%config /etc/ssh/sshd_config.new
%config /etc/ssh/auth
%config /home/keymgr
%attr(755,keymgr,users) /home/keymgr
%config /usr/local/bin

%changelog
* Thu Jul 31 2013 Fabien Bouleau <fabien.bouleau@ses.com> 1.0
- Initial Package
