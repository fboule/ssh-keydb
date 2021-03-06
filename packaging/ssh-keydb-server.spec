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

%define name ssh-keydb
%define pyname ssh-keydb
%define version 1.0
%define unmangled_version 1.0
%define release 4

Summary:        OpenSSH public key management tool
Name:           %{name}-server
Version:        %{version}
Release:        %{release}
Source0:        %{pyname}-server-%{unmangled_version}.tar.gz
License:        GPLv3
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix:         %{_prefix}

Requires:       python-elixir >= 0.7.1
Requires:       python-sqlalchemy == 0.7.9
Requires:       python-pysqlite >= 2.5
Requires:       python-skeletool >= 1.0
Requires:       python-setuptools
Requires:       apache
Requires:       git

BuildRequires:  python-setuptools
BuildArch:      noarch

Vendor:        Fabien Bouleau <fabien.bouleau@gmail.com>
Url:           http://code.google.com/p/ssh-keydb/

%description
The ssh-keydb project goal is to provide a way to easily manage the
authorized_keys files containing the OpenSSH public keys used for key-pair
authentication. Assuming the keys are managed per-user, it is then possible to
define roles and memberships on groups of machines for each individual. 

This package provides the server part of ssh-keydb.

%prep
%setup -n %{pyname}-server-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
install --directory %{buildroot}/srv/www
install --directory %{buildroot}/etc/apache2/conf.d
cp -vr ssh-keydb-www $RPM_BUILD_ROOT/srv/www/
cp -v ssh-keydb.conf $RPM_BUILD_ROOT/etc/apache2/conf.d/ssh-keydb.conf

%post
/sbin/service apache2 reload

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc GPL 
/srv/www/*
/etc/apache2/conf.d/ssh-keydb.conf

%changelog
* Thu Jul 09 2013 Fabien Bouleau <fabien.bouleau@gmail.com> 1.0
- Initial Package
