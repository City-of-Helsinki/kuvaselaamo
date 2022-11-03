import json
import logging

from django.db import migrations

# make sure a id mapping file exists or is created with the
# management command fetch_recrod_id_mappings
INPUT_FILE = "./hkm/migrations/data/id_map.json"

logger = logging.getLogger(__name__)


def update_record_ids(apps, schema_editor, reverse=False):
    logger.info(f"Loading id map from file '{INPUT_FILE}'.")
    id_map = json.load(open(INPUT_FILE))
    logger.info(f"Id map loaded. Found {len(id_map)} mappings.")

    if reverse:
        id_map = {v: k for k, v in id_map.items()}
        logger.info(f"Id map reversed.")

    # Records
    Record = apps.get_model("hkm", "Record")

    map_count = 0
    item_count = 0

    logger.info("Start updating Records.")
    for record in Record.objects.all():
        item_count += 1
        if replace_record_id(record, id_map):
            map_count += 1

    logger.info(f"{map_count} Records updated. Total Record count is {item_count}.'")

    # Feedbacks
    Feedback = apps.get_model("hkm", "Feedback")

    map_count = 0
    item_count = 0

    logger.info("Start updating Feedbacks.")
    for feedback in Feedback.objects.all():
        item_count += 1
        if replace_record_id(feedback, id_map):
            map_count += 1

    logger.info(
        f"{map_count} Feedbacks updated. Total Feedback count is {item_count}.'"
    )

    # TmpImages
    TmpImage = apps.get_model("hkm", "TmpImage")

    map_count = 0
    item_count = 0

    logger.info("Start updating TmpImages.")
    for tmp in TmpImage.objects.all():
        item_count += 1
        if replace_record_id(tmp, id_map):
            map_count += 1

    logger.info(
        f"{map_count} TmpImages updated. Total TmpImage count is {item_count}.'"
    )


def reverse_update_record_ids(apps, schema_editor):
    update_record_ids(apps, schema_editor, True)


def replace_record_id(item, id_map):
    id_replacement = id_map.get(item.record_id)
    if id_replacement:
        logger.info(f"Replacing id '{item.record_id}' -> '{id_replacement}'.")
        item.record_id = id_replacement
        item.save(update_fields=["record_id"])
        return True
    else:
        logger.info(f"No id replacement for '{item.record_id}'.")
        return False


class Migration(migrations.Migration):

    dependencies = [
        ("hkm", "0046_alter_showcase_after_django_upgrades"),
    ]

    operations = [
        migrations.RunPython(update_record_ids, reverse_update_record_ids, atomic=False)
    ]
