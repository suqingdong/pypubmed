import click


@click.group()
@click.option('-d', '--debug', help='logging in debug mode', default=False, is_flag=True)
def cli(debug):
    click.echo(click.style(f'loggin in debug mode[{debug}]', fg='bright_green'))
    click.secho(f'loggin in debug mode[{debug}]', fg='bright_green')


@click.command()
@click.option('-n', '--name', help='the name of input')
@click.option('-k', '--api-key', help='the api_key of Pubmed', envvar='NCBI_API_KEY')
@click.argument('term', nargs=-1)
def search(**kwargs):
    print(kwargs)


cli.add_command(search, name='S')
# first.add_command(third)

if __name__ == '__main__':
    cli()
    
