%define dirname ssh-keydb
%define name python-ssh-keydb
%define version 1.0
%define unmangled_version 1.0
%define release 1

Summary: OpenSSH public key management tool
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPLv3
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}

Requires:       python-elixir >= 0.7.1
Requires:       python-sqlalchemy == 0.7.9
Requires:       python-pysqlite >= 2.5
Requires:       python-skeletool >= 1.0
Requires:       apache
Requires:       git

BuildRequires:  python-setuptools
BuildArch: noarch

Vendor: Fabien Bouleau <fabien.bouleau@gmail.com>
Url: http://code.google.com/p/ssh-keydb/

%description
The ssh-keydb project goal is to provide a way to easily manage the
authorized_keys files containing the OpenSSH public keys used for key-pair
authentication. Assuming the keys are managed per-user, it is then possible to
define roles and memberships on groups of machines for each individual. 

This package provides the server part of ssh-keydb.

%prep
%setup -n %{dirname}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --single-version-externally-managed --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%post
cp -r ssh-keydb-www $RPM_BUILD_ROOT/var/www/
cp ssh-keydb.conf $RPM_BUILD_ROOT/etc/apache2/mods-enabled/ssh-keydb.conf
/sbin/service apache2 reload

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc GPL 

%changelog
* Thu Jul 09 2013 Fabien Bouleau <fabien.bouleau@gmail.com> 1.0
- Initial Package
