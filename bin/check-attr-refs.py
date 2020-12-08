#!/usr/bin/python -u

import sys
import os
import re
import argparse
import subprocess
import shutil


if __name__ == "__main__":
    count_not_used = 0
    count_dep_refs = 0
    count_rm_refs = 0
    attr_declared = {}
    deprecated_attr = []
    removed_attr = []
    index_files = ["pmix-standard.idx", "index_attribute.idx"]

    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard Attribute Reference Check")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-f", "--fyi", help="FYI References (not errors)", action="store_true")

    parser.parse_args()
    args = parser.parse_args()


    #
    # Verify that we have the necessary files in the current working directory
    # * pmix-standard.aux
    # * index_files - see above
    #
    missing_index = False
    for fname in index_files:
        if os.path.exists(fname) is False:
            missing_index = True
    if os.path.exists("pmix-standard.aux") is False or missing_index is True:
        print("Error: Cannot find the .aux or .idx files necessary for processing in the current directory.")
        print("       Please run this script from the base PMIx Standard build directory, and with a recent build.")
        sys.exit(1)


    #
    # Extract the declared attributes
    #   grep "newlabel{attr" pmix-standard.aux
    #
    if args.verbose is True:
        print("-"*50)
        print("Extracting declared attributes")
        print("-"*50)

    p = subprocess.Popen("grep \"newlabel{attr\" pmix-standard.aux",
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
    sout = p.communicate()[0].decode("utf-8").splitlines()
    if p.returncode != 0:
        print("Error: Failed to extract declared attributes. grep error code "+str(p.returncode)+")");
        sys.exit(2)

    for line in sout:
        line = line.rstrip()
        m = re.match(r'\s*\\newlabel{attr:(\w+)', line)
        if m is None:
            print("Error: Failed to extract an attribute on the following line")
            print(" line: "+line)
            sys.exit(1)
        # Count will return to 0 when verified
        attr_declared[m.group(1)] = -1

    p.wait()

    if args.verbose is True:
        for attr in attr_declared:
            print("Attribute: " + attr)
        print("Number of declared attributes: " + str(len(attr_declared)))


    #
    # Verify the list against the index
    # If any difference then post a warning
    #
    if args.verbose is True:
        print("-"*50)
        print("Verifying list against the index")
        print("-"*50)


    for fname in index_files:
        if os.path.exists(fname) is False:
            continue
        if args.verbose is True:
            print("Processing Index File: "+fname)

        p = subprocess.Popen("grep \"hyperindexformat{\" "+fname+" | sort",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
        sout = p.communicate()[0].decode("utf-8").splitlines()

        if p.returncode != 0:
            print("Error: Failed to verify declared attribute \""+attr+"\". grep error code "+str(p.returncode)+"");
            sys.exit(2)

        for line in sout:
            line = line.rstrip()

            m = re.match(r'\s*\\indexentry{(\w+)', line)
            if m is None:
                print("Error: Failed to extract an attribute on the following line")
                print(" line: "+line)
                sys.exit(1)
            else:
                attr_to_find = m.group(1)

                # Some index entries have a prefix on them for sorting order, so
                # access the actual printed string not the sorting version of
                # the string.
                m2 = re.match(r'\s*\\indexentry{(\w+)@(\w+)', line)
                if m2 is not None:
                    attr_to_find = m2.group(2)

                # Check to see if this is deprecated
                if re.search("(Deprecated)", line) is not None:
                    if args.verbose is True:
                        print("Found a Deprecated Attribute: "+attr_to_find)
                    deprecated_attr.insert(0, attr_to_find)

                # Check to see if this is removed
                if re.search("(Removed)", line) is not None:
                    if args.verbose is True:
                        print("Found a Removed Attribute: "+attr_to_find)
                    removed_attr.insert(0, attr_to_find)

                if attr_to_find in attr_declared:
                    attr_declared[attr_to_find] = attr_declared[attr_to_find] + 1
        p.wait()

    # Sanity check. Should never trigger, but check just in case
    err_out = False
    num_missing = 0
    for attr in attr_declared:
        if attr_declared[attr] < 0:
            print("Error: Attribute \""+attr+"\" declared, but not in the index")
            err_out = True
            num_missing += 1
    if err_out is True:
        print("-"*50)
        print("Number of deprecated attributes: " + str(len(deprecated_attr)))
        print("Number of removed attributes   : " + str(len(removed_attr)))
        print("Number of declared attributes  : " + str(len(attr_declared)))
        print("Number of missing attributes   : " + str(num_missing))
        sys.exit(1)

    if args.verbose is True:
        print("Verified all "+str(len(attr_declared))+" attributes are present in the index")


    #
    # Look for usage references for each attribute
    #   grep "\|hyperpage" pmix-standard.idx
    #
    if args.verbose is True:
        print("-"*50)
        print("Count the usage of each attribute in the document")
        print("-"*50)

    for fname in index_files:
        if os.path.exists(fname) is False:
            continue
        if args.verbose is True:
            print("Processing Index File: "+fname)

        # Result set was too big for Python to handle, so use an intermediate file
        output_file = "pmix-standard.idx-grep"
        with open(output_file, 'w') as logfile:
            ret = subprocess.call(['grep', '\|hyperpage', fname],
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
    for attr in sorted(attr_declared):
        if attr_declared[attr] <= 0:
            if attr not in deprecated_attr and attr not in removed_attr and attr != "PMIX_ATTR_UNDEF":
                print("Attribute Missing Reference: "+attr)
                count_not_used += 1
        elif attr in deprecated_attr and attr in removed_attr and attr_declared[attr] == 1:
            # There is an entry for the deprecation and the removal. This is fine
            continue
        elif attr in deprecated_attr or attr in removed_attr:
            # Allow references within the Chap_Revisions.tex - count them
            num_in_chap_revisions = 0
            p = subprocess.Popen("grep \"refattr{"+attr+"}\" Chap_Revisions.tex | wc -l",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
            sout = p.communicate()[0].decode("utf-8").splitlines()
            if p.returncode != 0:
                print("Error: Failed to verify declared attribute \""+attr+"\". grep error code "+str(p.returncode)+"");
                sys.exit(2)
            for line in sout:
                line = line.rstrip()
                num_in_chap_revisions = int(line)

            # Extra increment for deprecated and removed items
            if attr in deprecated_attr and attr in removed_attr:
                num_in_chap_revisions += 1

            # If there are other references outside of the Revisions chapter then error out
            if attr_declared[attr] - num_in_chap_revisions > 0:
                if attr in deprecated_attr:
                    print("Deprecated Attribute: "+attr+" (Referenced "+str(attr_declared[attr]-num_in_chap_revisions)+" times)")
                    count_dep_refs += 1
                elif attr in removed_attr:
                    print("Removed    Attribute: "+attr+" (Referenced "+str(attr_declared[attr]-num_in_chap_revisions)+" times)")
                    count_rm_refs += 1

    #
    # Additional analysis for optional, non-error reporting
    #
    if args.fyi is True:
        for attr in sorted(removed_attr):
            if attr not in deprecated_attr:
                print("Removed attribute that was not deprecated: "+attr);
        
    #
    # Final summary
    #
    print("%3d of %3d Attributes are missing reference" % (count_not_used, len(attr_declared)))
    print("%3d of %3d Deprecated Attributes with references remaining" % (count_dep_refs, len(deprecated_attr)))
    print("%3d of %3d Removed Attributes with references remaining" % (count_rm_refs, len(removed_attr)))

    sys.exit(count_not_used + count_dep_refs + count_rm_refs)
