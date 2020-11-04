#!/bin/bash

#
# A script to run after every 'make' of the standard to check its integrity.
#
FINAL_STATUS=0

#
# Check for "Hyper reference" warnings which indicate missing cross reference.
#
echo "====> Checking Hyper References"
grep "Hyper reference" pmix-standard.log | grep Warning
if [ $? == 0 ] ; then
    echo "====> Error check references (above)"
    FINAL_STATUS=$((FINAL_STATUS+1))
else
    echo "====> Passed"
fi

#
# Check for missing cross references
#
echo "====> Checking Cross References"
grep "Warning: Reference" pmix-standard.log | grep "undefined"
if [ $? == 0 ] ; then
    echo "====> Error check references (above)"
    FINAL_STATUS=$((FINAL_STATUS+1))
else
    echo "====> Passed"
fi

#
# Check for Acronym used but not defined
#
echo "====> Checking Acronyms"
grep "Acronym" pmix-standard.log | grep "is not defined on input"
if [ $? == 0 ] ; then
    echo "====> Error check references (above)"
    FINAL_STATUS=$((FINAL_STATUS+1))
else
    echo "====> Passed"
fi

#
# Check for multiple declarations
#
echo "====> Checking Multiple Declarations"
./bin/check-multi-declare.py 2>/dev/null 1>/dev/null
if [ $? == 0 ] ; then
    echo "====> Passed"
else
    ./bin/check-multi-declare.py
    echo "====> Error check references (above)"
    FINAL_STATUS=$((FINAL_STATUS+1))
fi

#
# Check for attribute references
#
echo "====> Checking Attributes are both declared and referenced"
./bin/check-attr-refs.py 2>/dev/null 1>/dev/null
if [ $? == 0 ] ; then
    echo "====> Passed"
else
    ./bin/check-attr-refs.py
    echo "====> Error check references (above)"
    FINAL_STATUS=$((FINAL_STATUS+1))
fi

#
# All done
#
exit $FINAL_STATUS
