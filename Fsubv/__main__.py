import uvloop
from Fsubv import Bot
from .database.db import create_table

uvloop.install()
create_table()
Bot().run()