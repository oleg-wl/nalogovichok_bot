#!/bin/bash python
# -*- coding: UTF-8 -*-

import os
import logging
import click

from source.main import main
from dotenv import load_dotenv

@click.command()
@click.option('-d/-p', default=False, help='Set logger and api key to dev')
def app(d):
    """Run this bot"""    
    load_dotenv('config.env')

    if d: 
        token = os.environ['BOT_API_DEV']
        level = logging.DEBUG
        click.echo('Run in debug mode')
    else: 
        token = os.environ['BOT_API']
        level = logging.WARNING
    logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
)
    logging.getLogger("httpx").setLevel(level=logging.ERROR)
    logging.getLogger("httpcore").setLevel(level=logging.ERROR)

    main(token=token)

if __name__ == "__main__":
    app()