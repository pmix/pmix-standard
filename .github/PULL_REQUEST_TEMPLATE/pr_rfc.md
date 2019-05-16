---
name: Request for Comment/Change
about: Modifications and extensions to the document
title: ''
labels: ''
assignees: ''

---

## Title
> A short, descriptive title of what is being proposed.


## Link to relevant issue(s): (*required*)
> *Note:* Please do not create a pull request without creating an issue first.


## Labels
> *Note:* After applying labels remove this section from your PR.

Apply at least one of the following labels :

* [MODIFICATION] - modifies an existing PMIx definition (API, key string, etc.)
* [EXTENSION] - adds a new PMIx definition
* [BEHAVIOR] - modifies the underlying behavior of an existing PMIx function
* [ORGANIZATION] - changes the organization of the existing files, perhaps
  moving files across directories
* [CLIENT-API] - modifies/extends the client-side API
* [SERVER-API] - modifies/extends the server-side API
* [RM-INTERFACE] - modifies/extends the interface to the host resource manager

While it is permissible to combine these labels in a single RFC, best practices are to separate such operations into individual RFCs. For example, it is requested that authors separate modifications from extensions to avoid confusion. Where this is not logically possible (e.g., an extension that requires an accompanying change in the behavior of an existing PMIx function), then all applicable labels shall be provided.


## Abstract
> A brief description of the proposed change.

## Description
> A detailed description of the proposed change. The length and degree of detail should be commensurate with the magnitude of the change. This is not intended to be burdensome, nor are there any awards for verbosity - but clear communication will avoid repeated requests for alterations. The description should indicate what is being modified, both functionally and by file name.


## Prototype Implementation

> *Note:* A prototype implementation is optional when creating a PR, but required before the PR can enter the acceptance process.
> Provide a reference link to the accompanying Pull Request (PR) against an open-source PMIx implementation. If the prototype implementation has been tested against an appropriately modified resource manager and/or client program, then references to those prototypes should be provided. Logs or output from the implementation being used are encouraged (if the output is large, please use a GitHub Gist).


## Author(s)
> Provide a list of authors, including contact info. This can be in the form of email address or Github ID.


## Copyright Notice
This document is subject to all provisions relating to code contributions to the PMIx community as defined in the community's [LICENSE](https://github.com/pmix/RFCs/tree/master/LICENSE) file. Code Components extracted from this document must include the License text as described in that file.


## Acceptance Process Dates
_The PMIx Community will update this section as the PR progresses through the acceptance process._

|                  | Date | Link to discussion |
| ---------------- | ---- | ------------------ |
| **Reading**      |      |                    |
| **Acceptance**   |      |                    |

