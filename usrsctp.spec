%define commit d5f916d2a42606a7660384e8cbc9a05a933815b4
%define shortcommit %(c=%{commit}; echo ${c:0:7})

%define major 1
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	Reference Implementation for SCTP running in User Space
Name:		usrsctp
Version:	0.9.3.0
Release:	1
License:	BSD
Group:		System/Libraries
Url:		https://github.com/sctplab/%{name}/
Source0:	https://github.com/sctplab/%{name}/archive/%{commit}/%{name}-%{commit}.zip

BuildRequires:	texlive

%description
This is a the reference implementation for SCTP (RFC4960) running in User
Space.

It is part of the reference implementation for SCTP. It is portable and
runs on FreeBSD/MAC-OS/Windows and in User Space (including linux). It is
full featured and offers all of the features found in the SCTP RFC's as
well as some new drafts. It is actively maintained by many of the draft
and RFC authors. 

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Reference Implementation for SCTP running in User Space
Group:		System/Libraries

%description -n %{libname}
This is a the reference implementation for SCTP (RFC4960) running in User
Space.

It is part of the reference implementation for SCTP. It is portable and
runs on FreeBSD/MAC-OS/Windows and in User Space (including linux). It is
full featured and offers all of the features found in the SCTP RFC's as
well as some new drafts. It is actively maintained by many of the draft
and RFC authors.

%files -n %{libname}
%{_libdir}/libusrsctp.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name} library
Group:		Development/C
Requires: 	%{libname} = %{version}-%{release}
Provides:	%{name}-devel

%description -n %{devname}
Development files for %{name} library.

%files -n %{devname}
%{_includedir}/*
%{_libdir}/lib%{name}.so
%doc Manual.pdf

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{commit}
# Add missing files
touch AUTHORS NEWS README ChangeLog

# Use optimization flag O2
sed -i -e 's|-O0|-O2|' configure.ac

# Fix spurious-executable-perm
find . \( -name "*.c" -o -name "*.h" \) -exec chmod 0644 '{}' \;

%build
export CPPFLAGS="-O2 "
autoreconf -fiv
%configure --disable-warnings-as-errors
%make

# doc (three times needed for toc and bibliography)
pdflatex Manual.tex
pdflatex Manual.tex
pdflatex Manual.tex

%install
%makeinstall_std

