/*
 * Copyright (c) 2004-2010 The Trustees of Indiana University and Indiana
 *                         University Research and Technology
 *                         Corporation.  All rights reserved.
 * Copyright (c) 2004-2011 The University of Tennessee and The University
 *                         of Tennessee Research Foundation.  All rights
 *                         reserved.
 * Copyright (c) 2004-2005 High Performance Computing Center Stuttgart,
 *                         University of Stuttgart.  All rights reserved.
 * Copyright (c) 2004-2005 The Regents of the University of California.
 *                         All rights reserved.
 * Copyright (c) 2006-2013 Los Alamos National Security, LLC.
 *                         All rights reserved.
 * Copyright (c) 2009-2012 Cisco Systems, Inc.  All rights reserved.
 * Copyright (c) 2011      Oak Ridge National Labs.  All rights reserved.
 * Copyright (c) 2013-2018 Intel, Inc. All rights reserved.
 * Copyright (c) 2015      Mellanox Technologies, Inc.  All rights reserved.
 * Copyright (c) 2020      IBM Corporation.  All rights reserved.
 * $COPYRIGHT$
 *
 * Additional copyrights may follow
 *
 * $HEADER$
 *
 */

#define _GNU_SOURCE
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
#include <ctype.h>

#include <pmix.h>

int main(int argc, char **argv)
{
    pid_t pid;
    char hostname[1024];
    pmix_status_t rc = PMIX_SUCCESS;
    pmix_proc_t myproc;
    pmix_value_t *val;
    uint16_t localrank;

    pid = getpid();
    gethostname(hostname, 1024);

    /* Initialize PMIx - client role */
    rc = PMIx_Init(&myproc, NULL, 0);
    if (PMIX_SUCCESS != rc) {
        fprintf(stderr, "Client ns %s rank %d: PMIx_Init failed: %s\n",
                myproc.nspace, myproc.rank, PMIx_Error_string(rc));
        return 1;
    }

    /* Get our rank local to this node */
    rc = PMIx_Get(&myproc, PMIX_LOCAL_RANK, NULL, 0, &val);
    if (PMIX_SUCCESS != rc) {
        fprintf(stderr,
                "Client ns %s rank %d: PMIx_Get local rank failed: %s\n",
                myproc.nspace, myproc.rank, PMIx_Error_string(rc));
        goto done;
    }
    localrank = val->data.uint16;
    PMIX_VALUE_RELEASE(val);

    printf("Client ns %s rank %d pid %lu: Running on host %s localrank %d\n",
            myproc.nspace, myproc.rank, (unsigned long)pid, hostname ,
            (int)localrank);

    /* Fence to hold all processes in this namespace */
    pmix_proc_t wildproc;
    PMIX_PROC_CONSTRUCT(&wildproc);
    (void)strncpy(wildproc.nspace, myproc.nspace, PMIX_MAX_NSLEN);
    wildproc.rank = PMIX_RANK_WILDCARD;

    rc = PMIx_Fence(&wildproc, 1, NULL, 0);
    if (PMIX_SUCCESS != rc) {
        fprintf(stderr,
                "Client ns %s rank %d: PMIx_Fence failed: %s\n",
                myproc.nspace, myproc.rank, PMIx_Error_string(rc));
        goto done;
    }

  done:
    /* Finalize the PMIx library */
    printf("Client ns %s rank %d: Finalizing\n", myproc.nspace, myproc.rank);
    rc = PMIx_Finalize(NULL, 0);
    if (PMIX_SUCCESS != rc) {
        fprintf(stderr, "Client ns %s rank %d:PMIx_Finalize failed: %s\n",
                myproc.nspace, myproc.rank, PMIx_Error_string(rc));
    } else {
        printf("Client ns %s rank %d:PMIx_Finalize successfully completed\n",
               myproc.nspace, myproc.rank);
    }

    return rc;
}
