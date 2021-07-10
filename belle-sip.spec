# TODO: tunnel? (BR: pkgconfig(tunnel) or TunnelConfig.cmake)
#
# Conditional build:
%bcond_without	dnssd		# MDNS/DNSSD support
%bcond_without	static_libs	# static library
%bcond_with	tests		# enable tests
#
Summary:	SIP (RFC3261) object-oriented implementation in C
Summary(pl.UTF-8):	Implementacja SIP (RFC3261) w C
Name:		belle-sip
Version:	4.5.20
Release:	2
License:	GPL v2+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/belle-sip/-/tags
Source0:	https://gitlab.linphone.org/BC/public/belle-sip/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	57b680975c7c78955bc06b5331f651bf
Patch0:		antlr_jar.patch
Patch1:		%{name}-pc.patch
URL:		http://www.linphone.org/
%{?with_tests:BuildRequires:	CUnit >= 2.0}
BuildRequires:	bctoolbox-devel >= 0.5.0
BuildRequires:	cmake >= 3.1
BuildRequires:	java-antlr3 >= 3.2
BuildRequires:	jre
BuildRequires:	libantlr3c-devel >= 3.4
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel >= 1.2.3
Requires:	bctoolbox >= 0.5.0
Requires:	libantlr3c >= 3.4
Requires:	zlib >= 1.2.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Belle-sip is a SIP (RFC3261) implementation written in C, with an
object oriented API.

%description -l pl.UTF-8
Belle-sip to implementacja SIP (RFC3261) napisana w C z API
zorientowanym obiektowo.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	bctoolbox-devel >= 0.5.0
Requires:	libantlr3c-devel >= 3.4

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%package static
Summary:	Static %{name} library
Summary(pl.UTF-8):	Statyczna biblioteka %{name}
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static %{name} library.

%description static -l pl.UTF-8
Statyczna biblioteka %{name}.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
install -d builddir
cd builddir
%cmake .. \
	%{?with_dnssd:-DENABLE_MDNS=ON} \
	%{!?with_static_libs:-DENABLE_STATIC=OFF} \
	%{!?with_tests:-DENABLE_TESTS=OFF}

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

# disable completeness check incompatible with split packaging
%{__sed} -i -e '/^foreach(target .*IMPORT_CHECK_TARGETS/,/^endforeach/d; /^unset(_IMPORT_CHECK_TARGETS)/d' $RPM_BUILD_ROOT%{_libdir}/cmake/BelleSIP/BelleSIPTargets.cmake

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbellesip.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbellesip.so
%{_includedir}/belle-sip
%{_pkgconfigdir}/belle-sip.pc
%{_libdir}/cmake/BelleSIP

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbellesip.a
%endif
