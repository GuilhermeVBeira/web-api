import asyncio

import click

from web_app.apps.users.models import User
from web_app.apps.users.schemas import pwd_context
from web_app.config import settings
from web_app.main import db


@click.group()
def cli():
    pass


async def create_user(username, email, password):
    await db.set_bind(settings.DATABASE_URL)
    await User.create(username=username, email=email, is_active=True, password=password)


@click.option('--password', prompt=True, hide_input=True,
              confirmation_prompt=True)
@click.option('--email', prompt=True)
@click.option('--username', prompt=True)
@click.command()
def createuser(username, email, password):
    password = pwd_context.hash(password)
    asyncio.run(create_user(username, email, password))
    click.echo(f'User {username} created')


cli.add_command(createuser)

if __name__ == '__main__':
    cli()

