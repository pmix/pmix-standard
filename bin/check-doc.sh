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
# Check for Acronym used but not defined
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
# All done
#
exit $FINAL_STATUS
