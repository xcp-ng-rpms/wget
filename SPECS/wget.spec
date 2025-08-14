Summary: A utility for retrieving files using the HTTP or FTP protocols
Name: wget
Version: 1.14
Release: 15%{?dist}.1
License: GPLv3+
Group: Applications/Internet
Url: http://www.gnu.org/software/wget/
Source: ftp://ftp.gnu.org/gnu/wget/wget-%{version}.tar.xz

Patch1: wget-rh-modified.patch
Patch2: wget-1.12-path.patch
Patch3: wget-1.14-sslreadtimeout.patch
Patch4: wget-1.14-manpage-tex5.patch
Patch5: wget-1.14-add_missing_options_doc.patch
Patch6: wget-1.14-texi2pod_error_perl518.patch
Patch7: wget-1.14-fix-double-free-of-iri-orig_url.patch
Patch8: wget-1.14-Fix-deadcode-and-possible-NULL-use.patch
Patch9: wget-1.14-doc-missing-opts-and-fix-preserve-permissions.patch
Patch10: wget-1.14-set_sock_to_-1_if_no_persistent_conn.patch
Patch11: wget-1.14-document-backups.patch
Patch12: wget-1.14-fix-backups-to-work-as-documented.patch
Patch13: wget-1.14-CVE-2014-4877.patch
Patch14: wget-1.14-rh1203384.patch
Patch15: wget-1.14-rh1147572.patch
Patch16: wget-1.14-CVE-2016-4971.patch
# needed because fix for CVE-2016-4971 changes default behavior
# and the file is not saved in correct encoding. This caused the
# Test-ftp-iri-fallback test to fail. This additional change makes
# Test-ftp-iri-fallback test pass again.
Patch17: wget-1.14-support-non-ASCII-characters.patch
Patch18: wget-1.14-add-openssl-tlsv11-tlsv12-support.patch
# Fix for randomly failing unit test
# combination of upstream commits without the support for Valgrind
# commit 3eff3ad69a46364475e1f4abdf9412cfa87e3d6c
# commit 2303793a626158627bdb2ac255e0f58697682b24
Patch19: wget-1.14-fix-synchronization-in-Test-proxied-https-auth.patch
Patch20: wget-1.14-CVE-2017-13089.patch
Patch21: wget-1.14-CVE-2017-13090.patch

Provides: webclient
Provides: bundled(gnulib) 
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
BuildRequires: openssl-devel, pkgconfig, texinfo, gettext, autoconf, libidn-devel, libuuid-devel, perl-podlators
# dependencies for the test suite
BuildRequires: perl-libwww-perl
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GNU Wget is a file retrieval utility which can use either the HTTP or
FTP protocols. Wget features include the ability to work in the
background while you are logged out, recursive retrieval of
directories, file name wildcard matching, remote file timestamp
storage and comparison, use of Rest with FTP servers and Range with
HTTP servers to retrieve files over slow or unstable connections,
support for Proxy servers, and configurability.

%prep
%setup -q
%patch1 -p0
%patch2 -p1
%patch3 -p1 -b .sslreadtimeout
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1 -b .tls11_tls12
%patch19 -p1 -b .test_synch_fix
%patch20 -p1 -b .CVE-2017-13089
%patch21 -p1 -b .CVE-2017-13090

%build
if pkg-config openssl ; then
    CPPFLAGS=`pkg-config --cflags openssl`; export CPPFLAGS
    LDFLAGS=`pkg-config --libs openssl`; export LDFLAGS
fi
%configure --with-ssl=openssl --enable-largefile --enable-opie --enable-digest --enable-ntlm --enable-nls --enable-ipv6 --disable-rpath
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CFLAGS="$RPM_OPT_FLAGS"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%find_lang %{name}

%post
/sbin/install-info %{_infodir}/wget.info.gz %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/wget.info.gz %{_infodir}/dir || :
fi

%clean
rm -rf $RPM_BUILD_ROOT

%check
make check

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAILING-LIST NEWS README COPYING doc/sample.wgetrc
%config(noreplace) %{_sysconfdir}/wgetrc
%{_mandir}/man1/wget.*
%{_bindir}/wget
%{_infodir}/*

%changelog
* Tue Oct 24 2017 Tomas Hozza <thozza@redhat.com> - 1.14-15.1
- Fixed various security flaws (CVE-2017-13089, CVE-2017-13090)

* Fri May 05 2017 Tomas Hozza <thozza@redhat.com> - 1.14-15
- Added TLSv1_1 and TLSv1_2 as secure-protocol values to help (#1439811)
- Fixed synchronization in randomly failing unit test Test-proxied-https-auth (#1448440)

* Wed Apr 12 2017 Tomas Hozza <thozza@redhat.com> - 1.14-14
- TLS v1.1 and v1.2 can now be specified with --secure-protocol option (#1439811)

* Mon Jun 20 2016 Tomas Hozza <thozza@redhat.com> - 1.14-13
- Fix CVE-2016-4971 (#1345778)
- Added support for non-ASCII URLs (Related: CVE-2016-4971)

* Mon Mar 21 2016 Tomas Hozza <thozza@redhat.com> - 1.14-12
- Fix wget to include Host header on CONNECT as required by HTTP 1.1 (#1203384)
- Run internal test suite during build (#1295846)
- Fix -nv being documented as synonym for two options (#1147572)

* Fri Oct 24 2014 Tomas Hozza <thozza@redhat.com> - 1.14-11
- Fix CVE-2014-4877 wget: FTP symlink arbitrary filesystem access (#1156136)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.14-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.14-9
- Mass rebuild 2013-12-27

* Mon Jul 15 2013 Tomas Hozza <thozza@redhat.com> - 1.14-8
- Fix deadcode and possible use of NULL in vprintf (#913153)
- Add documentation for --regex-type and --preserve-permissions
- Fix --preserve-permissions to work as documented (and expected)
- Fix bug when authenticating using user:password@url syntax (#912358)
- Document and fix --backups option

* Wed Jul 10 2013 Tomas Hozza <thozza@redhat.com> - 1.14-7
- Fix double free of iri->orig_url (#981778)

* Mon Jun 24 2013 Tomas Hozza <thozza@redhat.com> - 1.14-6
- add missing options accept-regex and reject-regex to man page
- fix errors in texi2pod introduced in Perl-5.18

* Fri Feb 22 2013 Tomas Hozza <thozza@redhat.com> - 1.14-5
- Added BuildRequires: perl-podlators for pod2man
- Patched manpage to silent new Tex errors
- Resolves: (#914571) 

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 11 2012 Tomas Hozza <thozza@redhat.com> 1.14-3
- Added libuuid-devel to BuildRequires to use libuuid functions
  in "src/warc.c" functions (#865421)

* Wed Oct 10 2012 Tomas Hozza <thozza@redhat.com> 1.14-2
- Added libidn-devel to BuildRequires to support IDN domains (#680394)

* Thu Aug 09 2012 Karsten Hopp <karsten@redhat.com> 1.14-1
- Update to wget-1.14

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Karsten Hopp <karsten@redhat.com> 1.13.4-4
- fix timeout if http server doesn't answer to SSL handshake (#860727)

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 1.13.4-3
- add virtual provides per https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Jon Ciesla <limburgher@gmail.com> - 1.13.4-1
- New upstream, BZ 730286.
- Modified path patch.
- subjectAltNames patch upstreamed.
- Specified openssl at config time.

* Thu Jun 23 2011 Volker Fröhlich <volker27@gmx.at> - 1.12-4
- Applied patch to accept subjectAltNames in X509 certificates (#674186)
- New URL (#658969)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 18 2009 Karsten Hopp <karsten@redhat.com> 1.12-2
- don't provide /usr/share/info/dir

* Tue Nov 17 2009 Karsten Hopp <karsten@redhat.com> 1.12-1
- update to wget-1.12
- fixes CVE-2009-3490 wget: incorrect verification of SSL certificate
  with NUL in name

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.11.4-5
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> 1.11.4-2
- rebuild with new openssl

* Wed Aug 13 2008 Karsten Hopp <karsten@redhat.com> 1.11.4-1
- update

* Wed Jun 04 2008 Karsten Hopp <karsten@redhat.com> 1.11.3-1
- wget-1.11.3, downgrades the combination of the -N and -O options
  to a warning instead of an error

* Fri May 09 2008 Karsten Hopp <karsten@redhat.com> 1.11.2-1
- wget-1.11.2, fixes #179962

* Mon Mar 31 2008 Karsten Hopp <karsten@redhat.com> 1.11.1-1
- update to bugfix release 1.11.1, fixes p.e. #433606

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.11-2
- Autorebuild for GCC 4.3

* Tue Dec 04 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-17
- rebuild to pick up new openssl SONAME

* Mon Aug 27 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-16
- fix license tag
- rebuild

* Mon Feb 12 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-15
- fix discarding of expired cookies
- escape non-printable characters
- drop to11 patch for now (#223754, #227853, #227498)

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-14
- shut up rpmlint, even though xx isn't a macro

* Mon Feb 05 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-13
- merge review changes (#226538)
  - use version/release/... in buildroot tag
  - remove BR perl
  - use SMP flags
  - use make install instead of %%makeinstall
  - include copy of license
  - use Requires(post)/Requires(preun)
  - use optflags
  - remove trailing dot from summary
  - change tabs to spaces

* Thu Jan 18 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-12
- don't abort (un)install scriptlets when _excludedocs is set (Ville Skyttä)

* Wed Jan 10 2007 Karsten Hopp <karsten@redhat.com> 1.10.2-11
- add fix for CVE-2006-6719

* Fri Dec 08 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-10
- fix repeated downloads (Tomas Heinrich, #186195)

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-9
- add distflag, rebuild

* Thu Dec 07 2006 Karsten Hopp <karsten@redhat.com> 1.10.2-8
- Resolves: #218211
  fix double free corruption

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-6
- fix resumed downloads (#205723)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-5.1
- rebuild

* Thu Jun 29 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-5
- updated german translations from Robert Scheck

* Tue Jun 27 2006 Karsten Hopp <karsten@redhat.de> 1.10.2-4
- upstream patches

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.10.2-3.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 1.10.2-3
- rebuilt against new openssl

* Tue Oct 25 2005 Karsten Hopp <karsten@redhat.de> 1.10.2-2
- use %%{_sysconfdir} (#171555)

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- 1.10.2

* Thu Sep 08 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-7
- fix builtin help of --load-cookies / --save-cookies (#165408)

* Wed Sep 07 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-6
- convert changelog to UTF-8 (#159585)

* Mon Sep 05 2005 Karsten Hopp <karsten@redhat.de> 1.10.1-5
- update
- drop patches which are already in the upstream sources

* Wed Jul 13 2005 Karsten Hopp <karsten@redhat.de> 1.10-5
- update german translation

* Mon Jul 11 2005 Karsten Hopp <karsten@redhat.de> 1.10-4
- update german translation (Robert Scheck)

* Tue Jul 05 2005 Karsten Hopp <karsten@redhat.de> 1.10-3
- fix minor documentation bug
- fix --no-cookies crash

* Mon Jul 04 2005 Karsten Hopp <karsten@redhat.de> 1.10-2
- update to wget-1.10
  - drop passive-ftp patch, already in 1.10
  - drop CVS patch
  - drop LFS patch, similar fix in 1.10
  - drop protdir patch, similar fix in 1.10
  - drop actime patch, already in 1.10

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-22
- build with gcc-4

* Wed Feb 02 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-21 
- remove old copy of the manpage (#146875, #135597)
- fix garbage in manpage (#117519)

* Tue Feb 01 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-20 
- texi2pod doesn't handle texinfo xref's. rewrite some lines so that
  the man page doesn't have incomplete sentences anymore (#140470)

* Mon Jan 31 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-19 
- Don't set actime to access time of the remote file or tmpwatch might 
  remove the file again (#146440).  Set it to the current time instead.
  timestamping checks only modtime, so this should be ok.

* Thu Jan 20 2005 Karsten Hopp <karsten@redhat.de> 1.9.1-18
- add support for --protocol-directories option as documented
  in the man page (Ville Skyttä, #145571)

* Wed Sep 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-17 
- additional LFS patch from Leonid Petrov to fix file lengths in 
  http downloads

* Thu Sep 16 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-16 
- more fixes

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-15 
- added strtol fix from Leonid Petrov, reenable LFS

* Tue Sep 14 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-14
- buildrequires gettext (#132519)

* Wed Sep 01 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-13
- disable LFS patch for now, it breaks normal downloads (123524#c15)

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-12 
- move largefile stuff inside the configure script, it didn't
  get appended to CFLAGS

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-11
- rebuild

* Tue Aug 31 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-10 
- fix patch

* Sun Aug 29 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-9
- more cleanups of the manpage (#117519)

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-8
- rebuild

* Fri Aug 27 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-7 
- clean up manpage (#117519)
- buildrequire texinfo (#123780)
- LFS patch, based on wget-LFS-20040630.patch from Leonid Petrov
  (#123524, #124628, #115348)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Mar 11 2004 Karsten Hopp <karsten@redhat.de> 1.9.1-3 
- fix documentation (#117517)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-3
- update to -stable CVS
- document the passive ftp default

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-2
- add patch from -stable CVS

* Fri Nov 28 2003 Karsten Hopp <karsten@redhat.de> 1.9.1-1
- update to 1.9.1
- remove obsolete patches

* Mon Aug 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.3
- fix variable usage

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-15.2
- rebuild

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15.1
- rebuilt

* Wed Jun 25 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-15
- default to passive-ftp (#97996)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-13
- rebuild

* Wed Jun 04 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-12
- merge debian patch for long URLs
- cleanup filename patch

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-11
- rebuild

* Sun May 11 2003 Karsten Hopp <karsten@redhat.de> 1.8.2-10
- upstream fix off-by-one error

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.8.2-8
- rebuild

* Fri Dec 13 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl pkg-config data, if present
- don't bomb out when building with newer openssl

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 1.8.2-7
- rebuild on all arches

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches

* Fri Oct 4 2002 Karsten Hopp <karsten@redhat.de> 1.8.2-5
- fix directory traversal bug

* Wed Jul 24 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.2-3
- Don't segfault when downloading URLs A-B-A (A-A-B worked) #49859

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.2 (bug-fix release)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove s390 patch, not needed anymore

* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.8.1-4
- Rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add hack to not link against libmd5, even if available

* Fri Dec 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8.1

* Thu Dec 13 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.8
- also include md5global to get it compile

* Sun Nov 18 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.7.1

* Wed Sep  5 2001 Phil Knirsch <phil@redhat.de> 1.7-3
- Added va_args patch required for S390.

* Mon Sep  3 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.7-2
- Configure with ssl support (duh - #53116)
- s/Copyright/License/

* Wed Jun  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 1.7
- Require perl for building (to get man pages)
- Don't include the Japanese po file, it's now included
- Use %%{_tmppath}
- no patches necessary
- Make /etc/wgetrc noreplace
- More docs

* Tue Jan 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Norwegian isn't a iso-8859-2 locale, neither is Danish.
  This fixes #15025.
- langify

* Sat Jan  6 2001 Bill Nottingham <notting@redhat.com>
- escape %%xx characters before fnmatch (#23475, patch from alane@geeksrus.net)

* Fri Jan  5 2001 Bill Nottingham <notting@redhat.com>
- update to 1.6, fix patches accordingly (#23412)
- fix symlink patch (#23411)

* Mon Dec 18 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese and Korean Resources

* Tue Aug  1 2000 Bill Nottingham <notting@redhat.com>
- setlocale for LC_CTYPE too, or else all the translations think their
  characters are unprintable.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- build in new environment

* Mon Jun  5 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHS compliance

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Thu Aug 26 1999 Jeff Johnson <jbj@redhat.com>
- don't permit chmod 777 on symlinks (#4725).

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- build for 6.0 tree
- add Provides

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.5.3

* Sat Jun 27 1998 Jeff Johnson <jbj@redhat.com>
- updated to 1.5.2

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- modified group to Applications/Networking

* Wed Apr 22 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.5.0
- they removed the man page from the distribution (Duh!) and I added it back
  from 1.4.5. Hey, removing the man page is DUMB!

* Fri Nov 14 1997 Cristian Gafton <gafton@redhat.com>
- first build against glibc
