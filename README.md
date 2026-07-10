# Mini Redis

A Redis-inspired in-memory key-value server built in Python using gevent and a simplified RESP protocol.

## Features

- TCP client/server architecture
- Concurrent client handling with gevent
- RESP request parsing and response serialization
- Key expiration and TTL tracking
- JSON persistence
- Atomic command execution using a semaphore
- Automated tests with pytest

## Supported Commands

SET
GET
DEL
EXISTS
PING
EXPIRE
TTL
INCR
DECR
KEYS
FLUSHDB
SAVE
LOAD
MGET
MSET
RENAME
DBSIZE
TYPE

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt