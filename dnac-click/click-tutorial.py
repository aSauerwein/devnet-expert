# https://www.assemblyai.com/blog/the-definitive-guide-to-python-click/
import click
import json
from pprint import pprint

"""
@click.group(<name>) creates a command that instantiates a group class
a group is intended to be a set of related commands
@click.argument(<argument name>) tells us that we will be passing an argument
and referring to that argument in the function by the name we pass it
@click.pass_context tells the group command that we're going to be using
the context, the context is not visible to the command unless we pass this
"""


@click.group("cli")
@click.pass_context
@click.argument("document")
def cli(ctx, document):
    """
    An example CLI for interfacing with a document
    """
    with open(document) as f:
        _dict = json.load(f)
        ctx.obj = _dict


@cli.command("check_context_object")
@click.pass_context
def check_context(ctx):
    pprint(type(ctx.obj))


pass_dict = click.make_pass_decorator(dict)


@cli.command("get_keys")
@pass_dict
def get_keys(_dict):
    keys = list(_dict.keys())
    click.secho("The keys in our dictionary are", fg="green")
    click.echo(click.style(str(keys), fg="blue"))


@cli.command("get_key")
@click.argument("key")
@click.pass_context
def get_key(ctx, key):
    pprint(ctx.obj[key])


@cli.command("get_summary")
@click.pass_context
def get_summary(ctx):
    ctx.invoke(get_key, key="summary")


@cli.command("get_results")
@click.option(
    "-d", "--download", is_flag=True, help="Pass to download the result to a json file"
)
@click.option("-k", "--key", help="Pass a key to specify that key from the results")
@click.pass_context
def get_results(ctx, download: bool, key: str):
    results = ctx.obj["results"]
    if key is not None:
        result = {}
        for entry in results:
            if key in result:
                result[key] += entry[key]
            else:
                result[key] = entry[key]
        results = result
    if download:
        if key is not None:
            filename = key + ".json"
        else:
            filename = "results.json"
        with open(filename, "w") as f:
            json.dump(results, f)
        print("File saved to", filename)
    else:
        pprint(results)

@cli.command("get_text")
@click.option("-s", "--sentences", is_flag=True, help="Pass to return sentences")
@click.option("-p", "--paragraphs", is_flag=True, help="Pass to return paragraphs")
@click.option("-d", "--download", is_flag=True, help="Download as a json file")
@click.pass_obj
def get_text(_dict, sentences, paragraphs, download):
    results = _dict["results"]
    text = {}
    for idx, entry in enumerate(results):
        if paragraphs:
            text[idx] = entry["text"]
        else:
            if 'text' in text:
                text['text'] += entry['text']
            else:
               text['text'] = entry['text']
        if sentences:
            sentences = text['text'].split('.')
            for i in range(len(sentences)):
                if sentences[i] != '':
                    text[i] = sentences[i]
            del text['text']
        pprint(text)
        if download:
            if paragraphs:
                filename = "paragraphs.json"
            elif sentences:
                filename = "sentences.json"
            else:
                filename = "text.json"
            with open(filename, 'w') as w:
                w.write(json.dumps(results))
            print("File saved to", filename)

def main():
    cli(prog_name="cli")


if __name__ == "__main__":
    main()
