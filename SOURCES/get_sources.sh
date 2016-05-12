#!/bin/bash

echo 'downloading sources'
echo '-------------------'

version=`rpm -qa \*-release | grep -Ei "redhat|centos" | cut -d"-" -f3`

srcs=()
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/otp-OTP-18.2.1.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/libkml-1.2.0-svn-28-aug-2015.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/lcms2-2.7.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/openjpeg-2.1.0.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/gdal-2.1.0.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/postgis-2.2.2.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/apache-tomcat-8.0.33.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/mod_xsendfile-0.12.tar.bz2")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver/2.8/geoserver.war")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver_data-geogig_od3.zip")

if [ $version == 7 ];then
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc48.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/swig-1.3.40.tar.gz")
else
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc44.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/Python-2.7.11.tgz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/setuptools-20.9.0.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/virtualenv-15.0.1.tar.gz")
fi

for src in "${srcs[@]}"
do
  filename=`echo $src | sed 's/.*\///'`
  if [[ ! -f $filename ]]
  then
    wget $src
  else
    echo $filename "already downloaded"
  fi
done

echo '-------------------'
echo 'finished get sources'
