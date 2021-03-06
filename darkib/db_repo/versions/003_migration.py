from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
images = Table('images', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('md5_hash', String(length=40)),
    Column('height', Integer),
    Column('weight', Integer),
    Column('type', Integer),
    Column('date_upload', DateTime),
    Column('user_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['images'].columns['date_upload'].create()
    post_meta.tables['images'].columns['user_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['images'].columns['date_upload'].drop()
    post_meta.tables['images'].columns['user_id'].drop()
