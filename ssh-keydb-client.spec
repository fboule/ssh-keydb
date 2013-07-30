Summary:       Installation package for the client part of ssh-keydb.
Name:          ssh-keydb-client
%define version 1.0
%define unmangled_version 1.0
%define release 1

Version:       %{version}
Release:       %{release}

License:       GPLv3+
Group:         System Environment/Base

URL:           http://tbd.com
Source0:       GPL
Source1:       ssh-keydb-client-setup
Source2:       gitconfig

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:     noarch
Requires(pre): shadow-utils
Requires(pre): git
Requires:      redhat-release >=  %{version} 

%description
Installation package for the client part of ssh-keydb.

%prep
%setup -q -c -T
install -pm 644 %{SOURCE0} .
install -pm 755 %{SOURCE1} .
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ssh/auth
if ! getent passwd keymgr >/dev/null ; then
    useradd -m  -c "ssh-keydb key management account." keymgr
fi
mkdir -p $RPM_BUILD_ROOT/home/keymgr/
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT/home/keymgr/.gitconfig

%build

%install
rm -rf %{buildroot}
%{SOURCE1} $RPM_BUILD_ROOT

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc GPL ssh-keydb-client-setup

%changelog
* Thu Jun 20 2013 Fabien Bouleau <fabien.bouleau@ses.com> 1.0
- Initial Package
