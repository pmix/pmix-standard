#!/usr/bin/env python3

from pmix import *

def main():
    #<EG BEGIN ID="pmix_init">
    client_hdl = PMIxClient()
    #<EG END ID="pmix_init">
    print("Testing PMIx ", client_hdl.get_version())

    print("Init")
    #<EG BEGIN ID="pmix_init">
    info = []
    (rc,myproc) = client_hdl.init(info)
    if 0 != rc:
        exit(1)
    #<EG END ID="pmix_init">

    print("Get")
    info = []
    rc, get_val = client_hdl.get(myproc, "PMIX_LOCAL_RANK", info)
    print("Get result: ", rc)
    print("Get value returned: ", get_val)

    print("Finalize")
    info = []
    client_hdl.finalize(info)

if __name__ == '__main__':
    main()
