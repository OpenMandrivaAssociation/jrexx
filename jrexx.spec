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

Summary:	Automaton based regluar expression API for Java
Name:		jrexx
Version:	1.1.1
Release:	11
License:	LGPLv2
Url:		https://www.karneim.com/jrexx/
Group:		Development/Java
Source0:	jrexx-1.1.1-src.zip
Source1:	jrexx-build.xml
%if !%{gcj_support}
BuildArch:	noarch
BuildRequires:	java-devel
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.5.32
BuildRequires:	ant >= 0:1.5.4
BuildRequires:	locales-en

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
Summary:	Javadoc for %{name}
Group:		Development/Java

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
mkdir -p %{buildroot}%{_javadir}
cp -p output/dist/lib/%{name}-%{version}.jar \
	%{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr output/dist/jdoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%doc %{_javadocdir}

