# TODO: tunnel? (BR: pkgconfig(tunnel))
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with	tests		# enable tests
#
Summary:	SIP (RFC3261) object-oriented implementation in C
Summary(pl.UTF-8):	Implementacja SIP (RFC3261) w C
Name:		belle-sip
Version:	1.4.1
Release:	1
License:	GPL v2+
Group:		Libraries
Source0:	http://download-mirror.savannah.gnu.org/releases/linphone/belle-sip/%{name}-%{version}.tar.gz
# Source0-md5:	c6460e294e77bd0646b7eda7fbe21523
Patch0:		antlr_jar.patch
URL:		http://www.linphone.org/
%{?with_tests:BuildRequires:	CUnit >= 2.0}
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	java-antlr3 >= 3.2
BuildRequires:	jre
BuildRequires:	libantlr3c-devel >= 3.4
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	polarssl-devel >= 1.2
BuildRequires:	pkgconfig
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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} -Wno-error=pragmas" \
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
%doc AUTHORS NEWS README
%attr(755,root,root) %{_libdir}/libbellesip.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbellesip.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbellesip.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libbellesip.a
%endif
