#!/bin/bash -xe

if [ ! -f "pmix-standard.tex" ] ; then
    echo "Error: Must be in the top pmix-standard directory"
    exit 1
fi

docker pull jjhursey/pmix-standard

docker run --rm \
       --user $(id -u):$(id -g) \
       -v $PWD:/home/pmixer/doc \
       jjhursey/pmix-standard \
       ./bin/build-std.sh /home/pmixer/doc inplace
