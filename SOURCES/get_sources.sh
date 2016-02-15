#!/bin/bash

echo 'downloading sources'
echo '-------------------'

version=`rpm -qa \*-release | grep -Ei "redhat|centos" | cut -d"-" -f3`

srcs=()
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver/2.8/geoserver.war")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geoserver_data-geogig_od3.zip")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/geogig-cli-app-1.0.zip")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/otp-OTP-18.2.1.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/libkml-1.2.0-svn-28-aug-2015.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/lcms2-2.7.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/openjpeg-2.1.0.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/gdal-2.0.2.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/postgis-2.2.1.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/apache-tomcat-8.0.32.tar.gz")
srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/mod_xsendfile-0.12.tar.bz2")

if [ $version == 7 ];then
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc48.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/swig-1.3.40.tar.gz")
else
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/MrSID_DSDK-9.5.1.4427-linux.x86-64.gcc44.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/Python-2.7.10.tgz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/setuptools-18.7.1.tar.gz")
  srcs+=("https://s3.amazonaws.com/boundlessps-public/geoshape/src/virtualenv-13.1.0.tar.gz")
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
[ ! -d pkgs ] && mkdir pkgs
pushd pkgs
while read line;
do
  name=`echo $line | awk -F '==' '{print $1}'`
  version=`echo $line | awk -F '==' '{print $2}'`
  base="https://pypi.python.org/packages/source"
  name_lc=`echo $name | tr '[:upper:]' '[:lower:]'`
  loop=1
  for ext in {.tar.gz,.zip}
  do
    urls=()
    urls+=("${base}/${name:0:1}/${name}/${name}-${version}${ext}")
    # substitute a char with alpha in version variable
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//a/alpha}${ext}")
    # substitute b char with beta in version variable
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//b/beta}${ext}")
    # modify name variable to lowercase
    urls+=("${base}/${name:0:1}/${name}/${name_lc}-${version}${ext}")
    # substitute hypens with undrscores in name variable
    urls+=("${base}/${name:0:1}/${name//-/_}/${name//-/_}-${version}${ext}")
    # pad version variable with a 0.0 for Unidecode
    urls+=("${base}/${name:0:1}/${name}/${name}-${version//0./0.0}${ext}")
    for url in "${urls[@]}"
    do
      filename=`echo $url | sed 's/.*\///'`
      if [[ `wget -S --spider $url  2>&1 | grep 'HTTP/1.1 200 OK'` ]]
      then
        if [[ ! -f $filename ]]
        then
          wget $url
          loop=0
          break
        else
          echo $filename "already downloaded"
          loop=0
          break
        fi
      fi
    done
    [ $loop -eq 0 ] && break
  done
  [ $loop -eq 1 ] && echo $name-$version "not found" >> missing-packages.txt
done < ../requirements.txt
cp -f geoshape-* ..
popd
[ -f pkgs.zip ] && rm -f pkgs.zip
zip -r pkgs.zip pkgs -x "*.DS_Store"
echo '-------------------'
echo 'finished get sources'
