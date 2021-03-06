from django.db import connections, DatabaseError, transaction
from django.conf import settings

from framework.utils.cornflakes.sql import create_sequence_if_not_exists_sql, postgres_shard_id_function_sql


def create_global_sequence(sequence_name, db_alias, reset_sequence=False):
    cursor = connections['default'].cursor()
    sid = transaction.savepoint('default')
    try:
        cursor.execute(create_sequence_if_not_exists_sql % sequence_name)
    except DatabaseError:
        transaction.savepoint_rollback(sid, using=db_alias)
    else:
        transaction.savepoint_commit(sid, using=db_alias)
    if reset_sequence:
        cursor.execute("SELECT setval('%s', 1, false)" % (sequence_name,))
    cursor.close()


def create_shard_id_function(sequence_name, db_alias, shard_id):
    cursor = connections[db_alias].cursor()
    cursor.execute(
        postgres_shard_id_function_sql % {
            'shard_epoch': settings.SHARD_EPOCH,
            'shard_id': shard_id,
            'sequence_name': sequence_name
        }
    )
    cursor.close()
