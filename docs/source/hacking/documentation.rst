Documenting Sensu Go Ansible collection
=======================================

Documentation for the Sensu Go Ansible collection consists of two distinct
kinds: the general guides and the API documentation. The general guides live
in the ``docs/source`` directory while the API documentation is part of the
modules' source code.


Authoring the documentation
---------------------------

Adding a new piece of general documentation is reasonably straightforward. We
need to create a new file somewhere inside the ``docs/source`` directory and
fill it with reStructuredText-formatted content.

As a general rule, we use two levels of headings: a document title and as many
section titles as needed. If you feel you need something more complex, try
simplifying the documentation first. The end-users will thank you for this.

First few lines of the document you are just reading look like this:

.. literalinclude:: documentation.rst
   :language: rst
   :lines: 1-20

Once we have the content ready, we need to bind it with the rest of the
documentation. We do this by adding our document to one of the ``toctree``
directives. We can find the important ones in the ``index.rst`` file.

We follow the `upstream guides`_ when it comes to documenting the modules,
with one exception: ``version_added`` field holds the Sensu Go collection
version instead of Ansible version. Typical module starts with the next few
lines:

.. literalinclude:: ../../../plugins/modules/handler_set.py
   :language: python
   :lines: 1-30

.. _upstream guides:
   https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html


Publishing the documentation
----------------------------

We use the `ansible-doc-extractor`_ tool to convert the embedded module
documentation into a set of reStructuredText documents. Once we have those
documents ready, we bind the various parts of the documentation together using
Sphinx_. In practice, we just run the ``make docs`` command in the root of the
repository and open the ``docs/build/html/index.html`` file in our browser of
choice.

.. _ansible-doc-extractor: https://github.com/xlab-si/ansible-doc-extractor
.. _Sphinx: https://www.sphinx-doc.org

We use `GitHub Pages`_ for hosting the online version of our documentation. To
update the content of our `documentation site`_, we must copy the rendered
documentation into the ``gh-pages`` branch, commit the changes, and push them
to GitHub. The described procedure translates into the following series of
steps::

    (venv) $ make docs
    (venv) $ git worktree add gh-pages gh-pages
    (venv) $ rm -rf gh-pages/*
    (venv) $ cp -r docs/build/html/* gh-pages
    (venv) $ cd gh-pages
    (venv) $ git add . && git commit
    (venv) $ git push origin gh-pages
    (venv) $ cd ..
    (venv) $ git worktree remove gh-pages

.. _GitHub Pages: https://pages.github.com/
.. _documentation site: https://sensu.github.io/sensu-go-ansible/
