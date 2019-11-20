.. _developing:

If you are hacking on stompest itself, it's important to know how to run the
test suite.

Running the integration tests
=============================

In addition to plain unit tests, Stompest also ships with integration tests
where you can run a test suite against a real STOMP broker (see
``src/core/stompest/tests/__init__.py`` for connection details). This document
walks through how to do that.

Installing ActiveMQ
-------------------

Please refer to the ActiveMQ documentation for official installation
instructions. Here is a quick way to get started in a development (non
production) environment.

Install ActiveMQ into /opt::

  cd /tmp
  wget https://archive.apache.org/dist/activemq/5.15.2/apache-activemq-5.15.2-bin.tar.gz
  tar xzf apache-activemq-5.15.2-bin.tar.gz
  sudo mv /tmp/activemq/apache-activemq-5.15.2 /opt
  sudo ln -s /opt/apache-activemq-5.15.2/ /opt/apache-activemq

Edit the default config so that only the ``stomp`` and ``stomp+ssl`` transports
are enabled::

  vim /opt/apache-activemq/conf/activemq.xml

  ...

        <transportConnectors>
            <transportConnector name="stomp" uri="stomp://0.0.0.0:61613"/>
            <transportConnector name="stomp+ssl" uri="stomp+ssl://0.0.0.0:61612"/>
        <transportConnectors>

Start the activemq service::

  sudo /opt/apache-activemq-5.15.2/bin/activemq start

You should see the activemq service listening on the two ports (61612 for SSL
and 61613 for plaintext).

Getting Stompest from Git
-------------------------

Set up a new virtualenv for stompest::

  git clone https://github.com/nikipore/stompest
  cd stompest
  virtualenv venv
  . venv/bin/activate

Running the twisted integration tests
-----------------------------------

In this example we will run the twisted (non-core) integration tests. We must
install Twisted's tls support so the SSL tests can pass::

  pip install twisted[tls]

Now, switch to the "twisted" code location and run the test suite::

  cd src/twisted
  make test

The integration tests should pass.

::

  ...
  ... (lots of output here) ...
  ...
  --------------------------------------------------------------------
  Ran 42 tests in 35.205s

  OK

Let's say you add your new bugfix or feature, and then you also update the
tests to reflect this. You can run your single test while you develop.

::

  python -m unittest stompest.twisted.tests.twisted_client_test.AsyncClientConnectErrorTestCase

This allows you to test only the specific code you may be editing.

When you are done, it's a good idea to run the full suite with ``make test``
again.
