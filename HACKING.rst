Developing Sensu Go Ansible Collection
======================================

So, you have decided to help us out. Great! Let us set up a development
environment together, and then you can start hacking ;)

Preparing a development environment
-----------------------------------

The first thing we need to do is create a new virtual environment and activate
it::

   $ cd /path/to/desired/directory
   $ python3 -m venv venv
   $ . venv/bin/activate

Next, we need to clone the source code::

   (venv) $ mkdir -p ansible_collections/sensu
   (venv) $ cd ansible_collections/sensu
   (venv) $ git clone git@github.com:sensu/sensu-go-ansible.git sensu_go

It is vitally important that we create two parent directories before checking
out the code and that you clone the code into the `sensu_go` directory.
Ansible development tools often assume that we are working from the
``ansible_collections/<namespace>/<collection>`` directory.

Now we need to install Ansible. At the moment, we can only use prerelease
Ansible versions greater or equal to ``2.9.0rc4``. We can get the appropriate
version by running::

   (venv) $ pip install --pre ansible

All that separates now from the fully functioning development environment is a
few dependencies. We can install them by running the next command::

   (venv) $ pip install \
              -r sanity.requirements \
              -r units.requirements \
              -r integration.requirements

And this is it. We are all set now. To validate our setup, we can run the
bundled tests::

   (venv) $ ansible-test sanity --python 3.7
   (venv) $ ansible-test units --python 3.7
   (venv) $ export ANSIBLE_COLLECTIONS_PATHS=$(pwd)/../../..
   (venv) $ cd tests/integration/modules
   (venv) $ molecule --base-config molecule/shared/base.yml test --all

.. note::
   In the example above, we used ``--python 3.7`` switch because we are using
   python 3.7 in our virtual environment. You can find appropriate value for
   your environment by first running ``python --version`` and using only major
   and minor version numbers.

All green? Great!

Before you start preparing the best pull request ever, let us quickly talk
about that ``ANSIBLE_COLLECTIONS_PATHS`` export. Ansible looks at the contents
of this environment variable to determine where it should look for the
collections. Development tools that are part of the `ansible` package do
something similar internally, and this is why we do not need to set this
environment variable when running ``ansible-test``. But ``molecule`` is a
general-purpose tool and knows nothing about Ansible's internal hackery.
So it is up to us to set up the execution environment before running the
integration tests.


Adding a new integration test
-----------------------------

Integration tests are a vital part of the Sensu Go Ansible collection. We use
them to make sure our modules and roles work with the supported set of Sensu
Go and Ansible versions.

Integration tests live in the ``tests/integration/molecule`` directory. As you
may have already guessed, we use Molecule to manage our integration tests. We
can add a new test scenario by creating a suitably named directory and
populating it with a ``playbook.yml`` playbook and ``molecule.yml``
configuration file.

If we are creating an integration test for a module, we can leave the molecule
configuration empty. But we must still create the configuration file, or
Molecule will not detect this scenario. For example, if we would like to
create a new Molecule scenario that is testing the ``asset`` module, we would
run this sequence of commands::

   $ cd tests/integration
   $ mkdir molecule/module_asset
   $ touch molecule/module_asset/molecule.yml

Now we need to write down the ``molecule/module_asset/playbook.yml`` playbook
that contains the actual test using ``vim``. And yes, the ``vim`` part is
mandatory ;)

Once we have our playbook ready, we can test our scenario by running::

   $ molecule --base-config base.yml test -s module_asset

One thing we need to make sure before we run this command is that we have
``ANSIBLE_COLLECTIONS_PATHS`` environment variable set as shown in the
quickstart section. And this is all there is to it.
