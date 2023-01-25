#!/usr/bin/env -S python3 -u

import sys
import os
import re
import argparse
import subprocess
import shutil

def check_missing_pmix_standard(std_all_refs, openpmix_all_refs,
                                std_deprecated, std_removed,
                                openpmix_deprecated, verbose=False):
    """Check for OpenPMIx definitions missing from the PMIx Standard"""

    print("-"*50)
    print ("Checking: Defined in OpenPMIx, but not in the PMIx Standard")
    print ("-"*50)

    missing_refs = []
    for openpmix_ref in openpmix_all_refs:
        found_ref = False
        for std_ref in std_all_refs:
            if openpmix_ref == std_ref:
                found_ref = True
                break
        if found_ref is False:
            # Double check that we didn't miss it earlier when parsing OpenPMIx
            p = subprocess.Popen("grep -in \"{"+openpmix_ref+"}\" *.tex | grep -i declare",
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
            p.wait()
            if p.returncode != 0 and p.returncode != 1:
                print("Error: Failed to grep and confirm missing item \""+openpmix_ref+"\". grep error code "+str(p.returncode)+")");
                sys.exit(2)
            if p.returncode == 0:
                possible_error = False
                for line in p.stdout:
                    line = line.rstrip()
                    line = line.decode()
                    parts = line.split(":", 2)

                    # if this reference is in a comment then ignore it
                    m = re.match(r"^\s*\*", parts[2])
                    if m is not None:
                        m = re.search(r'deprecated.h', parts[0])
                        if m is not None:
                            print("Warning: Found reference in comment: " + line)
                            continue
                    # if this reference is found in deprecated, ignore it
                    m = re.search(r'deprecated.h', parts[0])
                    if m is not None:
                        print("ERROR: Suspected Missing \""+openpmix_ref+"\" but found on "+parts[0]+"("+parts[1]+"):"+parts[2])
                        possible_error = True

                if possible_error is True:
                    sys.exit(1)


            missing_refs.append(openpmix_ref)

    return missing_refs

def check_missing_openpmix(std_all_refs, openpmix_all_refs,
                           std_deprecated, std_removed,
                           openpmix_deprecated, verbose=False):
    """Check for PMIx Standard definitions missing from OpenPMIx"""

    print ("-"*50)
    print ("Checking: Defined in PMIx Standard, but not in OpenPMIx")
    print ("-"*50)

    missing_refs = []
    for std_ref in std_all_refs:
        found_ref = False
        for openpmix_ref in openpmix_all_refs:
            if openpmix_ref == std_ref:
                found_ref = True
                break
        if found_ref is False:
            # Double check that we didn't miss it earlier when parsing OpenPMIx
            p = subprocess.Popen("grep -in \""+std_ref+"[^a-zA-Z0-9_]\" check-openpmix/include/*",
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
            p.wait()
            if p.returncode != 0 and p.returncode != 1:
                print("ERROR in script: Failed to grep and confirm missing item \""+std_ref+"\". grep error code "+str(p.returncode)+")");
                sys.exit(2)
            if p.returncode == 0:
                possible_error = False
                for line in p.stdout:
                    line = line.rstrip()
                    line = line.decode()
                    parts = line.split(":", 2)

                    # if this reference is in a comment then ignore it
                    m = re.match(r"^\s*\*", parts[2])
                    if m is not None:
                        # if this is a deprecated or removed reference, don't worry about it
                        if any(std_ref in s for s in openpmix_deprecated):
                            continue
                        elif any(std_ref in s for s in std_deprecated):
                            continue
                        elif any(std_ref in s for s in std_removed):
                            continue
                        else:
                            print("Warning: Found reference in comment: " + line)
                        continue

                    # if this is a deprecated or removed reference, don't worry about it
                    if any(std_ref in s for s in openpmix_deprecated):
                        continue
                    elif any(std_ref in s for s in std_deprecated):
                        continue
                    elif any(std_ref in s for s in std_removed):
                        continue
                    else:
                        print("ERROR in script: Suspected Missing \""+std_ref+"\" but found on "+parts[0]+"("+parts[1]+"):"+parts[2])
                        possible_error = True

                if possible_error is True:
                    sys.exit(1)

            # Ok it's missing so add it to the list if it hasn't been deprecated or removed
            if any(std_ref in s for s in openpmix_deprecated):
                continue
            elif any(std_ref in s for s in std_deprecated):
                continue
            elif any(std_ref in s for s in std_removed):
                continue
            else:
                missing_refs.append(std_ref)

    return missing_refs


if __name__ == "__main__":
    std_attributes = {}
    std_macros = {}
    std_consts = {}
    std_structs = {}
    std_apis = {}
    std_envars = {}
    std_all_refs = {}
    std_deprecated = []
    std_removed = []

    openpmix_defines = {}
    openpmix_structs = {}
    openpmix_apis = {}
    openpmix_cbs = {}
    openpmix_all_refs = {}
    openpmix_deprecated = []

    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard / OpenPMIx Cross Check")
    parser.add_argument("-v", "--verbose", help="Verbose output", action="store_true")
    parser.add_argument("-b", "--branch", help="OpenPMIx branch to be checked", nargs='?', default="master")

    parser.parse_args()
    args = parser.parse_args()

    #
    # Verify that we have the necessary files in the current working directory
    # * pmix-standard.aux
    # * check-openpmix
    #
    print ("-"*50)
    print ("Checking: OpenPMIx checkout (branch: "+args.branch+")")
    print ("-"*50)
    if os.path.exists("check-openpmix") is False:
        print("Warning: Missing OpenPMIx checkout. Trying to clone now")
        cmd = "git clone --single-branch -b " + args.branch + " https://github.com/openpmix/openpmix.git check-openpmix"
        rtn = os.system(cmd)
        if rtn != 0:
            print("Error: Failed to checkout the requested branch.")
            print("       Command: " + cmd)
            sys.exit(1)
    else:
        cmd = "cd check-openpmix ; git pull ; git checkout " + args.branch
        rtn = os.system(cmd)
        if rtn != 0:
            print("Error: Failed to checkout the requested branch.")
            print("       Command: " + cmd)
            sys.exit(1)

    print("-"*50)
    print("")

    if os.path.exists("pmix-standard.aux") is False or os.path.exists("check-openpmix") is False:
        print("Error: Cannot find the .aux files or OpenPMIx checkout necessary for processing in the current directory.")
        print("       Please run this script from the base PMIx Standard build directory, and with a recent build.")
        sys.exit(1)


    # --------------------------------------------------
    # Extract the declared items from the standard
    # attributes - grep "newlabel{attr" pmix-standard.aux
    # consts     - grep "newlabel{const" pmix-standard.aux
    # structs    - grep "newlabel{struct" pmix-standard.aux
    # macros     - grep "newlabel{macro" pmix-standard.aux
    # apis       - grep "newlabel{api" pmix-standard.aux
    # envars     - grep "newlabel{envar" pmix-standard.aux
    # --------------------------------------------------
    all_ref_strs = ["attr", "const", "struct", "macro", "apifn", "envar"]
    for ref_str in all_ref_strs:
        if args.verbose is True:
            print ("-"*50)
            print ("Extracting Standard: \""+ref_str+"\"")
            print ("-"*50)

        # subsection.A is Appendix A: Python Bindings
        p = subprocess.Popen("grep \"newlabel{"+ref_str+"\" pmix-standard.aux | grep -v subsection.A",
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, close_fds=True)
        p.wait()
        if p.returncode != 0:
            print("Error: Failed to extract declared \""+ref_str+"\". grep error code "+str(p.returncode)+")");
            sys.exit(2)

        for line in p.stdout:
            line = line.rstrip()
            line = line.decode()
            m = re.match(r"\s*\\newlabel{"+ re.escape(ref_str) + r":(\w+)", line)
            if m is None:
                print("Error: Failed to extract an \""+ref_str+"\" on the following line")
                print(" line: "+line)
                sys.exit(1)

            # Count will return to 0 when verified
            std_all_refs[m.group(1)] = -1
            if "Deprecated" in line:
                std_deprecated.append(m.group(1))
            elif re.search('removed', line, re.IGNORECASE):
                std_removed.append(m.group(1))
            elif ref_str == "attr":
                std_attributes[m.group(1)] = -1
            elif ref_str == "const":
                std_consts[m.group(1)] = -1
            elif ref_str == "struct":
                std_structs[m.group(1)] = -1
            elif ref_str == "macro":
                std_macros[m.group(1)] = -1
            elif ref_str == "apifn":
                std_apis[m.group(1)] = -1
            elif ref_str == "envar":
                std_envars[m.group(1)] = -1
            else:
                print("Error: Failed to classify the attribute: "+m.group(1))
                sys.exit(1)

    if args.verbose is True and 0 == 1:
        print ("-"*50)
        for val in std_attributes:
            print("Std Attribute: " + val)
        print ("-"*50)
        for val in std_consts:
            print("Std Const    : " + val)
        print ("-"*50)
        for val in std_structs:
            print("Std Struct   : " + val)
        print ("-"*50)
        for val in std_macros:
            print("Std Macro    : " + val)
        print ("-"*50)
        for val in std_apis:
            print("Std API      : " + val)
        print ("-"*50)
        for val in std_deprecated:
            print("Std Deprecated      : " + val)
        print ("-"*50)
        for val in std_removed:
            print("Std Removed      : " + val)
        print ("-"*50)
        for val in std_envars:
            print("Std Envar    : " + val)
        print ("-"*50)

    print("Number of Standard attributes  : " + str(len(std_attributes)))
    print("Number of Standard consts      : " + str(len(std_consts)))
    print("Number of Standard structs     : " + str(len(std_structs)))
    print("Number of Standard macros      : " + str(len(std_macros)))
    print("Number of Standard apis        : " + str(len(std_apis)))
    print("Number of Standard envars      : " + str(len(std_envars)))
    print("Total Number of Standard items : " + str(len(std_all_refs)))
    print("Number of Deprecated items     : " + str(len(std_deprecated)))
    print("Number of Removed items        : " + str(len(std_removed)))
    print("")


    # --------------------------------------------------
    # Extract the declared items from OpenPMIx
    # --------------------------------------------------
    openpmix_files = []
    for fname in os.listdir("check-openpmix/include"):
        m = re.search(r'.h', fname)
        if m is not None:
            m = re.search(r'pmi[2]?.h', fname) # Exclude pmi.h and pmi2.h
            if m is None:
                openpmix_files.append(fname)

    for openpmix_file in openpmix_files:
        openpmix_file = "check-openpmix/include/" + openpmix_file
        if args.verbose is True:
            print ("-"*50)
            print ("Extracting OpenPMIx Definitions from: " + openpmix_file)
            print ("-"*50)

        if "deprecated.h" in openpmix_file:
            parse_deprecated = True
        else:
            parse_deprecated = False
        parse_active = False
        parse_enum = False
        parse_struct = False
        defs_found = 0
        with open(openpmix_file) as fp:
            for line in fp:
                line = line.rstrip()

                m = re.match(r'extern "C"', line);
                if m is None and parse_active is False:
                    continue
                else:
                    parse_active = True

                # typedef enum {
                m = re.match(r'\s*typedef\s+enum\s*', line);
                if m is not None:
                    parse_enum = True
                    continue
                if parse_enum is True:
                    m = re.match(r'\s*}\s*(pmi\w*)', line)
                    if m is not None:
                        if parse_deprecated:
                            openpmix_deprecated.append(m.group(1))
                        else:
                            openpmix_structs[m.group(1)] = -1
                            openpmix_all_refs[m.group(1)] = -1
                            defs_found = defs_found + 1
                        parse_enum = False
                        continue
                    m = re.match(r'\s+(\w+)', line)
                    if m is not None:
                        #print("Define Enum: "+m.group(1))
                        if parse_deprecated:
                            openpmix_deprecated.append(m.group(1))
                        else:
                            openpmix_defines[m.group(1)] = -1
                            openpmix_all_refs[m.group(1)] = -1
                            defs_found = defs_found + 1
                        continue

                # typedef struct pmix_data_buffer {
                m = re.match(r'\s*typedef\s+struct\s*\w+\s+{', line);
                if m is not None:
                    parse_struct = True
                    continue
                else:
                    m = re.match(r'\s*typedef\s+struct\s*{', line);
                    if m is not None:
                        parse_struct = True
                        continue
                if parse_struct is True:
                    m = re.match(r'\s*}\s*(pmi\w+)', line)
                    if m is not None:
                        #print("Define Struct: "+m.group(1))
                        if parse_deprecated:
                            openpmix_deprecated.append(m.group(1))
                        else:
                            openpmix_structs[m.group(1)] = -1
                            openpmix_all_refs[m.group(1)] = -1
                            defs_found = defs_found + 1
                        parse_struct = False
                        continue
                    else:
                        continue

                # typedef uint8_t pmix_data_range_t;
                m = re.match(r'\s*typedef\s*\w*\s*(pmi\w*)[;|\[]', line);
                if m is not None:
                    #print("Define Struct1: "+m.group(1))
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_structs[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        defs_found = defs_found + 1
                    continue

                # #define PMIX_EVENT_BASE                     "pmix.evbase"
                m = re.match(r'#define\s+(\w+)\(', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_defines[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("Define FN: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # #define PMIx_Heartbeat()
                m = re.match(r'#define\s+(\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_defines[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("Define: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT const char* PMIx_Error_string
                m = re.match(r'PMIX_EXPORT\s+\w+\s+\w+\*\s+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("API1: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT <type>* PMI<function>
                m = re.match(r'PMIX_EXPORT\s+\w+\*\s+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("API3: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT <type>** PMI<function>
                m = re.match(r'PMIX_EXPORT\s+\w+\*+\*+\s+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        print("API4: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT <type> *PMI<function>
                m = re.match(r'PMIX_EXPORT\s+\w+\s+\*+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("API3: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT <type> **PMI<function>
                m = re.match(r'PMIX_EXPORT\s+\w+\s+\*+\*+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        print("API4: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # PMIX_EXPORT pmix_status_t PMIx_Init(
                m = re.match(r'PMIX_EXPORT\s+\w+\s+(PMI\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_apis[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("API2: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

                # typedef void (*pmix_iof_cbfunc_t)(
                m = re.match(r'\s*typedef\s+\w+\s+\(\*(\w+)', line);
                if m is not None:
                    if parse_deprecated:
                        openpmix_deprecated.append(m.group(1))
                    else:
                        openpmix_cbs[m.group(1)] = -1
                        openpmix_all_refs[m.group(1)] = -1
                        #print("CB: "+m.group(1))
                        defs_found = defs_found + 1
                    continue

        if args.verbose is True:
            print("Found "+str(defs_found)+" items in file "+openpmix_file)

    print("Number of OpenPMIx defines     : " + str(len(openpmix_defines)))
    print("Number of OpenPMIx structs     : " + str(len(openpmix_structs)))
    print("Number of OpenPMIx APIs        : " + str(len(openpmix_apis)))
    print("Number of OpenPMIx callbacks   : " + str(len(openpmix_cbs)))
    print("Total Number of OpenPMIx items : " + str(len(openpmix_all_refs)))
    print("Number of Deprecated items     : " + str(len(openpmix_deprecated)))
    print("")

    # --------------------------------------------------
    # Check to make sure that all of the items defined in OpenPMIx are in the PMIx Standard
    # - except for those explicitly excluded
    # --------------------------------------------------
    total_missing_refs = 0

    missing_refs = check_missing_pmix_standard(std_all_refs, openpmix_all_refs,
                                               std_deprecated, std_removed,
                                               openpmix_deprecated, args.verbose)
    total_missing_refs = total_missing_refs + len(missing_refs)
    if len(missing_refs) > 0:
        print ("-"*50)
        print("Found "+str(len(missing_refs))+" references defined in OpenPMIx, but not in the PMIx Standard")
        for ref in sorted(missing_refs):
            print("PMIx Standard Missing: "+ref)
        print("")


    # --------------------------------------------------
    # Check to make sure that all of the items defined in the PMIx Standard are in OpenPMIx
    # --------------------------------------------------
    missing_refs = check_missing_openpmix(std_all_refs, openpmix_all_refs,
                                          std_deprecated, std_removed,
                                          openpmix_deprecated, args.verbose)
    total_missing_refs = total_missing_refs + len(missing_refs)
    if len(missing_refs) > 0:
        print ("-"*50)
        print("Found "+str(len(missing_refs))+" references defined in PMIx Standard, but not in OpenPMIx")
        for ref in sorted(missing_refs):
            print("OpenPMIx Missing: "+ref)
        print("")


    # Return the total number of missing references
    sys.exit(total_missing_refs)

