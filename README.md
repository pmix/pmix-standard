[![Build Status](https://travis-ci.org/pmix/pmix-standard.svg?branch=master)](https://travis-ci.org/pmix/pmix-standard)

# PMIx Standard

This repository contains the LaTeX source for the PMIx standard document, and discussions regarding the PMIx standard.

## Contributing to the PMIx Standard

There are two main ways to contribute to the PMIx Standard: Participating in the discussion, and writing sections of the document.

### Participating in the discussion

If you have a question about the PMIx interface or want to raise a question for discussion then please file an Issue against this repository. We are using the Issues to discuss topics, and will link Pull Requests related to that topic to that Issue. This provides the community with a public, archived forum for discussion.

### Participatin in the writing

If you want to write a portion of the standard (or even fix a typo or two), then use the Pull Request mechanism to post the change for review.

If you want plan to work on a large section of the document then please coordinate with the community on the PMIx mailing list to make sure we are not duplicating efforts. When working on a large section (particularly if the changes are going to take a day or two to make) then let the community know, file a PR with your first set of changes, and mark the PR as "Work In Progress".  Once it is ready for review then remove the "Work In Progress" label, and let the community know that it's ready for discussion.

## Building the PMIx Standard document

You will need a LaTeX installation on your system.
To build simply type `make` and it will generate the standard PDF.
See documentation in header comment of `pmix-standard.tex`, and the macros provided by `pmix.sty`.
