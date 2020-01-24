modules   := $(wildcard molecule/module_*)
roles     := $(wildcard molecule/role_*)
actions   := $(wildcard molecule/action_*)
misc      := $(wildcard molecule/misc_*)
scenarios := $(modules) $(roles) $(actions) $(misc)

# Make sure ansible can find our collection without having to install it.
export ANSIBLE_COLLECTIONS_PATHS ?= $(realpath $(CURDIR)/../../../../..)


.PHONY: all
all: $(scenarios)

.PHONY: modules
modules: $(modules)

.PHONY: roles
roles: $(roles)

.PHONY: actions
actions: $(actions)

.PHONY: misc
misc: $(misc)

.PHONY: $(scenarios)
$(scenarios):
	molecule -c base.yml test --parallel -s $(notdir $@)

# CI stuff - partitioning logic ("true" is the value of the $CI variable)
.PHONY: true
true:
	cut -d" " -f1 scenario.times | sort > times.tmp
	find molecule/ -mindepth 1 -maxdepth 1 -type d | sort > dirs.tmp
	diff times.tmp dirs.tmp
	$(MAKE) $$(python partition.py scenario.times)
