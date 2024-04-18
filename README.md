# Crypto Exchange Services
It's a simple project that simulates a crypto exchange service. It's a REST API that allows users to create accounts, deposit money, buy and sell cryptocurrencies, and check their balance.

## Technologies
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Docker

## How to run
1. Clone the repository
2. Run `cd crypto_exchange`
3. Run `docker compose -f deployment/docker-compose up -d`

## Accessing the API
The API is available at `http://localhost:8000/swagger`

## Default users
- username: `user0`, password: `password`