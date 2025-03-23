# Ricopin Wishlist API

A Django REST API for managing personal wishlists, gift reservations, and user authentication.
Powered by JWT, Docker, Swagger.

---

## Implemented

- JWT-based user authentication at `/api/register` & `/api/login`
- Wishlist management (create, edit, delete wishes) at `/api/wishes`
- Gift reservation system at `/api/wishes/{id}/reserved` & `/api/wishes/{id}/unreserved`
- Unit tests with coverage (see Quickstart)
- Docker
- Swagger API docs at `/swagger`
- Prometheus metrics at `/metrics` + logging in console & file
- Github actions

---

## Quickstart via Docker

```bash
git clone https://github.com/r1copin/wishlist.git
cd wishlist-api
cp example-env.txt .env  # or create your own .env

# Build and run containers
docker-compose up --build

# Run tests with coverage
docker-compose run --rm web sh -c "coverage run manage.py test && coverage report"

