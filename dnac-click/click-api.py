import click
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self):
        url = f"{self.base_url}/get"
        response = requests.get(url)
        return response.text

    def post_data(self, data):
        url = f"{self.base_url}/post"
        response = requests.post(url, json=data)
        return response.text


@click.group()
@click.option("--base-url", default="https://postman-echo.com", help="Base URL of the REST API")
@click.pass_context
def cli(ctx, base_url):
    # set APIClient as object to be passed to other functions
    ctx.obj = APIClient(base_url)

@cli.command()
@click.pass_obj
def get_data(api_client):
    "execute GET request to base-url"
    data = api_client.get_data()
    click.echo(data)

@cli.command()
@click.argument("data")
@click.pass_obj
def post_data(api_client, data):
    "execute POST request to base-url with DATA as json"
    data = {"data": data}
    response = api_client.post_data(data)
    click.echo(response)

cli()