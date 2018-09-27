# root-get

- ROOT's package manager prototype

root-get is the project centric package manager for ROOT. The application provides simplified build and install process for ROOT packages and modules, along with functionality to plug external packages  and modules.

## Getting started

## Manifest file
The installation procedure in root-get has manifest files at its base. Manifest file is structured as yml file and provides the necessary attributes regarding an entity. (hereafter entity refers to package or module)
Package manifest contains the package attributes along with specifications regarding its modules. 
Module manifest contains attributes for a specific module.
The necessary attributes in any manifest file are :
- name (module/package)
- packageurl (In case of downloading the entity and using it)
- path (The absolute path for the entity if present in system)
- deps (Dependencies for the entity)
- publicheaders (Headers for the entity)
- sources 
- targets 

## Environment variables
Setting environment variables before using root-get is important to allow root-get to search for various required files from the system.
Important environment variables :
- ROOTSOURCES : The rootbase source files directory. Useful in build and install of root packages and modules.

- ROOT_PKG_PATH : The directory path where user can get the installed package/module.

- ROOTSYS : The rootbase build files directory.

- ROOT_MODULES : The directory with all the module manifest (.yml) files.

- ROOT_PKG_CACHE : The directory where entity source code, manifest and compiled sources are stored to avoid recompilation. 

Currently the installation procedure makes use of [rootbase](https://github.com/root-project/root) source files for root packages and modules.
- rootbase package install procedure

The routine uses package specific manifest file and installs each module from the manifest.
- rootbase module install procedure

The routine requires the module specific manifest file and proceeds with it.

root-get extensively makes use of cache to avoid re-building of entities. The already built packages are stored in cache directory.

## External entity handling routine

- External entity - Entity outside rootbase scope.

The entity can be present in user system or may not be present on the system. For external entity also, root-get requires manifest file.
The routine checks for entity presence in user system otherwise uses downloader routine to download the entity repository from GitHub(currently supported) and returns the path for the new downloaded directory. The further process takes the similar path as per internal entity routine.

User can provide own manifest file with all neccessary attributes present in it to plug an external entity. To create your own manifest file please follow the instructions below

- Creating module manifest file :
```
module:
  name: 'modulename'
  packageurl: 'link/to/github/repository'
  tag: 0.0.0 
  path: 'path/to/module/in/system'
  publicheaders: 'if present'
  sources: 'if present'
  targets: 'modulename'
  deps: 'dependencies'
```

- Example module.yml :
```
module: 
  name: root-get-Hello
  packageurl: "https://github.com/kiryteo/root-get-Hello"
  tag: 0.0.0
  path: /home/username/root-get-Hello
  publicheaders: 
  sources: no_sources
  targets: root-get-Hello
  deps: 
``` 

- Creating package manifest file :
```
package:
  name: 
  tag: 'version value'
  targets:
    target:
    name: 'package_name'
  products:
    package:
      name: 
  module1:
    name: 'modulename'
    packageurl: 'link/to/github/repository'
    tag: 0.0.0 
    path: 'path/to/module/in/system'
    publicheaders: 'if present'
    sources: 'if present'
    targets: 'modulename'
    deps: 'dependencies'
  module2:
    .
    .
  module:
```

- Example package_name.yml :
```
package: 
 name: "IO"
 tag: 0.0.0
 targets:
  target:
   name: "IO"
 products:
  package:
   name: IO
 module: 
  name: "RCastor"
  packageurl: "https://github.com/root-project/io/castor"
  tag: 0.0.0
  path: /home/ashwin/root/io/castor
  publicheaders: 
  sources: no_sources
  targets: 
  deps: Net;Core;RIO
 module: 
  name: "DCache"
  packageurl: "https://github.com/root-project/io/dcache"
  tag: 0.0.0
  path: /home/ashwin/root/io/dcache
  publicheaders: 
  sources: no_sources
  targets: 
  deps: Net;Core;RIO 
```

## Prerequisites

python3

matplotlib [installation](https://matplotlib.org/users/installing.html)

networkx [installation](https://networkx.github.io/documentation/stable/install.html)

pyyaml (install with - sudo apt-get install python-yaml)

cmake (Version 3.8 & above)


## Initial setup
Fork and Clone the repository (preferably in '/home/username' directory)
```
$ git clone https://github.com/oshadura/root-get
```
Create a directory where you would like to install new packages using root-get
(inside '/home/username' directory or any other path)
```
$ mkdir installdir
```
Set environment variables and get inside the root-get directory
```
$ export ROOTSOURCES="/path/to/root/source/directory"
$ export ROOT_PKG_PATH="/path/where/to/install/new/packages"
(/home/username/installdir if you have followed above method)
$ export ROOTSYS="/path/to/rootbuild/directory"
$ export ROOTSYS="/path/to/module/manifest/files"
$ cd root-get
```

## Installing

To install a new module with root-get (any of the following):
```
python ./bin/root_get.py -mi 'modulename'

python ./bin/root_get.py --module-install 'modulename' 
```

e.g. Installing XMLIO with root-get :
```
python ./bin/root_get.py -mi XMLIO

python ./bin/root_get.py --module-install XMLIO
```

To install a new package with root-get (any of the following):
```
python ./bin/root_get.py -pi 'package_name'

python ./bin/root_get.py --package-install 'package_name'
```

e.g. Installing IO package with root-get :
```
python ./bin/root_get.py -pi IO

python ./bin/root_get.py --package-install IO
```

## List installed packages in install directory
```
python ./bin/root_get.py -l/--list (use either)
```

## Search for a specific package in rootbase to be installed
```
python ./bin/root_get.py -s/--search (use either)
```

## Contributing

Please read [CONTRIBUTING.md]() for details on our code of conduct, and the process for submitting pull requests to us.

## License

## Acknowledgments

