%define PYTHON_NAME %((rpm -q --quiet python2 && echo python2) || echo python)
%define PYTHON_VERSION %(%{PYTHON_NAME} -c 'import sys; print sys.version[:3],')
%define NEXT_PYTHON_VERSION %(%{PYTHON_NAME} -c 'import sys; print "%d.%d" % (sys.version_info[0], sys.version_info[1]+1),')

Version: 1.1.7
Summary: Convenient and transparent local/remote incremental mirror/backup
Name: rdiff-backup
Release: 1
Epoch: 0
URL: http://rdiff-backup.stanford.edu/
Source: http://rdiff-backup.stanford.edu/OLD/1.1.7/rdiff-backup-1.1.7.tar.gz
License: GPL
Group: Applications/Archiving
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{PYTHON_NAME} >= %{PYTHON_VERSION}, %{PYTHON_NAME} < %{NEXT_PYTHON_VERSION}
BuildPrereq: %{PYTHON_NAME}-devel >= 2.2, librsync-devel >= 0.9.7

%description
rdiff-backup is a script, written in Python, that backs up one
directory to another and is intended to be run periodically (nightly
from cron for instance). The target directory ends up a copy of the
source directory, but extra reverse diffs are stored in the target
directory, so you can still recover files lost some time ago. The idea
is to combine the best features of a mirror and an incremental
backup. rdiff-backup can also operate in a bandwidth efficient manner
over a pipe, like rsync. Thus you can use rdiff-backup and ssh to
securely back a hard drive up to a remote location, and only the
differences from the previous backup will be transmitted.

%prep
%setup -q

%build
%{PYTHON_NAME} setup.py build

%install
%{PYTHON_NAME} setup.py install --root $RPM_BUILD_ROOT
# Produce .pyo files for %ghost directive later
%{PYTHON_NAME} -Oc 'from compileall import *; compile_dir("'$RPM_BUILD_ROOT/%{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup'")'
rm -rf $RPM_BUILD_ROOT/usr/share/doc/* 

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/rdiff-backup
%{_bindir}/rdiff-backup-statistics
%{_mandir}/man1/rdiff-backup*
%dir %{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup
%{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup/*.py
%{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup/*.pyc
%{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup/*.so
%ghost %{_libdir}/python%{PYTHON_VERSION}/site-packages/rdiff_backup/*.pyo
%doc CHANGELOG COPYING FAQ.html examples.html README

%changelog
* Mon Aug 22 2005 Ben Escoto <ben@emerose.org> - 1.0.0-3
- Matthijs van der Klip's patch to fix python2 support

* Tue Aug 16 2005 Ben Escoto <ben@emerose.org> - 1.0.0-2
- Removing /usr/share/doc in build for some obscure reason

* Mon Mar 28 2005 Ben Escoto <ben@emerose.org> - 0.13.5-1
- Set librsync >= 0.9.7 to encourage upgrade

* Sat Dec 15 2003 Ben Escoto <bescoto@stanford.edu> - 0.12.6-2
- Readded python2/python code; turns out not everyone calls it python
- A number of changes from Fedora rpm.

* Thu Sep 11 2003 Ben Escoto <bescoto@stanford.edu> - 0.12.4-1
- Removed code that selected between python2 and python; I think
  everyone calls it python now.

* Thu Aug 8 2003 Ben Escoto <bescoto@stanford.edu>
- Set librsync >= 0.9.6, because rsync.h renamed to librsync.h

* Sun Jul 20 2003 Ben Escoto <bescoto@stanford.edu>
- Minor changes to comply with Fedora standards.

* Sun Jan 19 2002 Troels Arvin <troels@arvin.dk>
- Builds, no matter if Python 2.2 is called python2-2.2 or python-2.2.

* Sun Nov 4 2001 Ben Escoto <bescoto@stanford.edu>
- Initial RPM
