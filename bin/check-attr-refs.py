#!/usr/bin/python -u

import sys
import os
import re
import argparse
import subprocess
import shutil


if __name__ == "__main__":
    count_not_used = 0
    attr_declared = {}

    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard Attribute Reference Check")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    parser.parse_args()
    args = parser.parse_args()


    #
    # Verify that we have the necessary files in the current working directory
    # * pmix-standard.aux
    # * pmix-standard.idx
    #
    if os.path.exists("pmix-standard.aux") is False or os.path.exists("pmix-standard.idx") is False:
        print("Error: Cannot find the .aux or .idx files necessary for processing in the current directory.")
        print("       Please run this script from the base PMIx Standard build directory, and with a recent build.")
        sys.exit(1)


    #
    # Extract the declared attributes
    #   grep "newlabel{attr" pmix-standard.aux
    #
    if args.verbose is True:
        print "-"*50
        print "Extracting declared attributes"
        print "-"*50

    p = subprocess.Popen("grep \"newlabel{attr\" pmix-standard.aux",
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
    p.wait()
    if p.returncode != 0:
        print("Error: Failed to extract declared attributes. grep error code "+str(p.returncode)+")");
        sys.exit(2)

    for line in p.stdout:
        line = line.rstrip()
        m = re.match(r'\s*\\newlabel{attr:(\w+)', line)
        if m is None:
            print("Error: Failed to extract an attribute on the following line")
            print(" line: "+line)
            sys.exit(1)
        # Count will return to 0 when verified
        attr_declared[m.group(1)] = -1

    if args.verbose is True:
        for attr in attr_declared:
            print("Attribute: " + attr)
        print("Number of declared attributes: " + str(len(attr_declared)))


    #
    # Verify the list against the index
    # If any difference then post a warning
    #  grep "PMIX_SERVER_REMOTE_CONNECTIONS\!Def" pmix-standard.idx
    #
    if args.verbose is True:
        print "-"*50
        print "Verifying list against the index"
        print "-"*50

    p = subprocess.Popen("grep \"\\!Definition\" pmix-standard.idx",
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
    p.wait()
    if p.returncode != 0:
        print("Error: Failed to verify declared attribute \""+attr+"\". grep error code "+str(p.returncode)+")");
        sys.exit(2)

    # List of Definition is larger than attribute list
    for line in p.stdout:
        line = line.rstrip()
        m = re.match(r'\s*\\indexentry{(\w+)', line)
        if m is None:
            print("Error: Failed to extract an attribute on the following line")
            print(" line: "+line)
            sys.exit(1)

        attr_to_find = m.group(1)
        if attr_to_find in attr_declared:
            attr_declared[attr_to_find] = attr_declared[attr_to_find] + 1

    # Sanity check. Should never trigger, but check just in case
    err_out = False
    for attr in attr_declared:
        if attr_declared[attr] < 0:
            print("Error: Attribute \""+attr+"\" declared, but not in the index")
            err_out = True
    if err_out is True:
        sys.exit(1)

    if args.verbose is True:
        print("Verified all "+str(len(attr_declared))+" attributes are present in the index")


    #
    # Look for usage references for each attribute
    #   grep "\|hyperpage" pmix-standard.idx
    #
    if args.verbose is True:
        print "-"*50
        print "Count the usage of each attribute in the document"
        print "-"*50

    # Result set was too big for Python to handle, so use an intermediate file
    output_file = "pmix-standard.idx-grep"
    with open(output_file, 'w') as logfile:
        ret = subprocess.call(['grep', '\|hyperpage', 'pmix-standard.idx'],
                              stdout=logfile, stderr=logfile, shell=False)
        if ret != 0:
            print("Error: Failed to verify declared attribute \""+attr+"\". grep error code "+str(ret)+")");
            sys.exit(2)

    # List of references is much larger than attribute list
    with open(output_file, 'r') as logfile:
        for line in logfile:
            line = line.rstrip()
            m = re.match(r'\s*\\indexentry{(\w+)', line)
            if m is None:
                print("Error: Failed to extract an attribute on the following line")
                print(" line: "+line)
                sys.exit(1)

            attr_to_find = m.group(1)
            if attr_to_find in attr_declared:
                attr_declared[attr_to_find] = attr_declared[attr_to_find] + 1

    if os.path.isfile(output_file):
        os.remove(output_file)


    #
    # Display a list of attributes that are declared but not used
    #
    for attr in attr_declared:
        if attr_declared[attr] <= 0:
            print("Attribute Missing Reference: "+attr)
            count_not_used += 1

    print("%3d of %3d Attributes are missing reference" % (count_not_used, len(attr_declared)))
    sys.exit(count_not_used)
