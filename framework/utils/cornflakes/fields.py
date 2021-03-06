from django.db.models import BigAutoField
from django.conf import settings

from framework.utils.cornflakes.utils import create_global_sequence, create_shard_id_function


class BaseShardIDField(object):

    def __init__(self, *args, **kwargs):

        if not hasattr(settings, 'SHARD_EPOCH'):
            raise ValueError("PostgresShardGeneratedIDField requires a SHARD_EPOCH to be defined in your settings file.")

        return super(BaseShardIDField, self).__init__(*args, **kwargs)

    @staticmethod
    def migration_receiver(*args, **kwargs):
        sequence_name = "global_id_sequence"
        shard_id = 1
        db_alias = 'default'
        create_global_sequence(sequence_name, db_alias, True)
        create_shard_id_function(sequence_name, db_alias, shard_id)


class ShadedIDField(BaseShardIDField, BigAutoField):
    empty_strings_allowed = False
    description = "Big (8 byte) positive integer storing ID of a model"

    def db_type(self, connection, *args, **kwargs):
        try:
            from django.db.backends.postgresql.base import DatabaseWrapper as PostgresDatabaseWrapper
        except ImportError:
            from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as PostgresDatabaseWrapper

        if connection.vendor == PostgresDatabaseWrapper.vendor:
            return "bigint DEFAULT next_sharded_id()"
        else:
            return super(ShadedIDField, self).db_type(connection)
