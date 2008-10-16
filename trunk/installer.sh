#!/bin/sh

wget http://pylast.googlecode.com/files/pyLast-0.2b12.tar.gz
tar -xf pyLast*.tar.gz
cd pyLast*
python setup.py install

mkdir -vp /usr/share/lastagent
cp -vf lastagent /usr/bin
chmod a+x /usr/bin/lastagent
cp -vf lastagent.desktop /usr/share/applications
cp * -rvf /usr/share/lastagent
