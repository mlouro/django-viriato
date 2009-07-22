# -*- coding: utf-8 -*-
import os
from settings import ROOT_DIR


DEBUG = True
LOCAL_DEV = True

DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#DATABASE_NAME = os.path.join("dev.db")  # Or path to database file if using sqlite3.
DATABASE_NAME = 'intranet'
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = 'lolada'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

INTERNAL_IPS = ('127.0.0.1',)
