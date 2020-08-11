#!/usr/bin/python -u

import sys
import os
import re
import argparse
import subprocess
import shutil


if __name__ == "__main__":
    count_not_used = 0
    std_attributes = {}
    std_macros = {}
    std_consts = {}
    std_structs = {}
    std_apis = {}
    std_all_refs = {}

    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard Double Declare Check")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")

    parser.parse_args()
    args = parser.parse_args()

    #
    # Extract all declarations
    #
    all_ref_strs = ["attr", "const", "struct", "macro", "apifn"]
    for ref_str in all_ref_strs:
        if args.verbose is True:
            print "-"*50
            print "Extracting Standard: \""+ref_str+"\""
            print "-"*50

        # subsection.A is Appendix A: Python Bindings
        p = subprocess.Popen("grep \"newlabel{"+ref_str+"\" pmix-standard.aux | grep -v subsection.A",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
        p.wait()
        if p.returncode != 0:
            print("Error: Failed to extract declared \""+ref_str+"\". grep error code "+str(p.returncode)+")");
            sys.exit(2)

        for line in p.stdout:
            line = line.rstrip()
            m = re.match(r"\s*\\newlabel{"+ re.escape(ref_str) + r":(\w+)", line)
            if m is None:
                print("Error: Failed to extract an \""+ref_str+"\" on the following line")
                print(" line: "+line)
                sys.exit(1)


            # Count will return to 0 when verified
            value = m.group(1)
            #print("Found \""+ref_str+"\" : "+value+" on line " + line)
            std_all_refs[value] = -1
            if ref_str == "attr":
                if value in std_attributes:
                    std_attributes[value] = std_attributes[value] + 1
                else:
                    std_attributes[value] = 1
            elif ref_str == "const":
                if value in std_consts:
                    std_consts[value] = std_consts[value] + 1
                else:
                    std_consts[value] = 1
            elif ref_str == "struct":
                if value in std_structs:
                    std_structs[value] = std_structs[value] + 1
                else:
                    std_structs[value] = 1
            elif ref_str == "macro":
                if value in std_macros:
                    std_macros[value] = std_macros[value] + 1
                else:
                    std_macros[value] = 1
            elif ref_str == "apifn":
                if value in std_apis:
                    std_apis[value] = std_apis[value] + 1
                else:
                    std_apis[value] = 1
            else:
                print("Error: Failed to classify the attribute: "+value)
                sys.exit(1)

    return_count = 0
    for val in std_attributes:
        if std_attributes[val] > 1:
            print("Error: " + val + " declared " + str(std_attributes[val]) + " times")
            return_count += 1
    for val in std_consts:
        if std_consts[val] > 1:
            print("Error: " + val + " declared " + str(std_consts[val]) + " times")
            return_count += 1
    for val in std_structs:
        if std_structs[val] > 1:
            print("Error: " + val + " declared " + str(std_structs[val]) + " times")
            return_count += 1
    for val in std_macros:
        if std_macros[val] > 1:
            print("Error: " + val + " declared " + str(std_macros[val]) + " times")
            return_count += 1
    for val in std_apis:
        if std_apis[val] > 1:
            print("Error: " + val + " declared " + str(std_apis[val]) + " times")
            return_count += 1

    print("-"*50)
    if return_count > 0:
        print("Found %d number of multiple declares" % (return_count))
    else:
        print("Success. No multiple declares detected!")
    sys.exit(return_count)
