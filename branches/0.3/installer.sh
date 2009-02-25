#!/bin/sh

mkdir -vp /usr/share/lastagent
cp -vf lastagent /usr/bin
chmod a+x /usr/bin/lastagent
cp -vf lastagent.desktop /usr/share/applications
cp * -rvf /usr/share/lastagent
