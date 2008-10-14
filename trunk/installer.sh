#!/bin/sh

wget 
mkdir -vp /usr/share/lastagent
cp -vf lastagent /usr/bin
chmod a+x /usr/bin/lastagent
##cp -vf pylast.py /usr/lib/python2.5/site-packages
cp -vf lastagent.desktop /usr/share/applications
cp * -rvf /usr/share/lastagent
