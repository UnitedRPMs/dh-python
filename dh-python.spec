%global _debpy_name python3-defaults

%global _debpy_ver	%version
%global _debpy_rel	1

%global _py3def_name 	dh-python
%global _py3def_ver	3.20190308

Name:           dh-python
Version:        3.7.3
Release:        1%{?dist}
Summary:        debhelper add-on to to handle python 3 files after build

BuildArch:      noarch
License:        GPLv2+
URL:            http://packages.debian.org/unstable/dh-python
Source0:        https://deb.debian.org/debian/pool/main/p/%{_debpy_name}/%{_debpy_name}_%{_debpy_ver}-%{_debpy_rel}.tar.gz
Source1:	http://debian.backend.mirrors.debian.org/debian/pool/main/d/%{_py3def_name}/%{_py3def_name}_%{_py3def_ver}.tar.xz
Patch:		py3versions.patch

BuildRequires:  python3-docutils
Requires:       python3-devel
BuildRequires:  dpkg-dev
BuildRequires:	debhelper
BuildRequires:	python3-rpm-macros

Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
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
%autosetup -n python3-defaults -p1 -a 1

%build

make

pushd %{_py3def_name}-%{_py3def_ver}
make
popd

%install

make DESTDIR="%{buildroot}/" PREFIX=/usr install

  mkdir -p %{buildroot}/%{python3_sitelib}
  install -m 755 debian/py3versions.py %{buildroot}/%{python3_sitelib}/
  ln -s -r -f %{_datadir}/python3/py3versions.py %{buildroot}/%{_bindir}/py3versions
  install -m 755 debian/debian_defaults %{buildroot}/%{python3_sitelib}/
  gzip -f debian/py3versions.1
  mkdir -p %{buildroot}/%{_mandir}/man1
  install -m 644 debian/py3versions.1.gz %{buildroot}/%{_mandir}/man1/

  mkdir -p %{buildroot}/%{_datadir}/licenses/%{name}/
  install -D -m 644 debian/copyright %{buildroot}/%{_datadir}/licenses/%{name}/

  pushd %{_py3def_name}-%{_py3def_ver}
  make DESTDIR="%{buildroot}/" PREFIX=/usr install

  ln -s -f -r %{_datadir}/dh-python/dh_pypy %{buildroot}/usr/bin/dh_pypy
  ln -s -f -r %{_datadir}/dh-python/dh_python3 %{buildroot}/usr/bin/dh_python3
  ln -s -f -r %{_datadir}/dh-python/pybuild %{buildroot}/usr/bin/pybuild

  mkdir -p %{buildroot}/%{_datadir}/perl5/vendor_perl
  mv -f %{buildroot}/%{_datadir}/perl5/Debian %{buildroot}/%{_datadir}/perl5/vendor_perl/Debian

  mv -f %{buildroot}/%{_datadir}/python3/debpython %{buildroot}/%{python3_sitelib}/
  mv -f %{buildroot}/%{_datadir}/python3/runtime.d %{buildroot}/%{python3_sitelib}/

%files
%doc *.rst
%license debian/copyright
%{_bindir}/dh_pypy
%{_bindir}/dh_python3
%{_bindir}/py3clean
%{_bindir}/py3compile
%{_bindir}/py3versions
%{_bindir}/pybuild
%{_datadir}/debhelper/
%{_datadir}/dh-python/
%{_mandir}/man1/py3versions.1.gz
%{python3_sitelib}/__pycache__/py3versions.cpython-*.opt-1.pyc
%{python3_sitelib}/__pycache__/py3versions.cpython-*.pyc
%{python3_sitelib}/debian_defaults
%{python3_sitelib}/py3versions.py
%{python3_sitelib}/debpython/
%{python3_sitelib}/runtime.d/
%{_datadir}/perl5/vendor_perl/Debian/Debhelper/Buildsystem/pybuild.pm
%{_datadir}/perl5/vendor_perl/Debian/Debhelper/Sequence/pypy.pm
%{_datadir}/perl5/vendor_perl/Debian/Debhelper/Sequence/python2.pm
%{_datadir}/perl5/vendor_perl/Debian/Debhelper/Sequence/python3.pm

%changelog

* Tue Apr 16 2019 David Va <davidva AT tuta DOT io> 3.7.3-1
- Updated to 3.7.3-1

* Thu Nov 22 2018 David Va <davidva AT tuta DOT io> 3-1
- Updated to 3-1
- Upstream

* Fri Oct 16 2015 Alec Leamas <leamas.alec@gmail.com> - 2.20150826-1
- Initial release

