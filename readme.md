# Welcome

This is an opinionated project template emphasizing productivity, allowing development for a project to hit the ground running.

# Stack

## server - NGINX Unit, Python 3.10

Handles high level routing for the entire application and natively serves static files, and the backend Django ASGI. Proxies the appropriate upstream containers and services to the public.

### Quick Start

#### Get current configuration
```sh
# The unitd api is exposed during development,
# Requests can be made from host or over ssh
curl localhost:8090
```

#### Put new configuration
```sh
# The unitd api is exposed during development
cd /srv/www/server/
cat unit.conf.dev.json | curl -X PUT -d@- localhost:8090/config
```

## api - Django 4.0
`Unit`: `http://localhost:8000/api` -> `https://example.com/api`

Django provides the versatility and utilitarianism available only through Python3.

Django's ORM provides robust models, clear fields and relationships with a distinctly powerful query system that trivializes the capability to reach across multiple table relationships.

For API endpoints, this template emphasizes use of [The Django Rest Framework](https://www.django-rest-framework.org/)

Additionally, Django provides a built in administration site for managing users, permissions and other entries for models in your project.

### Models and Migrations

``` python
# Create your model
# blog.models

class BlogPost(BaseModel):
    author = models.ForeignKey("account.user", on_delete=models.CASCADE)
    title = models.CharField(min_length=25)
    body = models.TextField()
    published = models.BooleanField(default=True)
```

``` bash
# Generate your migration files for the blog app

python manage.py makemigrations blog
```

``` bash
# Apply all your migrations to the database

python manage.py migrate
```

``` python
# Query for all blog entries containing "Spokane" in the title,
# and were authored by an administrator

entries = BlogPost.objects.filter(title__icontains="Spokane", author__is_superuser=True)
```

### Automatic schema generation

This template's api is self documenting, with three separate ways to browse.

These can be managed from `core.urls` and `core.settings`.

#### Swagger Schema
`localhost:8000/api/` or `localhost:8090/api/swagger/`

#### Redoc
`localhost:8000/api/redoc/`

#### Browsable, self describing endpoints
i.e. `localhost:8000/api/account/register`

### Views and Model ViewSets

ViewSets should be kept as simple as possible. Let the abstraction work for you, not against you. Following the guidelines below will make configuring views a breeze.

1. Defining the base queryset that requests will build on.
2. Defining and performing all permission checks for requests.
3. Instantiating serializers with data to be processed.
4. Returning the validated serializer response.

All object mutations must be handled by the serializer, making code readable, navigable and maintainable.

### Additionally

For in-depth documentation and tutorials, refer to [The Django Project](https://www.djangoproject.com/).

## client - Svelte
`Unit`: `http://localhost:8000` -> `https://example.com`

- TODO

## media storage - MinIO
`Unit`: `https://localhost:8000/media` -> `https://example.com/media`

MinIO is an S3 compatible object storage. Use it now for development and production. Upgrade later to a scale-able cloud object storage with minimal reconfiguration if your application ever outgrows it.

## design tool - Storybook
`Unit`: `http://localhost:8000/dev/sb` -> `n/a`
- TODO

## mock smtp - MailDev
`Unit`: `http://localhost:8000/dev/mail` -> `n/a`

### Why maildev?

- Recent releases with high development cadence.
- To swap out for an alternative like MailHog, just switch out docker containers and update the `.env.dev`.

## database - Postgresql
- TODO

# Getting Started
- TODO

# Changelog

1. Initial

# TODO

- Rewrite bash scripts
