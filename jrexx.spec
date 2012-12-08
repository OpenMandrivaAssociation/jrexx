# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

Summary:        Automaton based regluar expression API for Java
Name:           jrexx
Version:        1.1.1
Release:        3.1.1
Epoch:          0
License:        LGPL
URL:            http://www.karneim.com/jrexx/
Group:          Development/Java
Source0:        jrexx-1.1.1-src.zip
Source1:        jrexx-build.xml
BuildRequires:  java-rpmbuild >= 0:1.5.32
BuildRequires:  ant >= 0:1.5.4
BuildRequires:  locales-en
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
BuildRequires:  java-devel
%endif

%description
jrexx is a powerful easy-to-use regular expression 
API for textual pattern matching. Technically jrexx 
uses a minimized deterministic FSA (finite state 
automaton) and compiles the textual representation 
of the regular expression into such an automaton. 
Besides the usual pattern matching functionality, 
jrexx provides an introspection API for exploration 
of the automaton's structure by 'states' and 
'transitions'. Since the automaton is deterministic 
and minimized the pattern matching alogorithm is 
extremly fast (compared to the java regular 
expression API in JDK1.4) and works with huge 
patterns and input texts. Since FSA can be handled 
as sets, jrexx also offers all basic set operations 
for complement, union, intersection and difference, 
which is not provided by other regex implementations 
(as far as we know). 


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%prep
%setup -T -c %{name}-%{version}
unzip -q %{SOURCE0}
cp %{SOURCE1} build.xml

%build
export LC_ALL=ISO-8859-1
%{ant} dist

%install
# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p output/dist/lib/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif


%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}

# -----------------------------------------------------------------------------


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.1-3.0.8mdv2011.0
+ Revision: 665836
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.1-3.0.7mdv2011.0
+ Revision: 606112
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.1-3.0.6mdv2010.1
+ Revision: 523130
- rebuilt for 2010.1

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.1.1-3.0.5mdv2010.0
+ Revision: 425471
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.1.1-3.0.4mdv2009.1
+ Revision: 351314
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 0:1.1.1-3.0.3mdv2009.0
+ Revision: 140829
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.1-3.0.3mdv2008.1
+ Revision: 120946
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.1.1-3.0.2mdv2008.0
+ Revision: 87440
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Thu Aug 02 2007 David Walluck <walluck@mandriva.org> 0:1.1.1-3.0.1mdv2008.0
+ Revision: 58365
- Import jrexx



* Wed Jul 18 2007 Alexander Kurtakov <akurtakov@active-lynx.com> - 0:1.1.1-3.0.1mdv2008.0
- Adapt for Mandriva

* Thu Jan 05 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.1.1-3jpp
- First JPP 1.7 build

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:1.1.1-2jpp
- Rebuild with ant-1.6.2

* Tue Feb 24 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1.1-1jpp
- First JPackage release
