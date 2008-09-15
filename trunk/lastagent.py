#!/usr/bin/env python

import application
import sys

hidden = False
if '--hidden' in sys.argv:
	hidden = True

a = application.Application()
a.run(hidden)

