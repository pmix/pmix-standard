# Source Code Examples

## General Rules

 * All examples should be buildable
 * All examples should contain a comment in the header with:
   - How to run the example
   - Example output from a run

## Preprocessor Syntax

The preprocessor will automatically extract code snippets from the source files.

The code snippets will be in the `sources/_autogen_` directory which is deleted and recreated on every build.
The code snippets will be named `sources/_autogen_/FILENAME_TAG` where `FILENAME` is the source file and `TAG` is the tag used inside the code snippet to identify the snippet.
Code snippets can span multiple sections which are concatinated, in order of appearance, into the output file.
Code snippets cannot span multiple files.

 * Start a snippet tagged `myexample` : `<EG BEGIN ID="myexample">`
 * End a snippet tagged `myexample` : `<EG END ID="myexample">`
 * Tags may only contain alphabetic and numberic characters and the following symbols: `.` `_`
   - Quote marks are stripped out of the string
 * Lines containing the snippet syntax as stripped out of the generated examples.

### Example

Given the following example program called `hello-alt.c`

```
#include <pmix.h>

int main(int argc, char **argv)
{
    //<EG BEGIN ID="pmix_init">
    //<EG BEGIN ID="pmix_get">
    pmix_status_t rc = PMIX_SUCCESS;
    pmix_proc_t myproc;
    //<EG END ID="pmix_init">
    pmix_value_t *val;
    uint16_t localrank;
    //<EG END ID="pmix_get">

    //<EG BEGIN ID="pmix_init">
    rc = PMIx_Init(&myproc, NULL, 0);
    if (PMIX_SUCCESS != rc) {
        return 1;
    }
    //<EG END ID="pmix_init">

    //<EG BEGIN ID="pmix_get">
    /* Get our rank local to this node */
    rc = PMIx_Get(&myproc, PMIX_LOCAL_RANK, NULL, 0, &val);
    if (PMIX_SUCCESS != rc) {
        return 2;
    }
    localrank = val->data.uint16;
    PMIX_VALUE_RELEASE(val);
    //<EG END ID="pmix_get">
    
    rc = PMIx_Finalize(NULL, 0);
    return rc;
}
```

Produces two snippet files

```
Processing File: sources/hello-alt.c
	Example: in_fname=[sources/hello-alt.c] id=["pmix_get"] -- Stored in sources/_autogen_/hello-alt.c_pmix_get
	Example: in_fname=[sources/hello-alt.c] id=["pmix_init"] -- Stored in sources/_autogen_/hello-alt.c_pmix_init
```

```
shell$ cat sources/_autogen_/hello-alt.c_pmix_init 
pmix_status_t rc = PMIX_SUCCESS;
pmix_proc_t myproc;

rc = PMIx_Init(&myproc, NULL, 0);
if (PMIX_SUCCESS != rc) {
    return 1;
}
```

```
shell$ cat sources/_autogen_/hello-alt.c_pmix_get 
pmix_status_t rc = PMIX_SUCCESS;
pmix_proc_t myproc;
pmix_value_t *val;
uint16_t localrank;

/* Get our rank local to this node */
rc = PMIx_Get(&myproc, PMIX_LOCAL_RANK, NULL, 0, &val);
if (PMIX_SUCCESS != rc) {
    return 2;
}
localrank = val->data.uint16;
PMIX_VALUE_RELEASE(val);
```

## Including Code Snippets in Latex

Import C code with and without highlighting (line numbers from generated source)
```
Example without highlighting
\pmixCodeImportC{sources/_autogen_/hello-alt.c_pmix_init}%

Example with highlighting:
\pmixCodeImportC[highlightlines={2-3,7,11-13}]{sources/_autogen_/hello-alt.c_pmix_get}%

\pmixCodeInlineC{printf("Hello World");} prints ``Hello World''.
```

Import Python code

```
The inline code \pmixCodeInlinePy{print("Hello World")} prints ``Hello World''.

\pmixCodeImportPy{sources/_autogen_/hello.py_pmix_py}%
```