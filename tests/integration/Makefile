modules   := $(wildcard molecule/module_*)
roles     := $(wildcard molecule/role_*)
scenarios := $(modules) $(roles)


.PHONY: all
all: $(scenarios)

.PHONY: modules
modules: $(modules)

.PHONY: roles
roles: $(roles)

.PHONY: $(modules) $(roles)
$(modules) $(roles):
	molecule -c base.yml test --parallel -s $(notdir $@)
