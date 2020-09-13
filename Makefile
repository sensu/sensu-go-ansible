# Make sure we have ansible_collections/sensu/sensu_go as a prefix. This is
# ugly as heck, but it works. I suggest all future developer to treat next few
# lines as an opportunity to learn a thing or two about GNU make ;)
collection := $(notdir $(realpath $(CURDIR)      ))
namespace  := $(notdir $(realpath $(CURDIR)/..   ))
toplevel   := $(notdir $(realpath $(CURDIR)/../..))

err_msg := Place collection at <WHATEVER>/ansible_collections/sensu/sensu_go
ifneq (sensu_go,$(collection))
  $(error $(err_msg))
else ifneq (sensu,$(namespace))
  $(error $(err_msg))
else ifneq (ansible_collections,$(toplevel))
  $(error $(err_msg))
endif

python_version := $(shell \
  python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))' \
)


.PHONY: help
help:
	@echo Available targets:
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort

.PHONY: sanity
sanity:  ## Run sanity tests
	pip install -r sanity.requirements -r collection.requirements
	flake8
	if which ansible-lint 2> /dev/null; then ansible-lint -p roles/*; fi
	ansible-test sanity --python $(python_version) --requirements
	./tests/sanity/validate-role-metadata.py roles/*

.PHONY: units
units:  ## Run unit tests
	pip install -r collection.requirements
	-ansible-test coverage erase # On first run, there is nothing to erase.
	ansible-test units --python $(python_version) --coverage --requirements
	ansible-test coverage html

.PHONY: integration
integration:  ## Run integration tests
	pip install -r integration.requirements -r collection.requirements
	$(MAKE) -C tests/integration $(CI)

.PHONY: docs
docs:  ## Build collection documentation
	$(MAKE) -C docs -f Makefile.custom docs

.PHONY: clean
clean:  ## Remove all auto-generated files
	$(MAKE) -C docs -f Makefile.custom clean
	rm -rf tests/output
