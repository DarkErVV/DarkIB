from sqlalchemy import Table, Column, Integer, String, MetaData
from migrate import *

meta = MetaData()

account = Table(
        'account', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String(255)),
        Column('email', String(255)),
        Column('pswd_hash', String(40)),
    )


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    meta.bind = migrate_engine
    account.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    meta.bind = migrate_engine
    account.drop()
