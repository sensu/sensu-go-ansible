Modules
=======

While different modules perform different tasks, their interfaces all follow
the same pattern as much as possible.

The API of each module is composed of two parts. The *auth* parameter contains
the pieces of information that are related to the Sensu Go backend that the
module is connecting to. All other parameters hold the information related to
the resource that we are operating on. A typical task would look like this:

.. code-block:: yaml

   - name: Make sure asset is present
     asset:
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
       namespace: my-namespace
       name: my-asset-name
       builds: ...

If we would like to remove a certain resource from the Sensu backend, we can
write a task and set its *state* parameter to ``absent``:

.. code-block:: yaml

   - name: Make sure asset is absent
     asset:
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
       namespace: my-namespace
       name: my-asset-name
       state: absent

Almost every module for manipulating resources has its counterpart module that
can be used to retrieve information about the corresponding resources, for
instance *asset* and *asset_info* modules.

.. code-block:: yaml

   - name: Fetch a list of all assets
     asset_info:
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
       namespace: my-namespace
     register: result

Note the usage of the *asset_info* module in the example above. We can also
retrieve information about a single asset by adding a *name* parameter to the
previous task:

.. code-block:: yaml

   - name: Fetch a specific asset
     asset_info:
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
       namespace: my-namespace
       name: my-asset-name
     register: result

Info modules always return a list of objects that Sensu API returned. And if
we try to fetch a non-existing resource, the result will hold an empty list.
This makes it easy to write conditional tasks using next pattern:

.. code-block:: yaml

   - name: Fetch a specific asset
     asset_info:
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
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
       auth:
         url: http://sensu.host.com:8080
         user: my-user
         password: pass
       namespace: my-namespace
     register: result

   - name: Display number of builds in an asset
     debug:
       msg: "{{ item.metadata.name }}: {{ item.builds | length }}"
     loop: result.objects

For convenience, modules also consult some environment variables when getting
parameter values. This allows us to remove the *auth* and *namespace*
parameters from task definitions and define them only once:

.. code-block:: yaml

   ---
   - hosts: all
     collections: [ sensu.sensu_go ]
     environment:
       SENSU_URL: http://sensu.host.com:8080
       SENSU_USER: my-user
       SENSU_PASSWORD: pass
       SENSU_NAMESPACE: my-namespace

     tasks:
       - name: Asset task
         asset:
           name: my-asset
           # More parameters here

       - name: Check task
         check:
           name: my-check
           # More parameters here

       # More tasks here

Reference material for each module contains documentation on what parameters
certain modules accept and what values they expect those parameters to be.


.. toctree::
   :glob:
   :maxdepth: 1
   :caption: Available modules

   modules/*
