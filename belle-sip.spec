# TODO: tunnel >= 0.7.0? (BR: pkgconfig(tunnel) or TunnelConfig.cmake)
#
# Conditional build:
%bcond_without	dnssd		# MDNS/DNSSD support
%bcond_without	static_libs	# static library
%bcond_with	tests		# enable tests
#
Summary:	SIP (RFC3261) object-oriented implementation in C
Summary(pl.UTF-8):	Implementacja SIP (RFC3261) w C
Name:		belle-sip
Version:	5.4.17
Release:	1
License:	GPL v3+
Group:		Libraries
#Source0Download: https://gitlab.linphone.org/BC/public/belle-sip/-/tags
Source0:	https://gitlab.linphone.org/BC/public/belle-sip/-/archive/%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	c49ff21809abdfc5b15317b60f5e8758
Patch1:		%{name}-pc.patch
URL:		https://www.linphone.org/
%{?with_tests:BuildRequires:	CUnit >= 2.0}
%{?with_dnssd:BuildRequires:	avahi-compat-libdns_sd-devel}
BuildRequires:	bctoolbox-devel >= 5.3.0
BuildRequires:	belr-devel >= 5.3.0
BuildRequires:	cmake >= 3.22
BuildRequires:	jre
BuildRequires:	libantlr3c-devel >= 3.4
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	zlib-devel >= 1.2.3
Requires:	bctoolbox >= 5.3.0
Requires:	belr >= 5.3.0
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
Requires:	bctoolbox-devel >= 5.3.0
Requires:	belr-devel >= 5.3.0
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
%patch -P 1 -p1

%build
%if %{with static_libs}
%cmake -B builddir-static \
	-DBUILD_SHARED_LIBS=OFF \
	%{?with_dnssd:-DENABLE_MDNS=ON} \
	-DENABLE_UNIT_TESTS=OFF

%{__make} -C builddir-static
%endif

%cmake -B builddir \
	%{?with_dnssd:-DENABLE_MDNS=ON} \
	%{!?with_static_libs:-DENABLE_STATIC=OFF} \
	%{!?with_tests:-DENABLE_UNIT_TESTS=OFF}

%{__make} -C builddir

%if %{with tests}
%{__make} -C builddir test ARGS=--output-on-failure
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with static_libs}
%{__make} -C builddir-static install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%{__make} -C builddir install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md CHANGELOG.md README.md
%attr(755,root,root) %{_libdir}/libbelle-sip.so.1
%{_datadir}/belr/grammars/sdp_grammar.belr
%{_datadir}/belr/grammars/sip_grammar.belr

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbelle-sip.so
%{_includedir}/belle-sip
%{_pkgconfigdir}/belle-sip.pc
%{_libdir}/cmake/BelleSIP

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbelle-sip.a
%endif
