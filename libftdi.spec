%global	major	1
%global	minor	20
%global	micro	0
%global	libname	%mklibname ftdi %{major}
%global	devname	%mklibname -d ftdi
%global	libcpp	%mklibname ftdip %{major}

Name:		libftdi
Version:	0.20
Release:	1
Summary:	Library to program and control the FTDI USB controller

Group:		System/Libraries
License:	LGPLv2
URL:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/de/produkte/opensource/ftdi/TGZ/%{name}-%{version}.tar.gz
Source1:	no_date_footer.html
Patch0:		libftdi-0.17-multilib.patch
# update to recent libusb
Patch1:		libftdi-0.19-libusb.patch
Patch2:		libftdi-0.19-fix-doxygen-errors-patch.patch

BuildRequires:	libusb-devel doxygen boost-devel python-devel swig cmake
Requires(pre):	shadow-utils

%package -n	%{libname}
Summary:	%{summary}
Group:		System/Libraries

%package -n	%{devname}
Summary:	Header files and static libraries for libftdi
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libcpp} = %{EVRD}

%package -n	python-%{name}
Summary:	Libftdi library Python binding
Group:		Development/Python

%package -n	%{libcpp}
Summary:	Libftdi library C++ binding
Group:		Development/C++

%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%description -n	%{libname}
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%description -n %{devname}
Header files and static libraries for libftdi

%description -n	python-%{name}
Libftdi Python Language bindings.

%description -n	%{libcpp}
Libftdi library C++ language binding.

%prep
%setup -q
#kernel does not provide usb_device anymore
sed -e 's/usb_device/usb/g' -i packages/99-libftdi.rules
%patch0 -p1 -b .multilib~
%patch1 -p1 -b .libusb~
%patch2 -p1 -b .doxygen~
autoreconf -if

%build
%cmake
%make

%install
%makeinstall_std -C build
#no man install
pushd build/doc/man/man3
for man in *.3; do install -p -m644 $man -D %{buildroot}%{_mandir}/man3/$man; done
popd
install -p -m644 packages/99-libftdi.rules -D %{buildroot}%{_sysconfdir}/udev/rules.d/99-libftdi.rules
# fix cmake later..
install -d %{buildroot}%{py_platsitedir}
mv %{buildroot}%{_prefix}/site-packages/* %{buildroot}%{py_platsitedir}
rmdir %{buildroot}%{_prefix}/site-packages/

%files -n %{libname}
%{_libdir}/libftdi.so.%{major}
%{_libdir}/libftdi.so.%{major}.%{minor}.%{micro}*
%config(noreplace) %{_sysconfdir}/udev/rules.d/99-libftdi.rules

%files -n %{libcpp}
%{_libdir}/libftdipp.so.%{major}
%{_libdir}/libftdipp.so.%{major}.%{minor}.%{micro}

%files -n %{devname}
%doc build/doc/html
%doc AUTHORS ChangeLog README
%{_bindir}/libftdi-config
%{_libdir}/libftdi.so
%{_libdir}/libftdi.a
%{_libdir}/libftdipp.so
%{_libdir}/libftdipp.a
%{_includedir}/*.h
%{_includedir}/*.hpp
%{_libdir}/pkgconfig/libftdi.pc
%{_libdir}/pkgconfig/libftdipp.pc
%{_mandir}/man3/*

%files -n python-%{name}
%{py_platsitedir}/ftdi.py
%{py_platsitedir}/_ftdi.so

%pre
getent group plugdev >/dev/null || groupadd -r plugdev
exit 0

