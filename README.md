# PhoneBook App

## Overview

This is a simple RESTful API with CLI and embedded in-memory key-value data storage for a phonebook application 
built with Aiohttp, Typer and providing the following features:

- REST API for phonebook application built with Aiohttp and Pydantic
- CLI for REST API built with Typer
- Embedded key-value data storage based on JSON format
- Paginated output of Phonebook API entries from the data storage to the screen
- Ability to perform CRUD operations with entry's in Phonebook API with HTTP requests or CLI app
- Ability to perform search queries for entry's by one or more characteristics

## Installation

- Clone this repository and navigate to it:

```bash
git clone https://github.com/paraleipsis/phonebook-app.git && cd phonebook-app
```

- Install project in /src directory (sudo access may be required):

```bash
cd src && python3 -m pip install -e .
```

- Then you can use Docker to start API server in container or just install requirement packages and start server manually:

### Docker

- Run services with Docker Compose:

```bash
docker compose up -d
```

### Packages

- Install requirements:

```bash
pip install -r requirements.txt
```

- Run API server:

```bash
python3 src/core/main.py
```

After installing, you can use CLI to access the API:

```bash
python3 src/cli/main.py --help
```

## Configuration 

Project configuration available through environment variables or /conf/config file:

```bash
nano src/conf/config
```

Logging configuration available in yaml file:

```bash
nano src/logger/conf.yaml
```

