.. _`contributing`:

============
Contributing
============

If you’re reading this, you’re probably interested in contributing to EasyData. Thank
you very much! Open source projects live-and-die based on the support they receive
from others, and the fact that you’re even considering contributing to the EasyData
project is *very* generous of you.

.. important::

    Double check that you are reading the most recent version of this document at
    https://easydata.readthedocs.io/en/latest/contributing.html

There are many ways to contribute to EasyData. Here are some of them:

* Report bugs and request features in the `issue tracker`_, trying to follow
  the guidelines detailed in `Reporting bugs`_ below.

* Blog about EasyData. Tell the world how you're using EasyData. This will help
  newcomers with more examples and will help the EasyData project to increase its
  visibility.

* Submit *pull requests* for new functionalities and/or bug fixes. Please read
  *:ref:`how-to-contribute`* instructions below for details on how to
  write and submit a *pull request*.

Reporting bugs
==============

Well-written bug reports are very helpful, so keep in mind the following
guidelines when you're going to report a new bug.

* check the `open issues`_ to see if the issue has already been reported. If it
  has, don't dismiss the report, but check the ticket history and comments. If
  you have additional useful information, please leave a comment, or consider
  to open a *pull request* with a fix.

* write **complete, reproducible, specific bug reports**. The smaller the test
  case, the better. Remember that other developers won't have your project to
  reproduce the bug, so please include all relevant files required to reproduce
  it. See for example StackOverflow's guide on creating a
  `Minimal, Complete, and Verifiable example`_ exhibiting the issue.

* the most awesome way to provide a complete reproducible example is to send a pull
  request which adds a failing test case. This is helpful even if you don't have an
  intention to fix the issue yourselves.

* include the version of EasyData so developers working on your bug
  know exactly which version and platform it occurred on, which is often very
  helpful for reproducing it, or knowing if it was already fixed.

.. _Minimal, Complete, and Verifiable example: https://stackoverflow.com/help/mcve

.. _how-to-contribute:

How do I make a contribution?
=============================

Never made an open source contribution before? Wondering how contributions work in
our project? Here's a quick rundown!

1. Find an issue that you are interested in addressing or a feature that you would like to add.
2. Fork the repository associated with the issue to your local GitHub organization. This means
   that you will have a copy of the repository under ``your-GitHub-username/easydata``.
3. Clone the repository to your local machine using ``git clone https://github.com/sitegroove/easydata.git``.
4. Create a new branch for your fix using ``git checkout -b #issue-num/title-of-issue-fix``.
5. Make the appropriate changes for the issue you are trying to address or the feature that
   you want to add.
6. Use ``git add insert-paths-of-changed-files-here`` to add the file contents of the
   changed files to the "snapshot" git uses to manage the state of the project, also
   known as the index.
7. Use ``git commit -m "Insert a short message of the changes made here"`` to store the
   contents of the index with a descriptive message.
8. Push the changes to the remote repository using git push origin branch-name-here.
9. Submit a pull request to the upstream repository.
10. Title the pull request with a short description of the changes made and the issue or bug
    number associated with your change. For example, you can title an issue like so
    ``"Added more log outputting to resolve #4352"``.
11. In the description of the pull request, explain the changes that you made, any issues you
    think exist with the pull request you made, and any questions you have for the maintainers.
    It's OK if your pull request is not perfect (no pull request is), the reviewer will be able
    to help you fix any problems and improve it!
12. Wait for the pull request to be reviewed by a maintainer.
13. Make changes to the pull request if the reviewing maintainer recommends them.
14. Celebrate your success after your pull request is merged!

.. note::
    Try to keep code style changes (*PEP* 8 compliance, unused imports removal, etc)
    in separate commits since this will make pull requests easier to review and more likely
    to get merged.

.. _coding-style:

Coding style
============

Please follow coding conventions listed bellow when writing code:

* Follow *PEP 8*.

* Line limit is **88** instead of recommended 79. This is because *black* code formatter
  prefers it.

* Don't put your name in the code you contribute since git provides enough metadata to
  identify author of the code.
  See https://help.github.com/en/github/using-git/setting-your-username-in-git for
  setup instructions.

Auto formatting
---------------

EasyData uses *black* and *isort* for automatic code formatting, so that we can focus
more on a fixing problem or new feature implementation that code formatting.

Right before you open open PR, please use::

    tox -e format

This will automatically run *black* and *isort* formatters so that code can be PEP 8
compliant.

Check for PEP 8 compliance
--------------------------

To run a check for PEP 8 compliance please use::

    tox -e lint

Tests
=====

Tests are implemented using the pytest.

.. _running-tests:

Running tests
-------------

To run tests locally please use::

    tox -e py3

To run a specific test (for example ``tests/test_models.py``) use::

    tox -e py3 -- tests/test_models.py

To run the tests on a specific tox environment, use ``-e <name>`` with an environment
name from ``tox.ini``. Example how to run tests with Python 3.6::

    tox -e py36

All tests runs will produce at the end of console output also coverage report.

Writing tests
-------------

All added new functionality (including new features and bug fixes) must include
a test case in order to check that everything works as expected, so please include
test cases for your patches, otherwise PR won't get merged.

EasyData uses *pytest*, which are located in the ``tests/`` directory.

Code of Conduct
===============

Our Pledge
----------

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to making participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, gender identity and expression, level of experience,
nationality, personal appearance, race, religion, or sexual identity and
orientation.

Our Standards
-------------

Examples of behavior that contributes to creating a positive environment
include:

* Using welcoming and inclusive language
* Being respectful of differing viewpoints and experiences
* Gracefully accepting constructive criticism
* Focusing on what is best for the community
* Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

* The use of sexualized language or imagery and unwelcome sexual attention or
  advances
* Trolling, insulting/derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or electronic
  address, without explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

Our Responsibilities
--------------------

Project maintainers are responsible for clarifying the standards of acceptable
behavior and are expected to take appropriate and fair corrective action in
response to any instances of unacceptable behavior.

Project maintainers have the right and responsibility to remove, edit, or
reject comments, commits, code, issues, and other contributions that are not
aligned to this Code of Conduct, or to ban temporarily or permanently any
contributor for other behaviors that they deem inappropriate, threatening,
offensive, or harmful.

Attribution
-----------

This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 1.4,
available at [http://contributor-covenant.org/version/1/4][version]

[homepage]: http://contributor-covenant.org
[version]: http://contributor-covenant.org/version/1/4/


.. _tests/: https://github.com/sitegroove/easydata/tree/master/tests
.. _open issues: https://github.com/sitegroove/easydata/issues
.. _issue tracker: https://github.com/sitegroove/easydata/issues
.. _pull request: https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request

Note: *Contributing section was inspired by *scrapy* contributing guidelines.*
