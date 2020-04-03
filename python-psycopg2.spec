%{?scl:%scl_package python-%{srcname}}
%{!?scl:%global pkg_name %{name}}

%global python3_pkgversion %{nil}

%bcond_with tests

%global srcname	psycopg2
%global sum	A PostgreSQL database adapter for Python
%global desc	Psycopg is the most popular PostgreSQL adapter for the Python \
programming language. At its core it fully implements the Python DB \
API 2.0 specifications. Several extensions allow access to many of the \
features offered by PostgreSQL.

%global python_runtimes python%{python3_version}

Summary:	%{sum}
Name:		%{?scl_prefix}python-%{srcname}
Version:	2.8.4
Release:	5%{?dist}
# The exceptions allow linking to OpenSSL and PostgreSQL's libpq
License:	LGPLv3+ with exceptions
Url:		http://initd.org/psycopg/

Source0:	http://initd.org/psycopg/tarballs/PSYCOPG-2-8/psycopg2-%{version}.tar.gz

%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}
BuildRequires:	%{?scl_prefix}python%{python3_pkgversion}-devel %{?scl_prefix}python%{python3_pkgversion}-setuptools %{?scl_prefix}python%{python3_pkgversion}-rpm-macros
BuildRequires:	gcc
BuildRequires:	postgresql-devel

# For testsuite
%if %{with tests}
BuildRequires: postgresql-test-rpm-macros
%endif

%description
%{desc}


%package -n %{?scl_prefix}python%{python3_pkgversion}-psycopg2-doc
Summary:	Documentation for psycopg python PostgreSQL database adapter


%description -n %{?scl_prefix}python%{python3_pkgversion}-psycopg2-doc
Documentation and example files for the psycopg python PostgreSQL
database adapter.


%prep
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%autosetup -p1 -n psycopg2-%{version}

%{?scl:EOF}


%build
%{?scl:scl enable %{scl} - << \EOF}
set -ex
export CFLAGS=${RPM_OPT_FLAGS} LDFLAGS=${RPM_LD_FLAGS}
for python in %{python_runtimes} ; do
  $python setup.py build
done

# Fix for wrong-file-end-of-line-encoding problem; upstream also must fix this.
for i in `find doc -iname "*.html"`; do sed -i 's/\r//' $i; done
for i in `find doc -iname "*.css"`; do sed -i 's/\r//' $i; done

# Get rid of a "hidden" file that rpmlint complains about
%{__rm} -f doc/html/.buildinfo

# We can not build docs now:
# https://www.postgresql.org/message-id/2741387.dvL6Cb0VMB@nb.usersys.redhat.com
# make -C doc/src html

%{?scl:EOF}


%check
%{?scl:scl enable %{scl} - << \EOF}
set -ex
%if %{with tests}
export PGTESTS_LOCALE=C.UTF-8
%postgresql_tests_run

export PSYCOPG2_TESTDB=${PGTESTS_DATABASES##*:}
export PSYCOPG2_TESTDB_HOST=$PGHOST
export PSYCOPG2_TESTDB_PORT=$PGPORT

cmd="import tests; tests.unittest.main(defaultTest='tests.test_suite')"

PYTHONPATH=%buildroot%python3_sitearch %__python3 -c "$cmd" --verbose
%endif

%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
set -ex
export CFLAGS=${RPM_OPT_FLAGS} LDFLAGS=${RPM_LD_FLAGS}
for python in %{python_runtimes} ; do
  $python setup.py install --no-compile --root %{buildroot}
done

%{?scl:EOF}


%files
%license LICENSE
%doc AUTHORS NEWS README.rst
%{python3_sitearch}/psycopg2/
%{python3_sitearch}/psycopg2-%{version}-py3*.egg-info

%files -n %{?scl_prefix}python%{python3_pkgversion}-psycopg2-doc
%license LICENSE
%doc doc


%changelog
* Tue Feb 04 2020 Lumír Balhar <lbalhar@redhat.com> - 2.8.4-5
- Import from the python38 module and modified for rh-python38 RHSCL
Resolves: rhbz#1671025

* Fri Dec 13 2019 Tomas Orsava <torsava@redhat.com> - 2.8.4-4
- Exclude unsupported i686 arch

* Wed Dec 11 2019 Tomas Orsava <torsava@redhat.com> - 2.8.4-3
- Fix shebang mangling
- Don't ship the debug module, it is not needed and was not shipped in RHEL8 either

* Thu Nov 21 2019 Lumír Balhar <lbalhar@redhat.com> - 2.8.4-2
- Adjusted for Python 3.8 module in RHEL 8

* Wed Nov 06 2019 Lumír Balhar <lbalhar@redhat.com> - 2.8.4-1
- New upstream version 2.8.4
- bcond check renamed to bcond tests

* Sun Oct 20 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.3-2
- Package python2-psycopg2 removed on Fedora 32+ (rhbz#1761216)

* Mon Sep 09 2019 Devrim Gündüz <devrim@gunduz.org> - 2.8.3-1
- Update to 2.8.3

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.7-5
- Package python2-psycopg2-debug removed on Fedora 32+ (rhbz#1747670)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.7-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Miro Hrončok <mhroncok@redhat.com> - 2.7.7-2
- Fixes for 3.8.0a4 rebuild
  Resolves: 1693641

* Tue Feb 05 2019 Pavel Raiskup <praiskup@redhat.com> - 2.7.7-1
- update to the latest upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 03 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.5-5
- prepare --without=debugrpms option (rhbz#1635166)
- get the python2 packages back for a while (rhbz#1634973)

* Wed Oct 03 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.5-4
- drop python2* on f30+ (rhbz#1634973)
- use proper compiler/linker flags (rhbz#1631713)
- correct the (build)requires

* Tue Jul 17 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.5-3
- standalone installable doc subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.5-2
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.5-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2018/06/17/psycopg-275-released/

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7.4-5
- Rebuilt for Python 3.7

* Mon May 21 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.4-4
- fix for python 3.7, by mhroncok

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.4-3
- depend on postgresql-test-rpm-macros

* Fri Apr 13 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.4-2
- re-enable testsuite

* Mon Feb 12 2018 Pavel Raiskup <praiskup@redhat.com> - 2.7.4-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2018/02/08/psycopg-274-released/

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 14 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.3.2-2
- treat python3/python2 equally

* Wed Oct 25 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.3.2-1
- update to 2.7.3.2, per release notes:
  http://initd.org/psycopg/articles/2017/10/24/psycopg-2732-released/

* Mon Aug 28 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.3.1-1
- http://initd.org/psycopg/articles/2017/08/26/psycopg-2731-released/

* Sun Aug 13 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.3-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2017/07/24/psycopg-273-released/

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.2-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2017/07/22/psycopg-272-released/

* Mon Mar 13 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7.1-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2017/03/01/psycopg-271-released/
- fix testsuite

* Thu Mar 02 2017 Pavel Raiskup <praiskup@redhat.com> - 2.7-1
- rebase to latest upstream release, per release notes:
  http://initd.org/psycopg/articles/2017/03/01/psycopg-27-released/
- enable testsuite during build, and package it

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.6.2-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 07 2016 Pavel Raiskup <praiskup@redhat.com> - 2.6.2-1
- rebase (rhbz#1353545), per release notes
  http://initd.org/psycopg/articles/2016/07/07/psycopg-262-released/

* Sun May 29 2016 Pavel Raiskup <praiskup@redhat.com> - 2.6.1-6
- provide python2-psycopg2 (rhbz#1306025)
- cleanup obsoleted packaging stuff

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Pavel Raiskup <praiskup@redhat.com> - 2.6.1-4
- again bump for new Python 3.5, not build previously?
- fix rpmlint issues
- no pyo files with python 3.5

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Jozef Mlich <jmlich@redhat.com> 2.6.1-1
- Update to 2.6.1

* Mon Feb 9 2015 Devrim Gündüz <devrim@gunduz.org> 2.6-1
- Update to 2.6, per changes described at:
  http://www.psycopg.org/psycopg/articles/2015/02/09/psycopg-26-and-255-released/

* Tue Jan 13 2015 Devrim Gündüz <devrim@gunduz.org> 2.5.4-1
- Update to 2.5.4, per changes described at:
  http://www.psycopg.org/psycopg/articles/2014/08/30/psycopg-254-released

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 04 2014 Pavel Raiskup <praiskup@redhat.com> - 2.5.3-1
- rebase to most recent upstream version, per release notes:
  http://www.psycopg.org/psycopg/articles/2014/05/13/psycopg-253-released/

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Jan 7 2014 Devrim Gündüz <devrim@gunduz.org> 2.5.2-1
- Update to 2.5.2, per changes described at:
  http://www.psycopg.org/psycopg/articles/2014/01/07/psycopg-252-released

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 07 2013 Pavel Raiskup <praiskup@redhat.com> - 2.5.1-1
- rebase to 2.5.1

* Thu May 16 2013 Devrim Gündüz <devrim@gunduz.org> 2.5-1
- Update to 2.5, per changes described at:
  http://www.psycopg.org/psycopg/articles/2013/04/07/psycopg-25-released/

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.4.5-6
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.4.5-5
- generalize python 3 fileglobbing to work with both Python 3.2 and 3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.4.5-4
- replace "python3.2dmu" with "python3-debug"; with_python3 fixes

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.4.5-3
- add with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr  7 2012 Tom Lane <tgl@redhat.com> 2.4.5-1
- Update to 2.4.5

* Thu Feb  2 2012 Tom Lane <tgl@redhat.com> 2.4.4-1
- Update to 2.4.4
- More specfile neatnik-ism

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 29 2011 Tom Lane <tgl@redhat.com> 2.4.2-2
- Fix mistaken %%dir marking on python3 files, per Dan Horak

* Sat Jun 18 2011 Tom Lane <tgl@redhat.com> 2.4.2-1
- Update to 2.4.2
Related: #711095
- Some neatnik specfile cleanups

* Thu Feb 10 2011 David Malcolm <dmalcolm@redhat.com> - 2.4-0.beta2
- 2.4.0-beta2
- add python 2 debug, python3 (optimized) and python3-debug subpackages

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 29 2010 Tom Lane <tgl@redhat.com> 2.3.2-1
- Update to 2.3.2
- Clean up a few rpmlint warnings

* Fri Dec 03 2010 Jason L Tibbitts III <tibbs@math.uh.edu> - 2.2.2-3
- Fix incorrect (and invalid) License: tag.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 20 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.2-1
- Update to 2.2.2

* Tue May 18 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.2.1-1
- Update to 2.2.1
- Improve description for 2.2 features.
- Changelog for 2.2.0 is: 
   http://initd.org/pub/software/psycopg/ChangeLog-2.2

* Wed Mar 17 2010 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.14-1
- Update to 2.0.14
- Update license (upstream switched to LGPL3)

* Sun Jan 24 2010 Tom Lane <tgl@redhat.com> 2.0.13-2
- Fix rpmlint complaints: remove unneeded explicit Requires:, use Conflicts:
  instead of bogus Obsoletes: to indicate lack of zope subpackage

* Sun Oct 18 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.13-1
- Update to 2.0.13

* Fri Aug 14 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.12-1
- Update to 2.0.12

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.11-1
- Update to 2.0.11

* Tue Apr 21 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.10-1
- Update to 2.0.10

* Fri Mar 20 2009 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.9-1
- Update to 2.0.9

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.8-2
- Rebuild for Python 2.6

* Sat Nov 29 2008 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.8-1
- Update to 2.0.8

* Sat Nov 29 2008 Devrim GUNDUZ <devrim@gunduz.org> - 2.0.8-1
- Update to 2.0.8

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.7-3
- Rebuild for Python 2.6

* Thu May 29 2008 Todd Zullinger <tmz@pobox.com> - 2.0.7-2
- fix license tags

* Wed Apr 30 2008 Devrim GUNDUZ <devrim@commandprompt.com> 2.0.7-1
- Update to 2.0.7

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.6-4.1
- Autorebuild for GCC 4.3

* Mon Jan 21 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.6-3.1
- Rebuilt against PostgreSQL 8.3

* Thu Jan 3 2008 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.6-3
- Rebuild for rawhide changes

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.0.6-2
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.6-1
- Update to 2.0.6

* Thu Apr 26 2007 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-8
- Disabled zope package temporarily.

* Wed Dec 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-7
- Rebuilt

* Wed Dec 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-5
- Bumped up spec version

* Wed Dec 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-4
- Rebuilt for PostgreSQL 8.2.0

* Mon Sep 11 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-3
- Rebuilt

* Wed Sep 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-2
- Remove ghost'ing, per Python Packaging Guidelines

* Mon Sep 4 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.5.1-1
- Update to 2.0.5.1

* Sun Aug 6 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-3
- Fixed zope package dependencies and macro definition, per bugzilla review (#199784)
- Fixed zope package directory ownership, per bugzilla review (#199784)
- Fixed cp usage for zope subpackage, per bugzilla review (#199784)

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-2
- Fixed 64 bit builds
- Fixed license
- Added Zope subpackage
- Fixed typo in doc description
- Added macro for zope subpackage dir

* Mon Jul 31 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.3-1
- Update to 2.0.3
- Fixed spec file, per bugzilla review (#199784)

* Sat Jul 22 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-3
- Removed python dependency, per bugzilla review. (#199784)
- Changed doc package group, per bugzilla review. (#199784)
- Replaced dos2unix with sed, per guidelines and bugzilla review (#199784)
- Fix changelog dates

* Sat Jul 22 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-2
- Added dos2unix to buildrequires
- removed python related part from package name

* Fri Jul 21 2006 - Devrim GUNDUZ <devrim@commandprompt.com> 2.0.2-1
- Fix rpmlint errors, including dos2unix solution
- Re-engineered spec file

* Mon Jan 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com>
- First 2.0.X build

* Mon Jan 23 2006 - Devrim GUNDUZ <devrim@commandprompt.com>
- Update to 1.2.21

* Tue Dec 06 2005 - Devrim GUNDUZ <devrim@commandprompt.com>
- Initial release for 1.1.20