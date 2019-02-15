#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import logging
import os
import pathlib
import subprocess
import tempfile
from typing import NoReturn

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import preserve_literal

logger = logging.getLogger(__name__)

yaml = YAML()

EDITOR = os.environ.get('EDITOR', 'vim')
JOURNAL_HOME = os.path.join(os.environ.get('HOME'), 'pyjour')

message_template = b""  # if you want to set up the file somehow


class JournalDay:
    def __init__(self, root: str, create_at: datetime.datetime):
        self._root = pathlib.Path(root)
        self._create_at = create_at

        self._root.mkdir(parents=True, exist_ok=True)

    def filename(self):
        return os.path.join(str(self._root),
                            str(self._create_at.year),
                            f'{self._create_at.month:02}',
                            f'{self._create_at.day:02}.yml')

    def content(self):
        try:
            with open(self.filename(), 'r') as fh:
                return yaml.load(fh)

        except IOError:
            return self._empty_entry()

    def write(self, gist, message):
        content = self.content()
        self._update_content(content, gist, message)

        filename = self.filename()

        pathlib.Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)

        with open(filename, 'w') as fh:
            yaml.dump(content, stream=fh)

    def _update_content(self, content: dict, gist: str, message: str):
        entry = {
            'gist': gist,
            'notes': preserve_literal(message.strip()),
            'time': self._create_at.strftime('%H:%M:%S +0000'),
        }

        content['entries'].append(entry)

    def _empty_entry(self):
        return {
            'date': f'{self._create_at.strftime("%Y-%m-%d")}',
            'entries': [],
        }


def add_journal_entry(gist: str) -> NoReturn:
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tfh:
        # tfh.write(message_template)
        # tfh.flush()

        try:
            subprocess.run([EDITOR, tfh.name], check=True)

            with open(tfh.name, 'r') as fh:
                message = fh.read()

                j = JournalDay(JOURNAL_HOME, datetime.datetime.utcnow())
                j.write(' '.join(gist), message)

        except subprocess.CalledProcessError as e:
            logger.error(repr(e))
