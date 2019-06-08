# TODO: tunnel? (BR: pkgconfig(tunnel) or TunnelConfig.cmake)
#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_with	tests		# enable tests
#
Summary:	SIP (RFC3261) object-oriented implementation in C
Summary(pl.UTF-8):	Implementacja SIP (RFC3261) w C
Name:		belle-sip
Version:	1.6.3
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	https://linphone.org/releases/sources/belle-sip/%{name}-%{version}.tar.gz
# Source0-md5:	90c40812d98671ad2f40621542500bc6
Patch0:		antlr_jar.patch
Patch1:		build.patch
URL:		http://www.linphone.org/
%{?with_tests:BuildRequires:	CUnit >= 2.0}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	bctoolbox-devel >= 0.5.0
BuildRequires:	java-antlr3 >= 3.2
BuildRequires:	jre
BuildRequires:	libantlr3c-devel >= 3.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig
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
%setup -q -n %{name}-%{version}-0
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
WARNFLAGS="-Wno-error=pragmas -Wno-error=array-bounds"
%if "%{cc_version}" >= "7"
WARNFLAGS="$WARNFLAGS -Wno-implicit-fallthrough -Wno-error=cast-function-type"
%endif
%configure \
	CFLAGS="%{rpmcflags} $WARNFLAGS" \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}

%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libbellesip.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README.md
%attr(755,root,root) %{_libdir}/libbellesip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbellesip.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbellesip.so
%{_includedir}/belle-sip
%{_pkgconfigdir}/belle-sip.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbellesip.a
%endif
