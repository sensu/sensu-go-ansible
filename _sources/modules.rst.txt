Modules
=======

While different modules perform different tasks, their interfaces all follow
the same pattern as much as possible. For example, all Sensu Go modules
support check mode, most of them can have their state set to either
``present`` or ``absent``, and they identify the resource to operate on using
the *name* and *namespace* parameters.

The API of each module is composed of two parts. The *auth* parameter contains
the pieces of information that are related to the Sensu Go backend that the
module is connecting to. All other parameters hold the information related to
the resource that we are operating on.


Authentication parameters
-------------------------

Each module has an *auth* parameter that holds the following information about
the Sensu Go backend:

1. The **url** key holds the address of the Sensu Go backend. If this key is
   not present in the task's definition, Ansible will consult the *SENSU_URL*
   environment variable and, if the variable is not set, use the default value
   of ``http://localhost:8080``.
2. The **user** and **password** keys contain the credentials that the module
   will use when connecting to the backend. It not present, Ansible will try
   to look up the *SENSU_USER* and *SENSU_PASSWORD* environment variables,
   falling back to the default values of ``admin`` and ``P@ssw0rd!``.
3. The **api_key** field should contain an `API key`_ that module will use to
   authenticate with the backend. If not present, Ansible will try to use the
   value stored in the *SENSU_API_KEY*.

.. _API key:
   https://docs.sensu.io/sensu-go/latest/guides/use-apikey-feature/

.. note::

   The API key authentication is only available in Sensu Go 5.15 or newer.

When Ansible tries to connect to the Sensu Go backend, it will try to
authenticate using the API key. If the *api_key* is not set, Ansible will
fallback to using the *user* and *password* values for authentication. What
this basically means is that there are two valid sets of *auth* parameters:

.. code-block:: yaml

   - name: Use API key authentication
     asset:
       auth:
         url: http://my.sensu.host:8765
         api_key: 7f63b5bc-41f4-4b3e-b59b-5431afd7e6a2
       # Other asset parameters here

   - name: Use user and password authentication
     asset:
       auth:
         url: http://my.sensu.host:8765
         user: my-user
         password: my-password
       # Other asset parameters here

It is not an error to specify all four parameters when writing an Ansible
task, but the *user* and *password* fields are ignored in this case:

.. code-block:: yaml

   - name: Use API key authentication and ignore user and password values
     asset:
       auth:
         url: http://my.sensu.host:8765
         user: my-user          # IGNORED
         password: my-password  # IGNORED
         api_key: 7f63b5bc-41f4-4b3e-b59b-5431afd7e6a2
       # Other asset parameters here

.. note::

   If the *api_key* parameter is set to an invalid value, Ansible will **NOT**
   fallback to the second method of authentication. Instead, it will report
   an error and abort the run.


Managing Sensu Go resources
---------------------------

There are three things we can do using the Sensu Go Ansible modules:

1. Make sure that the specified resource is present on the backend.
2. Make sure that the named resource is not present on the backend.
3. List all currently available resources on the backend.

.. note::

   We left out the *auth* parameter from the following examples in order to
   keep them short and readable.

A typical task for creating (and by *creating* we mean *making sure it
exists*) a resource on the backend would look like this:

.. code-block:: yaml

   - name: Make sure asset is present
     asset:
       namespace: my-namespace
       name: my-asset-name
       # Other asset parameters go here

We need to specify the resource's name and decide into what namespace to place
it if the resource is not a cluster-wide resource. There are a few exceptions
to this rule, but not many.

If we would like to remove a certain resource from the Sensu backend (and by
*remove* we mean *make sure it is not present*), we can write a task and set
its *state* parameter to ``absent``:

.. code-block:: yaml

   - name: Make sure asset is absent
     asset:
       namespace: my-namespace
       name: my-asset-name
       state: absent

Almost every module for manipulating resources has its counterpart module that
can be used to retrieve information about the corresponding resources, for
instance *asset* and *asset_info* modules.

.. code-block:: yaml

   - name: Fetch a list of all assets
     asset_info:
       namespace: my-namespace
     register: result

Note the usage of the *asset_info* module in the example above. We can also
retrieve information about a single asset by adding a *name* parameter to the
previous task:

.. code-block:: yaml

   - name: Fetch a specific asset
     asset_info:
       namespace: my-namespace
       name: my-asset-name
     register: result

Info modules always return a list of objects that Sensu API returned. And if
we try to fetch a non-existing resource, the result will hold an empty list.
This makes it easy to write conditional tasks using next pattern:

.. code-block:: yaml

   - name: Fetch a specific asset
     asset_info:
       namespace: my-namespace
       name: my-asset-name
     register: result

   - name: Do something if asset is there
     debug:
       msg: We are doing something
     when: result.objects | length == 1

Of course, you can also loop over the result using a *loop* construct:

.. code-block:: yaml

   - name: Fetch a list of all assets
     asset_info:
       namespace: my-namespace
     register: result

   - name: Display number of builds in an asset
     debug:
       msg: "{{ item.metadata.name }}: {{ item.builds | length }}"
     loop: result.objects

Reference material for each module contains documentation on what parameters
certain modules accept and what values they expect those parameters to be.


Module reference
----------------

.. toctree::
   :glob:
   :maxdepth: 1

   modules/*
