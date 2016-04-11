# Pytrader v2

Thanks to the wild interest in pytrader, core developers determined that it would be valuable to review and rebuild pytrader into a lighter, faster platform with better group-working capabilities

## Important changes from V1
* **Python 3**  Pytrader V2 targets Python 3.5 as it's primary language, moving from Python 2.7
* **Test-Driven Core** The core modules of Pytrader V2 are designed to be developed, built, and run under TDD procedures
* **Expandable Worker Sets** Unlike the limitations of single-worker setups, even with threading, Pytrader V2 is designed to harness large numbers of systems for asyncronous, long-running jobs.

## Main Feature Designs
* REST driven system, allowing for multiple frontends and expansion in the future
* Workers are designed to be easily upgraded for new neural networks
* Multiple user authentication designed from the ground up to allow users to host more than one user on an instance
* Multiple trade market support built in from the ground up
* Designed to be PEP8 Compliant

## App Layout
* rest_api - Main system for running pytrader
    * celery_jobs - All jobs that need to be run/handled in celery
* neural_network_worker - Handles all neural networking processes

## Design Considerations
* Asynchronous jobs need to be written to be run in the background in celery
* Long-running neural-networking tasks need to be designed/built to be run remotely in the remote worker.
    * Communicates via OAuth and the main REST API
* REST API
    * Utilizes [hug](https://github.com/timothycrosley/hug)
    * ORM - SQLAlchemy
    * Caching - Redis

## Architecture
V2 of pytrader is designed to be highly scalable and easy to do for the average user, in consideration of such, the application is being built so that heavy/long running tasks are abstracted from the main program flow, and are easier to edit.  Architecturally, we are utilizing the following bits and pieces:
* Docker
    * Chosen to support as many systems as possible
    * docker-compose.yml file provided to bring up all systems
* MySQL
    * Designed to run with Percona/Galera Clusters for the high levels of reads
    * App does not use high levels of writes, so MySQL is the proper choice
* Redis
    * Serves as a key-value store (Cache)
    * Serves as a backend for celery tasks

This overall abstraction allows for the breaking out of bits and pieces from the main docker system, and scaling out applications in sync as needed to support more parts, in particular, the celery apps + remote workers.