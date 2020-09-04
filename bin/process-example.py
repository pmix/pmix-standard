#!/usr/bin/python -u

#
# Recognized tags
#   <EG BEGIN ID="string">  : Start a block
#   <EG END ID="string">    : End a block
# Rules:
#   - The tag strings, regardless of ID, are removed from the final output
#   - If multiple blocks with the same ID exist then they are concatinated together
#   - ID can contain alphabetic and numberic characters and the following symbols: . _
#     - Quote marks are stripped out
#
import sys
import os
import re
import argparse
import subprocess
import shutil

EG_BEGIN_STR="EG BEGIN ID="
EG_END_STR="EG END ID="
EG_ID_PATTERN="[A-Za-z0-9_\.\"]"


class Example:
    """An example from the source code"""
    eid = None
    active = False
    filename = None
    code_block = ""

    def __init__(self):
        self.eid = ""
        self.active = False
        self.filename = None
        self.code_block = ""

    def __str__(self):
        return "in_fname=[%s] id=[%s]" % (self.filename, self.eid)

    def get_out_fname(self):
        f_id = self.eid.replace('"', '')
        return os.path.basename(self.filename) + "_" + f_id

    def append_line(self, line):
        self.code_block = self.code_block + line
        if line.endswith("\n") is False:
            self.code_block = self.code_block + "\n"

    def get_code_block(self):
        final_block = ""
        min_lead_spaces = 10000
        lines = 0
        total_lines = 0
        skip_last_lines = 0

        # First pass to find min spacing
        for line in self.code_block.splitlines(True):
            if re.search(r"\s*"+EG_BEGIN_STR, line) is not None:
                continue
            if re.search(r"\s*"+EG_END_STR, line) is not None:
                continue
            
            total_lines = total_lines + 1
            # Skip empty lines
            if len(line) <= 1:
                skip_last_lines = skip_last_lines + 1
                continue
            else:
                skip_last_lines = 0

            m = re.match(r"^([ \t]+)", line)
            if m is not None:
                c_len = len(m.group(1))
                if c_len > 1:
                    min_lead_spaces = min(c_len, min_lead_spaces)
            else:
                # Indicates that there is a line that does not have leading spaces, but is not empty
                min_lead_spaces = 0

        # Next pass to build the string
        lines = 0
        for line in self.code_block.splitlines(True):
            if re.search(r"\s*"+EG_BEGIN_STR, line) is not None:
                continue
            if re.search(r"\s*"+EG_END_STR, line) is not None:
                continue

            # Clear off trailing empty lines
            if total_lines - skip_last_lines == lines:
                break
            lines = lines + 1

            m = re.match(r"^([ \t]+)", line)
            if m is not None:
                line = line[min_lead_spaces:]
            final_block = final_block + line

        return final_block


def process_file(filename):
    """Process all of the key/value splitting in the file"""
    all_examples = {}
    eg_id = None
    
    with open(filename, 'r') as fd:
        for line in fd:
            line = line.rstrip()
            m = re.search(r"\s*"+EG_BEGIN_STR+"("+EG_ID_PATTERN+"*)", line)
            if m is not None:
                eg_id = m.group(1)
                # Find this object and update it
                found = False
                for example_id in all_examples:
                    if example_id == eg_id:
                        example = all_examples[example_id]
                        example.active = True
                        example.append_line(line)
                        found = True
                # Insert it if not found
                if found is False:
                    x = Example()
                    x.eid = eg_id
                    x.active = True
                    x.append_line(line)
                    x.filename = filename
                    all_examples[eg_id] = x
                continue

            m = re.search(r"\s*"+EG_END_STR+"("+EG_ID_PATTERN+"*)", line)
            if m is not None:
                eg_id = m.group(1)
                # Find this object and update it
                for example_id in all_examples:
                    if example_id == eg_id:
                        example = all_examples[example_id]
                        example.active = False
                        example.append_line("") # Add an empty line
                continue

            for example_id in all_examples:
                example = all_examples[example_id]
                if example.active is True:
                    example.append_line(line)

    return all_examples


if __name__ == "__main__":
    #
    # Command line parsing
    #
    parser = argparse.ArgumentParser(description="PMIx Standard Example Preprocessor")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("files", nargs='+', help="List of files to process")
    parser.parse_args()
    args = parser.parse_args()

    #
    # Create a temporary directory to store the snippets
    #
    gen_dir = "sources/_autogen_"
    if os.access(gen_dir, os.W_OK) is False:
        os.makedirs(gen_dir)

    #
    # Iterate through all examples and split out the snippets
    #
    for f in args.files:
        if os.path.exists(f) is False:
            print("ERROR: File does not exist: %s" % (f))
            sys.exit(1)

        print("Processing File: %s" % (f))
        example_blocks = process_file(f)
        for k, example in example_blocks.items():
            out_fname = gen_dir + "/" + example.get_out_fname()
            print("\tExample: %s -- Stored in %s" % (example, out_fname))
            if args.verbose:
                print("CODE BLOCK")
                print("-" * 50)
                print(example.get_code_block()),
                print("-" * 50)
            with open(out_fname, 'w') as fd:
                fd.write("%s" % (example.get_code_block()))

    sys.exit(0)
