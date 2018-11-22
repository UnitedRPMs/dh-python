%global __jar_repack 0
%global date_source 20180927

Name:           dh-python
Version:        3
Release:        1%{?dist}
Summary:        debhelper add-on to to handle python 3 files after build

BuildArch:      noarch
License:        GPLv2+
URL:            http://packages.debian.org/unstable/dh-python
Source0:        http://ftp.de.debian.org/debian/pool/main/d/dh-python/%{name}_%{version}.%{date_source}.tar.xz
Patch0:         0001-fix-python-syntax-error.patch

BuildRequires:  python3-docutils
BuildRequires:  dpkg-dev

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       debhelper
Requires:       python3-devel
Provides:	dh-python3 

%description
 * pybuild - invokes various build systems for requested Python versions in
   order to build modules and extensions
 * dh_python2 - calculates Python 2.X dependencies for Debian packages,
   adds maintainer scripts to byte compile files, etc.
 * dh_python3 - calculates Python 3.X dependencies for Debian packages,
   adds maintainer scripts to byte compile files, etc.
 * dh_pypy - calculates PyPy dependencies for Debian packages,
   adds maintainer scripts to byte compile files, etc.


%prep
%autosetup -n %{name}-%{version}.%{date_source} -p1

%build


%install
	DESTDIR=%{buildroot} PREFIX=/usr make install manpages
	mkdir -p %{buildroot}/%{_mandir}/man1
	cp *.1   %{buildroot}/%{_mandir}/man1

%files
%doc *.rst
%license debian/copyright
%{_datadir}/%{name}/dh_python?
%{_datadir}/%{name}/pybuild
%{_datadir}/%{name}/dh_pypy
%{_datadir}/%{name}/dhpython
%{_datadir}/%{name}/dist/*
%{_datadir}/debhelper/autoscripts/*
%{perl_vendorlib}/../Debian/Debhelper/Buildsystem/pybuild.pm
%{perl_vendorlib}/../Debian/Debhelper/Sequence/pypy.pm
%{perl_vendorlib}/../Debian/Debhelper/Sequence/python3.pm
%{perl_vendorlib}/../Debian/Debhelper/Sequence/python2.pm
%{_mandir}/man1/*


%changelog

* Thu Nov 22 2018 David Va <davidva AT tuta DOT io> 3-1
- Updated to 3-1
- Upstream

* Fri Oct 16 2015 Alec Leamas <leamas.alec@gmail.com> - 2.20150826-1
- Initial release

