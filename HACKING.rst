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
