Summary: Geospatial Data Abstraction Library
Name: gdal
Version: 2.1.2
Release: 1%{?dist}
License: MIT/X
Group: Applications/Engineering
URL: http://www.gdal.org/

%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%if 0%{?rhel} == 6
%define mrsid_name MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc44
%elseif 0%{?rhel} == 7
%define mrsid_name MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc48
%endif

Source0: http://download.osgeo.org/gdal/gdal-%{version}.tar.gz
Source1: %{mrsid_name}.tar.gz
BuildRequires: gcc
BuildRequires: geos-devel >= 3.3.3
BuildRequires: proj-devel
BuildRequires: curl-devel
BuildRequires: expat-devel
BuildRequires: sqlite-devel
BuildRequires: libkml-devel
BuildRequires: openjpeg2-devel
BuildRequires: postgresql96-devel
BuildRequires: poppler-devel
BuildRequires: xerces-c-devel
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: ant
BuildRequires: chrpath
BuildRequires: libtool
%{?el6:BuildRequires: swig}
%{?el6:BuildRequires: python27-devel}
%{?el7:BuildRequires: python-devel}
%{?el7:BuildRequires: swig = 1.3.40}

Requires: geos >= 3.3.3
%{?el6:Requires: swig}
%{?el7:Requires: swig = 1.3.40}
Requires: proj
Requires: poppler
Requires: postgresql96-libs
Requires: expat
Requires: curl
Requires: sqlite
Requires: xerces-c
Requires: libkml
Requires: openjpeg2
Requires: proj-devel

Patch0: gdal_driverpath.patch
Patch1: gdal_GDALmake.opt.in.patch

%description
The Geospatial Data Abstraction Library (GDAL) is a unifying C/C++ API for 
accessing raster geospatial data, and currently includes formats like 
GeoTIFF, Erdas Imagine, Arc/Info Binary, CEOS, DTED, GXF, and SDTS. It is 
intended to provide efficient access, suitable for use in viewer 
applications, and also attempts to preserve coordinate systems and 
metadata. Perl, C, and C++ interfaces are available.

# gdal-devel
%package devel
Summary: Header files, libraries and development documentation for %{name}.
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%package python
Summary: Python bindings for gdal and ogr
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
%{?el6:Requires: python27}
%{?el7:Requires: python}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%description python
This package contains Python bindings for GDAL/OGR library.

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/*.h

%prep
%setup
%ifarch x86_64
# In RedHat land, 32-bit libs go in /usr/lib and 64-bit ones go in /usr/lib64.
# The default driver search paths need changing to reflect this.
%patch0
%endif
%patch1

%build

sed -i 's|@LIBTOOL@|%{_bindir}/libtool|g' GDALmake.opt.in
tar -xf %{SOURCE1} -C .
# copying mrsid and mrsid_lidar lib and include to /usr/local because build fails if we point at location within the build directory
/bin/cp -rf %{_builddir}/%{name}-%{version}/%{mrsid_name}/Lidar_DSDK/lib/* /usr/local/lib
/bin/cp -rf %{_builddir}/%{name}-%{version}/%{mrsid_name}/Lidar_DSDK/include/* /usr/local/include
/bin/cp -rf %{_builddir}/%{name}-%{version}/%{mrsid_name}/Raster_DSDK/lib/* /usr/local/lib
/bin/cp -rf %{_builddir}/%{name}-%{version}/%{mrsid_name}/Raster_DSDK/include/* /usr/local/include

%if 0%{?rhel} == 6
%configure --datadir=/usr/share/gdal --disable-static --with-pg=/usr/pgsql-9.6/bin/pg_config --disable-rpath --with-mrsid=/usr/local  --with-mrsid_lidar=/usr/local --with-spatialite --with-curl --with-expat --with-python=/usr/local --with-java
%elseif 0%{?rhel} == 7
%configure --datadir=/usr/share/gdal --disable-static --with-pg=/usr/pgsql-9.6/bin/pg_config --disable-rpath --with-mrsid=/usr/local  --with-mrsid_lidar=/usr/local --with-spatialite --with-curl --with-expat --with-python --with-java
%endif

make
make %{?_smp_mflags}

# Java SWIG bindings
cd swig/java
sed -i '1iJAVA_HOME=/usr/lib/jvm/java-openjdk' java.opt
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

%ifarch x86_64 # 32-bit libs go in /usr/lib while 64-bit libs go in /usr/lib64
%define lib_dir /usr/lib64
%else
%define lib_dir /usr/lib
%endif
mkdir -p %{buildroot}/%{lib_dir}/gdalplugins
cp %{mrsid_name}/Raster_DSDK/lib/libltidsdk.so* %{buildroot}/%{lib_dir}
cp %{mrsid_name}/Lidar_DSDK/lib/liblti_lidar_dsdk.so* %{buildroot}/%{lib_dir}
cp %{mrsid_name}/Lidar_DSDK/lib/liblaslib.so %{buildroot}/%{lib_dir}
# Remove RPATHs
chrpath -d swig/java/*.so
cp swig/java/*.so %{buildroot}%{lib_dir}
cp swig/java/gdal.jar %{buildroot}%{lib_dir}/gdal-%{version}.jar

%clean
rm -rf %{buildroot}
rm -f /usr/local/lib/{libgeos*,libltidsdk*,libtbb*,liblti_lidar_dsdk*,liblaslib.so} && rm -f /usr/local/include/*.h && rm -rf /usr/local/include/{lidar,nitf}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, 0755)
%{_bindir}/*
%{_datadir}/gdal/
%{_libdir}/lib*
%{_libdir}/gdal-%{version}.jar
%{_libdir}/pkgconfig/gdal.pc

%files python
%defattr(-,root,root,-)
%{python_sitearch}
%{_bindir}/*.py

%changelog
* Sat Nov 12 2016 amirahav <arahav@boundlessgeo.com> [2.1.2-1]
- Bump to 2.1.2 and Postgres 9.6
* Tue Jul 5 2016 amirahav <arahav@boundlessgeo.com> [2.1.0-2]
- Add python support
- require proj-devel because proj is missing libproj.so
* Wed May 11 2016 amirahav <arahav@boundlessgeo.com> [2.1.0-1]
- Upgraded to GDAL 2.1.0
* Fri Feb 5 2016 amirahav <arahav@boundlessgeo.com> [2.0.2-1]
- Upgraded to GDAL 2.0.2
- Added MrSID/MrSID LiDAR
* Sat Jan 16 2016 amirahav <arahav@boundlessgeo.com> [2.0.1-2]
- Upgraded PostgreSQL to 9.5
* Sat Jan 16 2016 BerryDaniel <dberry@boundlessgeo.com> [2.0.1-1]
- Upgraded GDAL to 2.0.1
- Upgraded java to 1.8