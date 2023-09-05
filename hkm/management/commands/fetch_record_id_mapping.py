import json
import os
import xml.dom.minidom

import requests
from django.core.management.base import BaseCommand

OAIHANDLER_URL = "https://museoliittorepox.vserver.fi/repox/OAIHandler"
INIT_CALL_PARAMS = "?verb=ListRecords&set=finna_hkm_tuotanto&metadataPrefix=lido"
FOLLOW_UP_CALL_PARAMS = "?verb=ListRecords&resumptionToken="

DEFAULT_OUTPUT_FILE = "./hkm/migrations/data/id_map.json"

NEW_ID_PREFIX = "hkm."
OLD_ID_PREFIX = "hkm.HKMS000005:"


class Command(BaseCommand):
    help = """Reads old and new values of the record id from the OAIHandler
            250 records at a time and writes a json result to defined output file."""

    def add_arguments(self, parser):
        parser.add_argument(
            "-o",
            "--output",
            help="Output file for the record id mapping as a JSON formatted dictionary.",
            default=DEFAULT_OUTPUT_FILE,
        )

    def handle(self, *args, **options):
        output_file = options["output"]

        output_path = os.path.dirname(output_file)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            self.stdout.write(f"Created output path: {output_path}")

        id_map = {}  # mapping between old and new IDs

        # first request
        response = requests.get(OAIHANDLER_URL + INIT_CALL_PARAMS)
        content = response.text
        token = self.xml_records_to_dict(content, id_map)

        # loop for following calls until no next call token is received
        while token:
            self.stdout.write(f"Processed {len(id_map)} ID mappings ({token}).")
            response = requests.get(OAIHANDLER_URL + FOLLOW_UP_CALL_PARAMS + token)
            content = response.text

            token = self.xml_records_to_dict(content, id_map)

        with open(output_file, "w") as fp1:
            json.dump(id_map, fp1)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Resulting {len(id_map)} ID mappings written to: {output_file}"
            )
        )

    # Read record entities from an xml input and populate
    # each record id to either dictionary mapping old to a new id.
    # Return parsed resumptionToken for next call if defined. Otherwise None.
    def xml_records_to_dict(self, xml_content, id_map):

        doc = xml.dom.minidom.parseString(xml_content)
        records = doc.getElementsByTagName("record")
        self.stdout.write(f"Total count of records in response: {records.length}.")

        # read resumptionToken if found
        token = None
        token_el_list = doc.getElementsByTagName("resumptionToken")
        if token_el_list.length > 0:
            if token_el_list.item(0).hasChildNodes():
                token = token_el_list.item(0).firstChild.nodeValue

        # loop through all records
        for record in records:
            id_el_list = record.getElementsByTagName("lido:lidoRecID")
            id = id_el_list.item(0).firstChild.nodeValue

            old_id_el_list = record.getElementsByTagName("lido:recordInfoID")
            if old_id_el_list.item(0).hasChildNodes():
                old_id = old_id_el_list.item(0).firstChild.nodeValue
                id_map[OLD_ID_PREFIX + old_id] = NEW_ID_PREFIX + id

        return token
