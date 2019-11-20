stomp, stomper, stompest!
=========================

stompest is a full-featured [STOMP](http://stomp.github.com/) [1.0](http://stomp.github.com//stomp-specification-1.0.html), [1.1](http://stomp.github.com//stomp-specification-1.1.html), and [1.2](http://stomp.github.com//stomp-specification-1.2.html) implementation for Python 2.7 and Python 3 (versions 3.3 and higher) including both synchronous and asynchronous clients:

* The `sync.Stomp` client is dead simple. It does not assume anything about your concurrency model (thread vs process) or force you to use it any particular way. It gets out of your way and lets you do what you want.
* The `twisted.Stomp` client is based on [Twisted](http://twistedmatrix.com/), a very mature and powerful asynchronous programming framework. It supports destination specific message and error handlers (with default "poison pill" error handling), concurrent message processing, graceful shutdown, and connect and disconnect timeouts.

Both clients support [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security) for secure connections to ActiveMQ, and both clients make use of a generic set of components in the `protocol` module, each of which can be used independently to roll your own STOMP client:

* a wire-level STOMP frame parser `protocol.StompParser` and compiler `protocol.StompFrame`,

* a faithful implementation of the syntax of the STOMP protocol with a simple stateless function API in the `protocol.commands` module,

* a generic implementation of the STOMP session state semantics in `protocol.StompSession`, such as protocol version negotiation at connect time, heart-beating, transaction and subscription handling (including a generic subscription replay scheme which may be used to reconstruct the session's subscription state after a forced disconnect),

* and `protocol.StompFailoverTransport`, a [failover transport](http://activemq.apache.org/failover-transport-reference.html) URI scheme akin to the one used in ActiveMQ.

This package is thoroughly unit tested and production hardened for the functionality used by the current maintainer and by [Mozes](http://www.mozes.com/) — persistent queueing on [ActiveMQ](http://activemq.apache.org/). Minor enhancements may be required to use this STOMP adapter with other brokers.

Installation
============

* If you do not wish to use the asynchronous client (which depends on Twisted), stompest is fully self-contained.
* You can find all stompest releases on the [Python Package Index](http://pypi.python.org/pypi/stompest/). Just use the method you like most: `easy_install stompest`, `pip install stompest`, or `python setup.py install`.

Documentation & Code Examples
=============================

The stompest API is fully documented [here](http://nikipore.github.com/stompest/).

Building
--------

To *build* the documentation, you'll need a source checkout, and then first install the documentation dependencies into your virtual environment:

```
(env) $ pip install -e .[doc]
```

Then you can build the documentation in the `doc/` directory:

```
(env) $ cd doc/
(env) $ make html
```

The HTML documentation will be in the directory `doc/stompest-doc`.

Questions or Suggestions?
=========================
Feel free to open an issue [here](https://github.com/nikipore/stompest/issues/) or post a question on the [forum](http://groups.google.com/group/stompest/).

Features
========

Commands layer
--------------
* Transport and client agnostic.
* Full-featured implementation of all STOMP client commands.
* Client-side handling of STOMP commands received from the broker.
* Stateless and simple function API.

Session layer
-------------
* Manages the state of a connection.
* Replays subscriptions upon reconnect.
* Heart-beat handling.

Failover layer
--------------
* Mimicks the [failover transport](http://activemq.apache.org/failover-transport-reference.html) behavior of the native ActiveMQ Java client.
* Produces a (possibly infinite) sequence of broker network addresses and connect delay times.

Parser layer
------------
* Abstract frame definition.
* Transformation between these abstract frames and a wire-level byte stream of STOMP frames.

Clients
=======

`sync`
------
* Built on top of the abstract layers, the synchronous client adds a TCP connection and a synchronous API.
* The concurrency scheme (synchronous, threaded, ...) is free to choose by the user.

`twisted`
-------
* Based on the Twisted asynchronous framework.
* Fully unit-tested including a simulated STOMP broker.
* Graceful shutdown: on disconnect or error, the client stops processing new messages and waits for all outstanding message handlers to finish before issuing the `DISCONNECT` command.
* Error handling - fully customizable on a per-subscription level:
    * Disconnect: if you do not configure an errorDestination and an exception propagates up from a message handler, then the client will gracefully disconnect. This is effectively a `NACK` for the message (actually, disconnecting is the only way to `NACK` in STOMP 1.0). You can [configure ActiveMQ](http://activemq.apache.org/message-redelivery-and-dlq-handling.html) with a redelivery policy to avoid the "poison pill" scenario where the broker keeps redelivering a bad message infinitely.
    * Default error handling: passing an error destination parameter at subscription time will cause unhandled messages to be forwarded to that destination and then `ACK`ed.
    * Custom hook: you can override the default behavior with any customized error handling scheme.
* Separately configurable timeouts for wire-level connection, the broker's `CONNECTED` reply frame, and graceful disconnect (in-flight handlers that do not finish in time).

Acknowledgements
================
* Version 1.x of stompest was written by [Roger Hoover (@theduderog)](http://github.com/theduderog) at [Mozes](http://www.mozes.com/) and deployed in their production environment.
* Kudos to [Oisin Mulvihill](https://github.com/oisinmulvihill), the developer of [stomper] (https://github.com/oisinmulvihill/stomper)! His idea of an abstract representation of the STOMP protocol lives on in stompest.

Anyone willing to take over this project?
=========================================
I am no longer using stompest actively, because I have moved on inside my enterprise —
 which still uses stompest in production but has no-one with both the skill and time to maintain it — to a non-coding strategic/leadership position. Therefore, it is more of a hobby, and I have to rebuild my coding, testing and building environment from scratch every few months which rather sucks.

A few random thoughts:

0. I still do accept (and test) pull requests and bugfixes (if they come with complete and working unit and integration tests), but the Python 3 port was my last big effort for stompest.
1. I believe that fully implementing the (half-complete) SSL/TLS capability is the most urgent enhancement because apart of that I consider stompest pretty much feature complete and very stable up to Python 3.6; the rate of newly discovered bugs is very low indeed.
2. A port of the Twisted client to `asyncio` would make a lot of sense. If someone creates a pull request, I'll test it and create a new PyPI package.
3. If someone would like to take over the project, please let me know. I would actively consult as an *éminence grise*.

To Do
=====
* see [proposed enhancements](https://github.com/nikipore/stompest/issues?labels=enhancement&state=open)
