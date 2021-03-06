from django.db.models import signals
from django.apps import apps

from framework.utils.cornflakes.fields import BaseShardIDField


PRE_MIGRATION_DISPATCH_UID = "PRE_MIGRATE_FOR_MODEL_%s"


def model_config():
    def configure(cls):
        postgres_shard_id_fields = list(
            filter(lambda field: issubclass(type(field), BaseShardIDField), cls._meta.fields)
        )
        if postgres_shard_id_fields:
            for field in postgres_shard_id_fields:
                signals.pre_migrate.connect(
                    field.migration_receiver,
                    sender=apps.get_app_config(cls._meta.app_label),
                    dispatch_uid=PRE_MIGRATION_DISPATCH_UID % cls._meta.app_label
                )

        return cls
    return configure
