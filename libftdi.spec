%global	major	2
%global	api	1
%global	libname	%mklibname ftdi %{api} %{major}
%global	libcpp	%mklibname ftdip %{api} %{major}
%global	devname	%mklibname ftdi %{api} -d

Summary:	Library to program and control the FTDI USB controller
Name:		libftdi
Version:	1.5
Release:	1
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/en/developer/%{name}/download/%{name}1-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libconfuse)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(python)
Requires(pre):	shadow-utils
Conflicts:	%{_lib}ftdi1 < 0.20-2

%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%files
%{_bindir}/ftdi_eeprom
%config(noreplace) %{_udevrulesdir}/*-libftdi.rules

%pre
getent group plugdev >/dev/null || groupadd -r plugdev
exit 0

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library to program and control the FTDI USB controller
Group:		System/Libraries

%description -n %{libname}
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%files -n %{libname}
%{_libdir}/libftdi1.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{libcpp}
Summary:	Libftdi library C++ binding
Group:		Development/C++

%description -n %{libcpp}
Libftdi library C++ language binding.

%files -n %{libcpp}
%{_libdir}/libftdipp1.so.%{major}*
%{_libdir}/libftdipp1.so.3

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and static libraries for libftdi
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libcpp} = %{EVRD}
%rename		%{_lib}ftdi-devel

%description -n %{devname}
Header files and static libraries for libftdi

%files -n %{devname}
%doc AUTHORS ChangeLog README
%doc %{_datadir}/libftdi/examples
%{_bindir}/libftdi1-config
%{_libdir}/libftdi1.so
%{_libdir}/libftdi1.a
%{_libdir}/libftdipp1.so
%{_libdir}/libftdipp1.a
%dir %{_includedir}/libftdi1
%{_includedir}/libftdipp1/*hpp
%{_includedir}/libftdi1/*.h
%{_libdir}/pkgconfig/libftdi1.pc
%{_libdir}/pkgconfig/libftdipp1.pc
%{_libdir}/cmake/libftdi1

#----------------------------------------------------------------------------

%package -n	python-%{name}
Summary:	Libftdi library Python binding
Group:		Development/Python

%description -n	python-%{name}
Libftdi Python Language bindings.

%files -n python-%{name}
%{py_platsitedir}/ftdi1.py
%{py_platsitedir}/_ftdi1.so
%{py_platsitedir}/__pycache__/*

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}1-%{version}
#kernel does not provide usb_device anymore
sed -e 's/usb_device/usb/g' -i packages/99-libftdi.rules
sed -e 's/GROUP="plugdev"/TAG+="uaccess"/g' -i packages/99-libftdi.rules
%autopatch -p1

%build
%cmake -DFTDIPP=ON -DPYTHON_BINDINGS=ON
%make_build

%install
%make_install -C build

# Cleanup examples
rm -f %{buildroot}%{_bindir}/simple
rm -f %{buildroot}%{_bindir}/bitbang
rm -f %{buildroot}%{_bindir}/bitbang2
rm -f %{buildroot}%{_bindir}/bitbang_ft2232
rm -f %{buildroot}%{_bindir}/bitbang_cbus
rm -f %{buildroot}%{_bindir}/find_all
rm -f %{buildroot}%{_bindir}/find_all_pp
rm -f %{buildroot}%{_bindir}/baud_test
rm -f %{buildroot}%{_bindir}/serial_read
rm -f %{buildroot}%{_bindir}/serial_test
rm -rf %{buildroot}%{_datadir}/doc/libftdi1/example.conf
rm -rf %{buildroot}%{_datadir}/doc/libftdipp1/example.conf
	
mkdir -p %{buildroot}/lib/udev/rules.d/
install -pm 0644 packages/99-libftdi.rules %{buildroot}/lib/udev/rules.d/69-libftdi.rules


# fix includes
sed -i 's!#include <ftdi.h>!#include <libftdi1/ftdi.h>!g' %{buildroot}%{_includedir}/libftdipp1/ftdi.hpp
