import click
from envparse import env
from application import create_app


@click.command()
@click.option('-h', '--host', help='Bind host', default='localhost', show_default=True)
@click.option('-p', '--port', help='Bind port', default=8000, type=int, show_default=True)
@click.option('-e', '--env', help='Running env, override environment FLASK_ENV.', default='development', show_default=True)
@click.option('-f', '--env-file', help='Environment from file', type=click.Path(exists=True))
def main(**kwargs):
    if kwargs['env_file']:
        env.read_envfile(kwargs['env_file'])
    app = create_app(kwargs['env'])
    app.run(host=kwargs['host'], port=kwargs['port'])


if __name__ == '__main__':
    main()
