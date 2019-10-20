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

# Make sure ansible can find our collection without having to install it.
export ANSIBLE_COLLECTIONS_PATHS := $(realpath $(CURDIR)/../../..)


.PHONY: help
help:
	@echo Available targets:
	@fgrep "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort

.PHONY: docs
docs:  ## Build collection documentation
	$(MAKE) -C docs -f Makefile.custom docs

.PHONY: clean
clean:  ## Remove all auto-generated files
	$(MAKE) -C docs -f Makefile.custom clean
