# Welcome

This is an opinionated project template emphasizing productivity, allowing development for a project to hit the ground running.

# Stack

## server - NGINX Unit

Handles high level routing for the entire application and natively serves static files, and the backend Django ASGI. Proxies the appropriate upstream containers and services to the public.

- TODO

## api - Django 4.0, Python 3.10
`Unit`: `http://localhost:8000/api` -> `https://example.com/api`

Django provides the versatility and utilitarianism available only through Python3.

Django's ORM provides robust models, clear fields and relationships with a distinctly powerful query system that trivializes the capability to reach across multiple table relationships.

For API endpoints, this template emphasises use of [The Django Rest Framework](https://www.django-rest-framework.org/)

Additionally, Django provides a built in administation site for managing users, permissions and other entries for models in your project.

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

$>  python manage.py makemigrations blog
```

``` bash
# Apply all your migrations to the database

$> python manage.py migrate
```

``` python
# Query for all blog entries containing "Spokane" in the title,
# and were authored by an administrator

entries = BlogPost.objects.filter(title__icontains="Spokane", author__is_superuser=True)
```

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
