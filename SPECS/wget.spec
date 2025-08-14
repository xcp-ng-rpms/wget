%global package_speccommit e8abc4a1a016f9e0e665b2193a999490759dde6a
%global usver 1.21.3
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.21.3
Release: %{?xsrel}%{?dist}
License: GPLv3+
Url: http://www.gnu.org/software/wget/
Source0: wget-1.21.3.tar.gz
Patch0: wget-1.17-path.patch
Patch1: wget-1.21.3-hsts-32bit.patch


Provides: webclient
Provides: bundled(gnulib)
# needed for test suite
BuildRequires: make
%if 0%{?xenserver} < 9
# This is to remove dependencies which used for the unit test.
# We will no longer use wget in XS9, so it's safe to skip the unit test in XS9.
BuildRequires: perl(lib)
BuildRequires: perl(English)
BuildRequires: perl(HTTP::Daemon)
%endif
BuildRequires: python3
BuildRequires: gnutls-devel
BuildRequires: pkgconfig
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: autoconf
BuildRequires: libuuid-devel
BuildRequires: perl-podlators
BuildRequires: gpgme-devel
BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: git-core
%if 0%{?xenserver} > 8
BuildRequires: libidn2-devel
BuildRequires: libpsl-devel
BuildRequires: libmetalink-devel
# CP-46120: tests need it as well
BuildRequires: glibc-gconv-extra
%endif

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%prep
%autosetup -S git

# modify the package string
sed -i "s|\(PACKAGE_STRING='wget .*\)'|\1 (Red Hat modified)'|" configure
grep "PACKAGE_STRING='wget .* (Red Hat modified)'" configure || exit 1

%build
%configure \
    --with-ssl=gnutls \
    --with-libpsl \
    --enable-largefile \
    --enable-opie \
    --enable-digest \
    --enable-ntlm \
    --enable-nls \
    --enable-ipv6 \
    --disable-rpath \
    --with-metalink \
    --disable-year2038

%{make_build}

%install
rm -rf $RPM_BUILD_ROOT
%{make_install} CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}
%find_lang %{name}-gnulib

%check
# This is to remove dependencies which used for the unit test.
# We will no longer use wget in XS9, so it's safe to skip the unit test in XS9.
%if 0%{?xenserver} < 9
make check
%endif

%files -f %{name}.lang -f %{name}-gnulib.lang
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%{_bindir}/wget
%{_infodir}/*

%changelog
* Tue Oct 08 2024 Stephen Cheng <stephen.cheng@cloud.com> - 1.21.3-2
- CP-51608: Remove perl dependencies and skip the unit test for xs9

* Thu Jun 06 2024 Deli Zhang <deli.zhang@citrix.com> - 1.21.3-1
- First imported release

