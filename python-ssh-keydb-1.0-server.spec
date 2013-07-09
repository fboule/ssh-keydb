Summary:        Installation package for the client part of ssh-keydb.
Name:           python-ssh-keydb-server
Version:        1.0
Release:        1%{?dist}

License:        GPLv3+
Group:          System Environment/Base

URL:            https://gitorious.org/ssh-keydb
Source0:	python-ssh-keydb-%{version}-server.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       redhat-release >=  %{version}
Requires:       python-elixir >= 0.7.1
Requires:       python-sqlalchemy == 0.7.8
Requires:       python-pysqlite >= 2.5
Requires:       python-skeletool >= 0.3
Requires:       apache
Requires:       git

BuildRequires:  python-setuptools
BuildArch:      noarch

%description
The ssh-keydb project goal is to provide a way to easily manage the
authorized_keys files containing the OpenSSH public keys used for key-pair
authentication. Assuming the keys are managed per-user, it is then possible to
define roles and memberships on groups of machines for each individual. 

This package provides the server part of ssh-keydb.

%prep
%setup -n ssh-keydb

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%post
# configure apache

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL 
%{python_sitelib}/*

%changelog
* Thu Jul 09 2013 Fabien Bouleau <fabien.bouleau@gmail.com> 1.0
- Initial Package
