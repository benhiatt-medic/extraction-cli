#!/usr/local/bin/python3

import click
import importlib.util
from os import getcwd, mkdir, walk
from os.path import exists
import json

__author__ = 'Ben Hiatt'


def extract_values(variables, text):
    measurements = {}
    for line in text.split('\n'):
        for variable in variables:
            if line.startswith(variable):
                prefix = len(variable)
                pos = line.find('=')
                measurement = line[prefix: pos]
                if measurement.isdigit():
                    #measurement = int(measurement)  # json changes them to strings anyway
                    if measurement not in measurements:
                        measurements[measurement] = {}
                    measurements[measurement][variable] = variables[variable](line[pos + 1:])
    return measurements


def parse_files(variables, files, dir_in, dir_out):
    if not exists(dir_out):
        click.echo('creating ' + dir_out + '...')
        mkdir(dir_out)
    for file in files:
        with open(dir_in + '/' + file, 'r') as x:
            try:
                text = x.read()
                with open(dir_out + '/' + file.split('.')[0] + ' (' + ', '.join(variables) + ').json', 'w') as y:
                    json.dump(extract_values(variables, text), y)
                    click.echo('extracted ' + x.name + ' to ' + y.name)
            except UnicodeDecodeError:
                click.echo('skipping ' + x.name + '...')


@click.command()
@click.option('--dir-in',
              type=click.Path(exists=True, file_okay=False),
              default=getcwd(),
              help='Defaults to the current working directory')
@click.option('--dir-out',
              type=click.Path(file_okay=False, writable=True),
              default=getcwd() + '/extracted',
              help='Defaults to the directory "extracted" in the current working directory (creates if nonexistent)')
@click.argument('var-file',
                type=click.Path(exists=True, dir_okay=False))
def get_vars(dir_in, dir_out, var_file):
    """VAR-FILE refers to a Python file where "variables" is set to a dict of Strings mapped to function objects.

    Example:

        def identity(x):

            return x

        variables = {

            "variable1": identity,

            "variable2": lambda x: int(x) + 1,

        }
    """
    spec = importlib.util.spec_from_file_location('variables', var_file)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    for (path, dirs, files) in walk(dir_in):
        parse_files(foo.variables, [file for file in files if file[0] != '.'], dir_in, dir_out)
        break


if __name__ == '__main__':
    get_vars()
