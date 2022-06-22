%global major 2
%global api 1
%global libname %mklibname ftdi %{api} %{major}
%global libcpp %mklibname ftdip %{api} %{major}
%global devname %mklibname ftdi %{api} -d

Summary:	Library to program and control the FTDI USB controller
Name:		libftdi
Version:	1.5
Release:	3
License:	GPLv2+
Group:		System/Libraries
Url:		http://www.intra2net.com/de/produkte/opensource/ftdi/
Source0:	http://www.intra2net.com/en/developer/%{name}/download/%{name}1-%{version}.tar.bz2
# http://developer.intra2net.com/git/?p=libftdi;a=commitdiff;h=cdb28383402d248dbc6062f4391b038375c52385;hp=5c2c58e03ea999534e8cb64906c8ae8b15536c30
Patch0:		libftdi-1.5-fix_pkgconfig_path.patch
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	swig
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libconfuse)
BuildRequires:	pkgconfig(libusb)
BuildRequires:	pkgconfig(python)
Conflicts:	%{_lib}ftdi1 < 0.20-2

%description
A library (using libusb) to talk to FTDI's FT2232C,
FT232BM and FT245BM type chips including the popular bitbang mode.

%files
%{_bindir}/ftdi_eeprom
%config(noreplace) %{_udevrulesdir}/*-libftdi.rules

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library to program and control the FTDI USB controller
Group:		System/Libraries
Requires:	%{name}

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
%{_libdir}/*.so
%{_libdir}/*.a
%dir %{_includedir}/libftdi1
%{_includedir}/libftdi1/*.hpp
%{_includedir}/libftdi1/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/libftdi1

#----------------------------------------------------------------------------

%package -n python-%{name}
Summary:	Libftdi library Python binding
Group:		Development/Python

%description -n python-%{name}
Libftdi Python Language bindings.

%files -n python-%{name}
%{py_platsitedir}/ftdi1.py
%{py_platsitedir}/_ftdi1.so

#----------------------------------------------------------------------------

%prep
%autosetup -n %{name}1-%{version} -p1
# switch to uaccess control
sed -i -e 's/GROUP="plugdev"/TAG+="uaccess"/g' packages/99-libftdi.rules

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

install -D -pm 0644 packages/99-libftdi.rules %{buildroot}%{_udevrulesdir}/69-libftdi.rules

# fix includes
sed -i 's!#include <ftdi.h>!#include <libftdi1/ftdi.h>!g' %{buildroot}%{_includedir}/libftdi1/ftdi.hpp
