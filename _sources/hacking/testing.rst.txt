Testing Sensu Go Ansible Collection
===================================

Sensu Go Ansible collection contains a comprehensive test suite. We use this
test suite to make sure collection's source code

1. meets the Ansible code quality standards,
2. works with supported versions of Ansible,
3. works with supported versions of Sensu Go, and
4. works with supported versions of Python.


Sanity tests
------------

We use ``ansible-test sanity`` command to run wide variety of static analysis
tools over our source code. This command, among other things, makes sure that
our module documentation does not get out-of-sync with the argument
specification; that our code is python 2 and 3 compatible; and that we follow
the standard source code formatting conventions.

We can run the sanity test by running::

   (venv) $ make sanity

This command will take care of detecting our python version and running
``ansible-test sanity`` test with the right parameters.

We do not have to write those tests ourselves since they come bundled with
``ansible-test`` command. All we have to do is to run them regularly. Our CI
setup also runs them on each push to GitHub, making sure that upstream source
code is clean at all times.


Unit tests
----------

We use unit tests to test the logic and implementation of our helper functions
and various Ansible plugins that are part of the Sensu Go collection.

Unit tests live in the ``tests/unit`` directory and mirror the structure of
the code. For example, unit tests for the code in the
``plugins/modules/asset.py`` are stored in the
``tests/unit/modules/test_asset.py`` file. When we add new code to the
collection, we must also include the tests for this piece of code in the same
git commit.

We group our tests using classes. Each function or method gets its own
dedicated test class that contains one or more tests that check different
aspects of the code under scrutiny.

We use ``ansible-test units`` to execute the unit tests. But we can also
execute::

   (venv) $ make units

to run them. This convenience ``make`` rule will again select the appropriate
python version and run the unit tests. Additionally, it will also generate a
code coverage report and place it in the
``tests/output/reports/coverage/index.html`` HTML file.

Our CI process runs unit tests on each push to GitHub. And while developers
usually run the tests only against one version of Ansible and python, CI tools
run them against all supported versions, making sure our code is ready to be
used on a variety of systems.


Integration tests
-----------------

Integration tests are basically a collection of Ansible playbooks that we run
against all supported Sensu Go versions and operating systems. Integration
tests live in the ``tests/integration/molecule`` directory. We use Molecule_
to manage our integration tests.

.. _Molecule: https://molecule.readthedocs.io/en/stable/

We can add a new test scenario by creating a suitably named directory and
populating it with a ``playbook.yml`` playbook and ``molecule.yml``
configuration file.

If we are creating an integration test for a module, we can leave the molecule
configuration file empty. But we must still create the configuration file, or
Molecule will not detect this scenario. For example, if we would like to
create a new Molecule scenario that is testing the ``asset`` module, we would
run this sequence of commands::

   (venv) $ mkdir tests/integration/molecule/module_asset
   (venv) $ touch tests/integration/molecule/module_asset/{molecule,playbook}.yml

Now we need to add some content to the playbook we just created. There are
plenty of examples in our test directory if you need some inspiration ;)

Once we have our playbook ready, we can test our scenario by running::

   (venv) $ make tests/integration/molecule/module_asset

We can also run all integration tests with a single command:

   (venv) $ make integration

Do note that this will take about an hour or so, so make sure you have
something else to do in the mean time ;)

Adding a scenario for role is a bit more complicated since we need to inform
Molecule what docker images it should use for running tests, but nothing
drastic.

We run our integration tests as part of our CI process, further reducing the
chances of broken code getting into our repository.


Continuous integration
----------------------

We use CircleCI to run our test suite on each push and pull request. Our CI
pipeline is composed of two stages: a fast one and a slow one.

The fast stage is composed of sanity and unit tests. Once those tests are done
executing and passing, we start execution of the slow stage that runs
integration tests.

In order to keep the test times as short as possible, the slow stage is
parallelized. And in order to maximize the benefits of this parallel
execution, we need to split the work into similarly sized chunks. This is done
automatically on CircleCI based on the timings from the previous runs.
