# Structure

These are the top-level folder in the 101worker repository.

## modules

Modules that can be executed as part of a 101worker cycle. One level of folders and one module per folder. Don't go nesting them.

See also the [section about Module Contracts](#Module Contracts).

## libraries

Internal-use libraries. This folder will be added to the `$PYTHONPATH`, so you can just `import` them in modules written in Python. The same could be done for other languages, but right now we ain't needing it.

## configs

Contains configuration files for different 101worker cycle. The `production.json` is what's used normally.

The [test folder](configs/test) contains test configurations for [101test](https://github.com/101companies/101test).

The [env folder](configs/env) contains environment variable definitions. Those have their own [README](configs/env/README.md).

## schemas

JSON schema central.

## services

Web services relating to 101worker.

## attic

Stuff that nobody needs anymore, but you don't quite want to throw it away.

Somebody should probably clear out the attic sometime, since Git has a history of all files anyway. Unless Martin breaks it again, that is.


# Module Contracts

Modules go into the [modules folder](modules). A module consists of the following (optional things are marked as such, everything else is **required**).

* **The module itself**, which may be written in any language. Most of them are in Python though, so unless a different language is plain better at what you're trying to do, you should use Python.

* **Unit tests**. These are not optional. Other tests use the [Test Anything Protocol]() for their tests and `prove` to run it.

* **Functional tests** with [101test](https://github.com/101companies/101test). These are a bit more *optional* than unit tests, but you should still have them.

* **module.json** specifying which command is to be run, if you want to use 101diff, which environment variables you need and which other modules depend on it. See also [the schema](schemas/module.schema.json) and [this module.json](modules/predicates101meta/module.json) as an example.

* **README.md**, with a short explanation of what it does and how to use it.

* **Documentation** with a detailed explanation of the module's purpose on [101docs](https://github.com/101companies/101docs).

* **Makefile** with the following targets:

    * **test**, so that your tests can automatically be discovered when you run [./test](test). This command **must** exit with a non-zero exit code if your tests fail.

    * **install** (*optional*), if you need anything that doesn't come with a normal Ubuntu Server installation. These will automatically be discovered by [./install](install) and ***THEY WILL BE RUN WITH SUDO***. Don't go doing anything other than installs in this target. If you need to build your module, put separate target in your Makefile and call it from your `module.json`.

See [pull101repo](modules/pull101repo) as an example. Pretty much all other modules are legacy and don't properly fulfill those requirements though. Don't take them as examples.


## 101diff

TODO


# Cycles

In each 101worker cycle, it validates and then executes a list of modules. See the [module list used in production](configs/production.json).

The idea is that a cronjob performs these commands regularly. Just don't make it run 60 times at once, experience has shown that it don't work too well.

101worker updates itself with `git pull` after each run, so any changes in this repository will be applied in due time.


# Incrementalization Status

Module                      | Status
----------------------------|:--------:
pull101repo                 | ok
pull                        | n/a
pullLibraries               | n/a
build                       | n/a
gatherGeshi                 | n/a
rules101meta                | ok
matches101meta              | ok
metrics101meta              | ok
validate101meta             | ok
extract101meta              | ok
fragmentMetrics101meta      | ok
refineTokens                | **not ok**
predicates101meta           | ok
fragments101meta            | ok
summary101meta              | ok
wiki2json                   | **not ok**
themesExtractor             | **not ok**
languageExtractor           | **not ok**
vocabulary                  | **not ok**
wiki2tagclouds              | **not ok**
moretagclouds               | **not ok**
summarizeModuleDescriptions | **not ok**
members                     | **not ok**
resolve101meta              | **not ok**
index101meta                | **not ok**
repo2charts                 | **not ok**
parseMegaL                  | **not ok**
webDeployMegaModels         | **not ok**
validateModuleDescriptions  | **not ok**
integrate                   | **not ok**
