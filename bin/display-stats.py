#!/usr/bin/env -S python3 -u

import sys
import os
import re
import argparse
import subprocess
import shutil

class Reference:
    def __init__(self, name):
        self.name = name
        self.is_dep = False
        self.is_rm = False

    def __str__(self):
        if self.is_dep:
            return self.name + " (Deprecated)"
        elif self.is_rm:
            return self.name + " (Removed)"
        else:
            return self.name

    def __cmp__(self, other):
        return (self.name < other.name)

def display_header():
    print("Valid | Deprecated | Removed | Description")
    display_footer()

def display_footer():
    print("------+------------+---------+--------------")

def display_counts(refs, desc, filename = None):
    num_total  = len(refs)
    num_dep    = sum(x.is_dep for x in refs)
    num_rm     = sum(x.is_rm for x in refs)
    num_active = num_total - num_dep - num_rm

    print("%5d | %10d | %7d | %s" % (num_active, num_dep, num_rm, desc))

    if filename is not None:
        output = filename + "-" + desc + "-Deprecated.txt";
        with open(output, "w") as f:
            for x in sorted(refs, key=lambda x: x.name):
                if x.is_dep is True:
                    f.write(x.name + "\n")
        output = filename + "-" + desc + "-Removed.txt";
        with open(output, "w") as f:
            for x in sorted(refs, key=lambda x: x.name):
                if x.is_rm is True:
                    f.write(x.name + "\n")
        output = filename + "-" + desc + ".txt";
        with open(output, "w") as f:
            for x in sorted(refs, key=lambda x: x.name):
                if x.is_dep is False and x.is_rm is False:
                    f.write(x.name + "\n")

if __name__ == "__main__":
    std_all = []
    std_attributes = []
    std_macros = []
    std_consts = []
    std_structs = []
    std_apis = []

    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard Display Interface Stats")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-d", "--debug", help="Debugging output", action="store_true")
    parser.add_argument("-f", "--filename", help="File prefix to write values")

    parser.parse_args()
    args = parser.parse_args()

    if os.path.exists("pmix-standard.aux") is False:
        print("Error: Cannot find the .aux files necessary for processing in the current directory.")
        print("       Please run this script from the base PMIx Standard build directory, and with a recent build.")
        sys.exit(1)

    #
    # Extract all declarations
    #
    all_ref_strs = ["attr", "const", "struct", "macro", "apifn"]
    for ref_str in all_ref_strs:
        if args.verbose is True:
            print("-"*50)
            print("Extracting Standard: \""+ref_str+"\"")
            print("-"*50)

        # subsection.A is Appendix A: Python Bindings
        p = subprocess.Popen("grep \"newlabel{"+ref_str+"\" pmix-standard.aux | grep -v \"subsection.A\"",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
        sout = p.communicate()[0].decode("utf-8").splitlines()
        if p.returncode != 0:
            print("Error: Failed to extract declared \""+ref_str+"\". grep error code "+str(p.returncode)+")");
            sys.exit(2)

        for line in sout:
            line = line.rstrip()
            m = re.match(r"\s*\\newlabel{"+ re.escape(ref_str) + r":(\w+)", line)
            if m is None:
                print("Error: Failed to extract an \""+ref_str+"\" on the following line")
                print(" line: "+line)
                sys.exit(1)

            ref = Reference(m.group(1))
            ref.is_dep = re.search(r"Deprecated", line) is not None
            ref.is_rm  = re.search(r"Removed", line) is not None
            std_all.append(ref)

            if args.debug is True:
                print("DEBUG: Classify: %s" % ref)

            if ref_str == "attr":
                std_attributes.append(ref)
            elif ref_str == "const":
                std_consts.append(ref)
            elif ref_str == "struct":
                std_structs.append(ref)
            elif ref_str == "macro":
                std_macros.append(ref)
            elif ref_str == "apifn":
                std_apis.append(ref)
            else:
                print("Error: Failed to classify: %s" % ref)
                sys.exit(1)
        p.wait()

    #
    # Display summary
    #
    display_header()
    display_counts(std_apis, "APIs", args.filename)
    display_counts(std_attributes, "Attributes", args.filename)
    display_counts(std_consts, "Constants", args.filename)
    display_counts(std_macros, "Macros", args.filename)
    display_counts(std_structs, "Structs", args.filename)
    display_footer()
    display_counts(std_all, "Totals")

    sys.exit(0)
