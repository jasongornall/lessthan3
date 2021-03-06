**v0.6.5** (2014-03-21)

 - replace all substitutions, not just the first

**v0.6.4** (2014-03-21)

 - force utf8 for reading CSON files to fix arrays going into firebase

**v0.6.3** (2014-03-20)

 - change .page to .object to reinforce pages are just special objects

**v0.6.2** (2014-03-18)

 - make v2 sites the default commands and move v1 to v1:
 - use node instead of coffee for binaries to remove global coffee dependency

**v0.6.1** (2014-03-17)

 - fix site create when product has no collections
 - use config.core instead of config.type for compiling rules

**v0.6.0** (2014-03-16)

 - change domains.domain to domain.url
 - take advantage of new pre-processing with asset-wrap
 - better .exports shortcutting for new 2.0 site layouts
 - use pre-processing to add in extends for new coffee files
 - move old coffee-script replacements to new post-processing function
 - only init header js to {} if not explicitly settings data (config/schema)
 - imports.styl must be first as @import need to start the css file
 - concat variables.styl to the beginning of all other styl files
 - remove header initialization for libraries
 - add v2:add:page and v2:add:object for new sites
 - single file reload for more efficient reloading during development

**v0.5.17** (2014-03-10)

 - add v2:create for new site creation
 - modify getPackageConfig to look up any package config

**v0.5.16** (2014-03-10)

 - add code substitutions for Collection and Object

**v0.5.15** (2014-03-06)

 - use chokidar 0.7.1 due to windows bug in 0.8.0

**v0.5.14** (2014-03-06)

 - adding some debug info to fix a windows problem

**v0.5.13** (2014-03-06)

 - log error differently for local file watching

**v0.5.12** (2014-03-01)

 - better error message when unavailable to parse CSON

**v0.5.11** (2014-03-01)

 - only read cson files for schema - watch out for swap files

**v0.5.10** (2014-03-01)

 - bug in last deploy

**v0.5.9** (2014-03-01)

 - always set latest schema when loading main.js

**v0.5.8** (2014-02-24)

 - supply more information about the modified file for hot code pushes

**v0.5.7** (2014-02-24)

 - simpler css asset sorting

**v0.5.6** (2014-02-24)

 - import entire style directory for style.css
 - fix .css package dependencies

**v0.5.5** (2014-02-23)

 - separate config and schema for packages

**v0.5.4** (2014-02-23)

 - change load order for main.js compilation

**v0.5.3** (2014-02-23)

 - change View to Presenter

**v0.5.2** (2014-02-23)

 - ignore api.coffee for main.js compilation

**v0.5.1** (2014-02-23)

 - adding some backwards compatibility

**v0.5.0-beta** (2014-02-12)

 - read in individual schema files
 - make all fs calls async for better performance and error handling

**v0.4.2** (2014-02-07)

 - replace express bodyParser per expressjs 3.x request

**v0.4.1** (2014-02-04)

 - css or javascript compile errors are now 400 instead of 500 errors

**v0.4.0** (2014-02-03)

 - update dependencies

**v0.3.5** (2014-02-02)

 - bump asset-wrap version to 0.5.x

**v0.3.4** (2014-02-01)

 - do not cache api.coffee files on dev servers

**v0.3.3** (2014-01-20)

 - add initial lpm commands

**v0.3.2** (2014-01-12)

 - add --dev option to open to force local dev load

**v0.3.1** (2014-01-10)

 - fix error in usage dialog
 - disallow creating workspaces within other workspaces

**v0.3.0** (2014-01-08)

 - add admin to site
 - add app to site
 - add page to site app
 - create a new site
 - initialize a new workspace
 - new login workflow
 - daemonize dev server

**v0.2.10** (2013-12-17)

 - add maxAge header for /public files

**v0.2.9** (2013-12-02)

 - fix path.join error for node 0.10.x
 - lowercase import for cson
 - exit process after lt3 init
 - add basic create:entity support

**v0.2.8** (2013-11-04)

 - typo in last update

**v0.2.7** (2013-11-04)

 - add req.body shortcut

**v0.2.6** (2013-11-01)

 - watch out for custom main.js in config

**v0.2.5** (2013-11-01)

 - dont add connect path on prod
 - add version command to binaries
 - make paths Windows safe
 - remove package.cson and package.coffee support

**v0.2.4** (2013-10-13)

 - report error information in the console
 - fix non-package files in pkg (ex: .DS_STORE)

**v0.2.3** (2013-10-07)

 - add starting dev server to CLI

**v0.2.2** (2013-10-07)

 - fix path to binary in package.json

**v0.2.1** (2013-10-07)

 - begin work on CLI

**v0.2.0** (2013-10-04)

 - bump asset-wrap to 0.4.x

**v0.1.16** (2013-10-04)

 - use $ for prefix on stylus variables

**v0.1.15** (2013-10-01)

 - bump firebase version to 0.6.x

**v0.1.14** (2013-08-26)

 - fix api method routing

**v0.1.13** (2013-08-26)

 - allow string parameter to cache (assumes string is age)

**v0.1.12** (2013-08-24)

 - bug fixes

**v0.1.11** (2013-08-24)

 - allow package api calls to be GET or POST

**v0.1.10** (2013-08-06)

 - update asset-wrap

**v0.1.9** (2013-08-03)

  - return available local packages when connecting

**v0.1.8** (2013-08-03)

 - watch out for errors in bad packages
 - change /local-dev/setToken to /connect

**v0.1.7** (2013-07-30)

 - rename package to config. leaving package for backwards compatibility

**v0.1.6** (2013-07-30)

 - move read_package higher up to fix watcher

**v0.1.5** (2013-07-29)

 - prefer config.cson to package.cson
 - add some example packages

**v0.1.4** (2013-07-29)

 - add @query to context of api calls

**v0.1.3** (2013-07-29)

 - do not crash if a package can not be found
 - lowercase on comments

**v0.1.2**

 - Start CHANGELOG.md
