Summary:       Installation package for the client part of ssh-keydb.
Name:          python-ssh-keydb-client
Version:       1.0
Release:       1%{?dist}

License:       GPLv3+
Group:         System Environment/Base

URL:           https://gitorious.org/ssh-keydb
Source0:       GPL
Source1:       gitconfig

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires(pre): shadow-utils
Requires(pre): git
Requires:      redhat-release >=  %{version} 

%description
The ssh-keydb project goal is to provide a way to easily manage the
authorized_keys files containing the OpenSSH public keys used for key-pair
authentication. Assuming the keys are managed per-user, it is then possible to
define roles and memberships on groups of machines for each individual. 

This package provides the server part of ssh-keydb.

%prep
%setup -q -c -T

%build

%install
install -pm 644 %{SOURCE0} .
install -pm 644 %{SOURCE1} .

%post
mkdir -p %{_sysconfdir}/ssh/auth

if ! getent passwd keymgr >/dev/null ; then
    useradd -m  -c "ssh-keydb key management account." keymgr
fi
mkdir -p /home/keymgr/
cp %{SOURCE2} /home/keymgr/.gitconfig
rm -rf 

tempname=$( mktemp )

sed "s/^AuthorizedKeysFile/#AuthorizedKeysFile/g" /etc/ssh/sshd_config >$tempname.1
nline=$( grep -n AuthorizedKeysFile $tempname.1 | head -n 1 | cut -f 1 -d ':' )
head -n $nline $tempname.1 >$tempname
echo "AuthorizedKeysFile /etc/ssh/auth/authorized_keys_%u" >>$tempname
tail -n +$[ $nline + 1 ] $tempname.1 >>$tempname
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.old
mv $tempname /etc/ssh/sshd_config
rm $tempname.1

cd /home

ls -1 | while read d
do
    [ ! -e "$d/.ssh/authorized_keys" ] && continue
    cp -v "$d/.ssh/authorized_keys" /etc/ssh/auth/authorized_keys_$d
done

cd /home/keymgr
git init --bare keystore.git

cd /etc/ssh/auth
git init
git remote add origin /home/keymgr/keystore.git
git add .
git commit -m 'Initial import'
git push origin master
git branch --set-upstream master origin/master

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL 

%changelog
* Thu Jun 20 2013 Fabien Bouleau <fabien.bouleau@gmail.com> 1.0
- Initial Package
