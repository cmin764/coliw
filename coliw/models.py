import peewee

from coliw import coliw


db = peewee.SqliteDatabase(coliw.config.DATABASE_URI)


class BaseModel(peewee.Model):

    class Meta:
        database = db
