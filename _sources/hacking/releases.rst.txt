Releasing the Sensu Go Ansible Collection
=========================================

The Sensu Go Ansible collection is primarily available from `Ansible Galaxy`_
and `Automation Hub`_. Which means that we need to get our content up there
somehow. But before we can start uploading things, we need to do some chores
first.

.. _Ansible Galaxy:
   https://galaxy.ansible.com/sensu/sensu_go

.. _Automation Hub:
   https://cloud.redhat.com/ansible/automation-hub/sensu/sensu_go


First, we need to tag the commit and move the ``stable`` branch forward::

   $ VERSION=$(grep version: galaxy.yml | cut -d" " -f2)
   $ git tag -am "Version $VERSION" v$VERSION
   $ git branch -f stable v$VERSION

Now, we need to package the collection. Because the ``ansible-galaxy
collection build`` command will package anything that it can find next to the
``galaxy.yml`` file, we need to execute it in a clean environment. This is why
we will temporarily check out the *stable* branch into the *release*
subdirectory, build the collection package, and then delete the checkout. This
translates into the following sequence of commands::

   $ git worktree add release stable
   $ cd release
   $ ansible-galaxy collection build
   $ mv sensu-sensu_go-$VERSION.tar.gz ..
   $ cd ..
   $ git worktree remove release

Now we can upload the package to Ansible Galaxy::

   $ API_KEY=api-key-from-https://galaxy.ansible.com/me/preferences
   $ ansible-galaxy collection publish \
       --api-key "$API_KEY" \
       sensu-sensu_go-$VERSION.tar.gz

Last thing we need to do is push the ``stable`` branch and created tag to the
GitHub and attach the package to the GitHub release::

   $ git push origin stable v$VERSION

We need to attach the asset manually at the moment. Fully automated solution
is in the works.
