[![Build Status](https://travis-ci.org/pmix/pmix-standard.svg?branch=master)](https://travis-ci.org/pmix/pmix-standard)

# PMIx Standard

PMIx is an application programming interface (API) standard to provide
High Performance Computing (HPC) libraries and programming models with
portable and well-defined access to commonly available
distributed computing system services.

This repository contains the LaTeX source for the PMIx standard document
and discussions regarding the PMIx standard.

## Contributing to the PMIx Standard

We welcome participation in development of the PMIx Standard. To find out
more about how to participate, visit our web site at https://pmix.org/

On the web site, you will find [background documents and
publications](https://pmix.org/publications/), and information
about [joining our mailing lists, meetings,
and working groups](https://pmix.org/contribute/).
Additionally, you will find our governance document,
[The PMIx Standard Governance Rules](https://pmix.org/wp-content/uploads/2019/08/pmix-governance.pdf), which describes
rules for participation and making changes to the PMIx Standard.
The governance document includes instructions for how to raise questions
about the standard as well as how to propose changes to the standard.

## Building the PMIx Standard

### Building with Docker

The community maintains a [Docker container image](https://github.com/jjhursey/pmix-standard-dockerfile) that can be used to build the standard using the included script. This is the same container image that is used in CI.

```
./bin/build-with-docker.sh
```

### Building on Your System

 * If you are building on Ubuntu then take a look at [this Dockerfile](https://github.com/jjhursey/pmix-standard-dockerfile/blob/master/Dockerfile)
 * If you are building on Mac OSX start with [MacTeX](https://www.tug.org/mactex/) then add the rest of the dependencies:
```
sudo pip2 install --upgrade pip setuptools
sudo pip2 install Pygments
```
