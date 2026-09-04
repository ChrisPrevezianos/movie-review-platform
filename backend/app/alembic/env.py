"""Alembic configuration for database migrations and SQLModel metadata detection."""
from logging.config import fileConfig
from sqlmodel import SQLModel
from alembic import context
from sqlalchemy import engine_from_config, pool


config = context.config


assert config.config_file_name is not None
fileConfig(config.config_file_name)


from app.core.config import settings 

# Import all models so Alembic can detect their tables during autogeneration.
from app.models.actor import Actor 
from app.models.director import Director
from app.models.genre import Genre
from app.models.movie import Movie
from app.models.review import Review
from app.models.user import User

target_metadata = SQLModel.metadata


def get_url() -> str:
    """Return the configured database URL for Alembic."""
    return str(settings.DATABASE_URL)

def run_migrations_offline() -> None:
    """Run database migrations in offline mode."""
    url = get_url()
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run database migrations using an active database connection."""
    configuration = config.get_section(config.config_ini_section)
    assert configuration is not None
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata, compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()