#
# Conditional build:
%bcond_with	tests		# build with tests

%define		kdeappsver	26.08.1
%define		kframever	6.0.0
%define		qtver		6.5.0
%define		kaname		kdev-php

Summary:	KDE Integrated Development Environment - php
Summary(pl.UTF-8):	Zintegrowane środowisko programisty dla KDE - php
Name:		ka6-%{kaname}
Version:	26.08.1
Release:	1
License:	GPL
Group:		X11/Development/Tools
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	e13e8cd1155e55a6c360c875cb12969f
URL:		http://www.kdevelop.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
%{?with_tests:BuildRequires:	Qt6Test-devel >= %{qtver}}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	ka6-kdevelop-devel >= %{kdeappsver}
BuildRequires:	ka6-kdevelop-pg-qt >= 2.4.0
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-threadweaver-devel >= %{kframever}
BuildRequires:	kf6-ktexteditor-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	ka6-kdevelop
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	x32 i686
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KDE Integrated Development Environment - php.

%description -l pl.UTF-8
Zintegrowane środowisko programistyczne KDE dla języka PHP.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DFORCE_BASH_COMPLETION_INSTALLATION=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%{_includedir}/kdev-php
%{_libdir}/cmake/KDevPHP
%{_libdir}/libkdevphpcompletion.so
%{_libdir}/libkdevphpduchain.so
%{_libdir}/libkdevphpparser.so
%{_libdir}/qt6/plugins/kdevplatform/6?/kdevphpdocs.so
%{_libdir}/qt6/plugins/kdevplatform/6?/kdevphplanguagesupport.so
%{_libdir}/qt6/plugins/kdevplatform/6?/kdevphpunitprovider.so
%{_datadir}/kdevappwizard/templates/simple_phpapp.tar.bz2
%dir %{_datadir}/kdevphpsupport
%{_datadir}/kdevphpsupport/phpfunctions.php
%{_datadir}/kdevphpsupport/phpunitdeclarations.php
%{_datadir}/metainfo/org.kde.kdev-php.metainfo.xml
%{_datadir}/qlogging-categories6/kdevphpsupport.categories
