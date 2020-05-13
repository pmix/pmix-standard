#!/usr/bin/env python3

import os
import re
import sys
import string
import argparse
import itertools

hspace_template = string.Template(r"\hspace*{${num_spaces}\sigspace}")
def insert_hspace(line):
    old_len = len(line)
    line = line.lstrip(' ')
    num_spaces = old_len - len(line)
    if num_spaces == 0:
        return line
    else:
        return hspace_template.substitute(num_spaces=num_spaces) + line

def parse_name(signature_lines):
    struct_re = re.compile(r"(pmix_[a-z_]+_t)")
    name_re = re.compile(r"(PMIX_[A-Z_]+|PMIx_[A-Za-z_]+\()")
    #cbfunc_re = re.compile(r"typedef void \(*(pmix_[a-z_]+)")
    typedef_re = re.compile(r"typedef.*(pmix_[a-z_]+)")

    if "typedef struct" in signature_lines[0]:
        return struct_re.search(signature_lines[-1]).group(1)
    elif "typedef" in signature_lines[0]:
        return typedef_re.search(signature_lines[0]).group(1)
    name_match = name_re.search(signature_lines[0])
    if name_match is None and len(signature_lines) > 1:
        name_match = name_re.search(signature_lines[1])
    if name_match is None:
        raise RuntimeError("Failed to find name of:\n{}".format("".join(signature_lines)))
    return name_match.group(1).rstrip("(")

def parse_and_replace(tex_file):
    version_re = re.compile(r"\\versionMarker{([0-9.]+)}")
    signature_template = string.Template(
"""\\copySignature{$name}{$version}{
$signature
}
""")

    new_lines = []
    with open(tex_file, 'r') as infile:
        file_iter = iter(infile)
        try:
            while True:
                file_iter, file_iter2 = itertools.tee(file_iter)
                other_content = itertools.takewhile(lambda x: version_re.match(x) is None, file_iter2)
                new_lines.extend(other_content)
                file_iter = itertools.dropwhile(lambda x: version_re.match(x) is None, file_iter)
                version_line = next(file_iter)
                version_match = version_re.match(version_line)
                version = version_match.group(1)
                cspecificstart = next(file_iter)
                if not cspecificstart.startswith(r"\cspecificstart"):
                    new_lines.append(version_line)
                    new_lines.append(cspecificstart)
                    continue
                codepar = next(file_iter)
                assert codepar.startswith(r"\begin{codepar}")
                signature_lines = list(itertools.takewhile(lambda x: not x.startswith(r"\end{codepar}"), file_iter))
                assert len(signature_lines) >= 1
                cspecificend = next(file_iter)
                assert cspecificend.startswith(r"\cspecificend")
                name = parse_name(signature_lines)
                signature = " \\\\\n".join([insert_hspace(line.rstrip()) for line in signature_lines])
                signature = signature.replace("#", "\#") # escape macro argument symbol in latex
                new_lines.append(signature_template.substitute(version=version, signature=signature, name=name))
        except StopIteration:
            pass
    return new_lines

def output_lines(outfile, lines):
    for line in lines:
        print(line, end="", file=outfile)

def main():
    new_lines = parse_and_replace(args.tex_file)
    if args.inplace:
        with open(args.tex_file, 'w') as outfile:
            output_lines(outfile, new_lines)
    else:
        output_lines(sys.stdout, new_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file")
    parser.add_argument("-i", "--inplace", action="store_true", help="edit files in place")
    args = parser.parse_args()

    main()
