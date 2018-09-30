# Running an Angular application from Python and Flask
This is an example how to setup and run an Angular application from Python and Flask.

'Python and Flask serving Angular'
Copyright (C) 2018 Marc Bertens-Nguyen <m.bertens@pe2mbs.nl>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

This project was based on many internet sources. Many thanks to all those authors that 
showed how to solve part of the problem.

# Structure
```
<project-root-folder>
+- dist
+- e2e
+- python
   +- angular
      __init__.py
      loader.py
   +- api
      __init__.py
      contacts.py
      pager.py
   config.py
   server.py
   server.json
+- src
   (the angular source tree)
(the angular project files)      
```
      
# Versions
## Angular
The Angular version that was used with this project is:
``` 
Angular CLI: 6.2.3
Node: 8.11.4
OS: linux x64
Angular: 6.1.8
... common, compiler, compiler-cli, core, forms, http
... language-service, platform-browser, platform-browser-dynamic
... router

Package                           Version
-----------------------------------------------------------
@angular-devkit/architect         0.8.3
@angular-devkit/build-angular     0.8.3
@angular-devkit/build-optimizer   0.8.3
@angular-devkit/build-webpack     0.8.3
@angular-devkit/core              0.8.3
@angular-devkit/schematics        0.8.3
@angular/animations               6.1.9
@angular/cdk                      6.4.7
@angular/cli                      6.2.3
@angular/material                 6.4.7
@ngtools/webpack                  6.2.3
@schematics/angular               0.8.3
@schematics/update                0.8.3
rxjs                              6.2.2
typescript                        2.9.2
webpack                           4.20.1
``` 

## Python
``` 
Python 3.5.2
``` 
## Flask
``` 
Flask                         0.10.1                
Flask-Bcrypt                  0.7.1                 
Flask-Builder                 0.9                   
Flask-Classy                  0.6.10                
Flask-Cors                    3.0.6                 
Flask-Mail                    0.9.1                 
Flask-Migrate                 1.8.0                 
Flask-Script                  2.0.5                 
Flask-SQLAlchemy              2.1            
```   
  
# Starting the web service 
## Development modes
```bash 
# ./server.py --configuration dev
```
Or
```bash 
# ./server.py
```

## Test modes
```bash 
# ./server.py --configuration test
```

## Production modes
```bash 
# ./server.py --configuration production
```
  
## Startup options
    -c / --configuration  Is the configuration name, when omitted 'dev' is assumed.
    -v / --verbose        Gives some more output on what is being done.          

Note that the configuration name must be known to Angular in the angular CLI config file.
```json   
   "projects": {
     "<app-name>": {
       "targets": {
         "configurations": {
           "production": {
              "fileReplacements": [
                {
                  "replace": "src/environments/environment.ts",
                  "with": "src/environments/environment.prod.ts"
                }
              ],
              "optimization": true,
              "outputHashing": "all",
              "sourceMap": false,
              "extractCss": true,
              "namedChunks": false,
              "aot": true,
              "extractLicenses": true,
              "vendorChunk": false,
              "buildOptimizer": true
           },
           "test": {
              "fileReplacements": [
                {
                  "replace": "src/environments/environment.ts",
                  "with": "src/environments/environment.test.ts"
                }
              ],
              "optimization": true,
              "outputHashing": "all",
              "sourceMap": false,
              "extractCss": true,
              "namedChunks": false,
              "aot": true,
              "extractLicenses": true,
              "vendorChunk": false,
              "buildOptimizer": true
           }
         }
       }
     }
   }
```   
The example above results in three configurations: 'production', 'test', 'dev' 
  
# server.json configuration
The followinf is an axample configuration. 

```json
{
  "production":
  {
    "host": "0.0.0.0",
    "port": 6443,
    "extra_files": [],
    "debug": false,
    "ssl": {
      "certificate": "./cert/dev.angular.crt",
      "keyfile": "./cert/dev.angular.key"
    }
  },
  "test":
  {
    "host": "0.0.0.0",
    "port": 6443,
    "extra_files": [],
    "debug": false,
    "ssl": {
      "certificate": "./cert/dev.angular.crt",
      "keyfile": "./cert/dev.angular.key"
    }
  },
  "dev":
  {
    "host": "127.0.0.1",
    "port": 6080,
    "extra_files": [
      ".ts",
      ".css",
      ".scss",
      ".html"
    ],
    "debug": true
  }
} 
```  
## host
This is the host name or IP address where the server will listen on.
 
## port
This is the host port number where the server will listen on.

## debug
Set the mode to debug or not.

## extra_files
This is optional, when in debug mode an array of file extensions may be provided on which 
 the server shall reload when changes to those files are made.   

## ssl
This is optional, this SSL/TLS configuration and has two keys

### certificate
This is the SSL/TLS certificate file for the server

### keyfile  
This is the SSL/TLS key file for the server

## project_dir
This is optional, when the server.py is not in a subfolder of the angular project 
 this must be provided.

## angular_path
This is optional, this normally derives from the project_dir. When the Angular source folder 
is not 'dist' then this must be used.     

## source_path
This is optional, this normally derives from the project_dir. When the Angular source folder 
is not 'src' then this must be used.  

# Angular project
The Angular project contains a a simple contact's page to demonstrate the pagination component. It can be used for both remote and local data.
