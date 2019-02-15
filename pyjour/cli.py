# -*- coding: utf-8 -*-

"""Console script for pyjour."""
import logging
import sys

import click

from pyjour.pyjour import add_journal_entry


logging.basicConfig(
    level=logging.DEBUG,
    format='[%(name)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
)


@click.group()
def main():
    pass


@main.command()
@click.argument('gist', nargs=-1)
def add(gist: str):
    add_journal_entry(gist)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
