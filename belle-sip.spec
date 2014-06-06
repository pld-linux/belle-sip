#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_with	tests		# enable tests
#
Summary:	SIP (RFC3261) object-oriented implementation in C
Summary(pl.UTF-8):	Implementacja SIP (RFC3261) w C
Name:		belle-sip
Version:	1.3.0
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://download-mirror.savannah.gnu.org/releases/linphone/belle-sip/%{name}-%{version}.tar.gz
# Source0-md5:	ae9e8be12f62552a5376edd66b0265d9
Patch0:		antlr_jar.patch
URL:		http://www.linphone.org/
%{?with_tests:BuildRequires:	CUnit >= 2.0}
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	java
BuildRequires:	java-antlr3 >= 3.2
BuildRequires:	libantlr3c-devel >= 3.2
BuildRequires:	libtool
BuildRequires:	polarssl-devel >= 1.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Belle-sip is a SIP (RFC3261) implementation written in C, with an
object oriente d API.

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
	%{!?with_static_libs:--disable-static}

%{__make} V=1

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install V=1 \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/libbellesip.la

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
