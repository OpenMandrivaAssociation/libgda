%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define _disable_rebuild_configure 1

%define build_mysql 1
%{?_with_mysql: %global build_mysql 1}

%define enable_test 0

%define api 5.0
%define major 4
%define pkgname %{name}%{api}
%define oname gda

%define libname %mklibname %{oname} %{api} %{major} 
%define libnamereport %mklibname %{oname}-report %{api} %{major}
%define libnameui %mklibname %{oname}-ui %{api} %{major}
%define libnamexslt %mklibname %{oname}-xslt %{api} %{major}
%define girname %mklibname %{oname}-gir %{api}
%define girnameui %mklibname %{oname}ui-gir %{api}
%define devname %mklibname -d %{oname} %{api}

Summary:	GNU Data Access
Name:		libgda
Version:	5.2.9
Release:	1
License:	GPLv2+ and LGPLv2+
Group:		Databases
Url:		http://www.gnome-db.org/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Patch1:		libgda-5.1.1-linkage.patch
#Patch2:		libgda-5.1.2-fix-str-fmt.patch

BuildRequires:	bison
BuildRequires:	yelp-tools
BuildRequires:	flex
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	db-devel
BuildRequires:	gdbm-devel
BuildRequires:	openldap-devel
BuildRequires:	postgresql-devel
BuildRequires:	readline-devel
BuildRequires:	unixODBC-devel
BuildRequires:	xbase-devel
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(goocanvas)
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(gtksourceview-3.0)
BuildRequires:	pkgconfig(iso-codes)
BuildRequires:	pkgconfig(libcrypto)
BuildRequires:	pkgconfig(libgvc)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(popt)
BuildRequires:	pkgconfig(sqlite3) >= 3.7.15.2
%if %{build_mysql}
BuildRequires:	mysql-devel
%endif
%if %{enable_test}
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(check)
%endif

Requires:	iso-codes

%description
GNU Data Access is an attempt to provide uniform access to
different kinds of data sources (databases, information
servers, mail spools, etc).
It is a complete architecture that provides all you need to
access your data.

%package -n	%{pkgname}
Summary:	GNU Data Access Development
Group: 		Databases

%description -n	%{pkgname}
GNU Data Access is an attempt to provide uniform access to
different kinds of data sources (databases, information
servers, mail spools, etc).
It is a complete architecture that provides all you need to
access your data.

%package -n	%{libname}
Summary:	GNU Data Access Development
Group: 		System/Libraries
Provides:	libgda = %{EVRD}

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	%{libnamereport}
Summary:	GNU Data Access Development
Group: 		System/Libraries

%description -n	%{libnamereport}
This package contains the shared library for %{name}.

%package -n	%{libnameui}
Summary:	GNU Data Access Development
Group: 		System/Libraries

%description -n	%{libnameui}
This package contains the shared library for %{name}.

%package -n	%{libnamexslt}
Summary:	GNU Data Access Development
Group: 		System/Libraries

%description -n	%{libnamexslt}
This package contains the shared library for %{name}.

%package -n %{girname}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{girnameui}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries

%description -n %{girnameui}
GObject Introspection interface description for %{name}.

%package -n	%{devname}
Summary:	GNU Data Access Development
Group: 		Development/Databases
Requires:	%{libname} = %{EVRD}
Requires:	%{libnamereport} = %{EVRD}
Requires:	%{libnameui} = %{EVRD}
Requires:	%{libnamexslt} = %{EVRD}
Requires:	%{girname} = %{EVRD}
Requires:	%{girnameui} = %{EVRD}
Provides:	%{oname}%{api}-devel = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n	%{devname}
This package contains the development files for %{name}.

%package -n	%{pkgname}-postgres
Summary:	GDA PostgreSQL Provider
Group:		Databases
Requires:	%{name} = %{EVRD}

%description -n	%{pkgname}-postgres
This package includes the GDA PostgreSQL provider

%package -n	%{pkgname}-mysql
Summary:	GDA MySQL Provider
Group:		Databases
Requires:	%{name} = %{EVRD}

%description -n	%{pkgname}-mysql
This package includes the GDA MySQL provider

%package -n	%{pkgname}-bdb
Summary:	GDA Berkeley Database Provider
Group:		Databases
Requires:	%{name} = %{EVRD}

%description -n	%{pkgname}-bdb
This package includes the GDA Berkeley Database provider.

%package -n	%{pkgname}-sqlite
Summary:	GDA sqlite Provider
Group:		Databases
Requires:	%{name} = %{EVRD}
Obsoletes:      gda3.0-sqlite

%description -n	%{pkgname}-sqlite
This package includes the GDA sqlite provider

%package -n	%{pkgname}-ldap
Summary:	GDA LDAP Provider
Group:		Databases
Requires:	%{name} = %{EVRD}

%description -n	%{pkgname}-ldap
This package includes the GDA LDAP provider

%prep
%setup -q
%autopatch -p1
aclocal
automake -a
autoconf

%build
export CC=gcc
export CXX=g++
export CPPFLAGS+=' -I/usr/include/graphviz'
%configure2_5x \
	--disable-static \
	--enable-introspection=yes \
	--enable-gda-gi \
	--enable-gdaui-gi \
	--enable-system-sqlite \
%if %build_mysql
	--with-mysql=yes \
%endif
	--without-firebird \
	--with-bdb=%{_prefix} \
	--with-bdb-libdir-name=%{_lib}

%make LIBS='-ldl'

%install
%makeinstall_std
%find_lang %{name}-%{api} --with-gnome --all-name

%if %{enable_test}
%check
make check
%endif

%files -n %{pkgname} -f %{name}-%{api}.lang
%doc AUTHORS COPYING README
%dir %{_sysconfdir}/libgda-%{api}
%config(noreplace) %_sysconfdir/libgda-%{api}/sales_test.db
%config(noreplace) %{_sysconfdir}/libgda-%{api}/config
%{_bindir}/*
%{_datadir}/applications/gda-browser-%{api}.desktop
%{_datadir}/applications/gda-control-center-%{api}.desktop
%{_datadir}/pixmaps/gda*
%{_datadir}/icons/hicolor/*/apps/gda-control-center.*
%{_datadir}/libgda-%{api}
%exclude %{_datadir}/libgda-%{api}/demo
%dir %{_libdir}/libgda-%{api}
%dir %{_libdir}/libgda-%{api}/plugins
%dir %{_libdir}/libgda-%{api}/providers
%{_libdir}/libgda-%{api}/plugins/*.xml
%{_libdir}/libgda-%{api}/plugins/libgda-ui-plugins.so
%{_libdir}/libgda-%{api}/providers/libgda-web.so
%{_libdir}/libgda-%{api}/providers/libgda-sqlcipher.so
%{_mandir}/man1/*
%{_datadir}/appdata/gda-browser-5.0.appdata.xml


%files -n %{libname}
%{_libdir}/libgda-%{api}.so.%{major}*

%files -n %{libnamereport}
%{_libdir}/libgda-report-%{api}.so.%{major}*

%files -n %{libnameui}
%{_libdir}/libgda-ui-%{api}.so.%{major}*

%files -n %{libnamexslt}
%{_libdir}/libgda-xslt-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Gda-%{api}.typelib

%files -n %{girnameui}
%{_libdir}/girepository-1.0/Gdaui-%{api}.typelib

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/libgda-%{api}/
%doc %{_datadir}/gtk-doc/html/gda-browser
%{_libdir}/libgda-%{api}.so
%{_libdir}/libgda-report-%{api}.so
%{_libdir}/libgda-ui-%{api}.so
%{_libdir}/libgda-xslt-%{api}.so
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/libgda-%{api}/demo
%{_datadir}/gir-1.0/Gda-%{api}.gir
%{_datadir}/gir-1.0/Gdaui-%{api}.gir

%files -n %{pkgname}-sqlite
%{_libdir}/libgda-%{api}/providers/libgda-sqlite.so

%files -n %{pkgname}-postgres
%{_libdir}/libgda-%{api}/providers/libgda-postgres.so

%files -n %{pkgname}-bdb
%{_libdir}/libgda-%{api}/providers/libgda-bdb.so

%if %{build_mysql}
%files -n %{pkgname}-mysql
%{_libdir}/libgda-%{api}/providers/libgda-mysql.so
%endif

%files -n %{pkgname}-ldap
%{_libdir}/libgda-%{api}/providers/libgda-ldap.so

