# -*- coding:utf-8 -*-

# alter http headers
#

import sys
import httplib2

if len(sys.argv) < 2:
    print sys.argv[0] + "<url>"
    sys.exit(1)

webclient = httplib2.Http()
header, content = webclient.request(sys.argv[1], "GET")

for filed, value in header.items():
    print filed + ": " + value
