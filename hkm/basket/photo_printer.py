# -*- coding: utf-8 -*-
import os
from StringIO import StringIO

import paramiko
from django.utils import timezone

from hkm.image_utils import get_cropped_full_res_file
from hkm.finna import DEFAULT_CLIENT as FINNA

# Note DOS line endings
DPOF_TEMPLATE = u"""
[HDR]\r\n
GEN REV = 01.00\r\n
GEN CRT = "OrderConverter 1.33"-01.00\r\n
GEN DTM = {datetime_stamp}\r\n
USR NAM = "{username}"\r\n
USR TEL = ""\r\n
VUQ RGN = BGN\r\n
VUQ VNM = "SEIKO EPSON" -ATR "Print Info"\r\n
PRT PCH = {print_settings_preset}\r\n
VUQ RGN = END\r\n

[JOB]\r\n
PRT PID = {orderline_id}\r\n
PRT TYP = STD\r\n
PRT QTY = {amount}\r\n
IMG FMT = EXIF2 -J\r\n
<IMG SRC = "../IMAGES/{img_source}">\r\n
VUQ RGN = BGN\r\n
VUQ VNM = "SEIKO EPSON" -ATR "Print Info"\r\n
VUQ VER = 01.00\r\n
PRT CVP1 = 1 -STR "10137_MIT_CK_FTP1 - Pasi Paavola"\r\n
PRT CVP2 = 1 -STR "{file_name}"\r\n
VUQ RGN = END\r\n

"""


class PhotoPrinter(object):
    """
    Handles printing of an order: transfers file to a museum printer over sftp, generates DPOF meta file to create
    a job for a printer.
    """

    def __init__(self, username, password, address):
        client = paramiko.SSHClient()
        # a host fingerprint must exist in users known_hosts file.
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
                address,
                username=username,
                password=password,
                look_for_keys=False,
                allow_agent=False,
        )
        # we need username for path
        self.username = username
        self.client = client

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.client:
            self.client.close()
            self.client = None

    def upload(self, file_obj, filename, remote_path):
        base_folder = "/home/%s" % self.username
        with self.client.open_sftp() as connection:
            for folder in remote_path.split("/"):
                if folder == "":
                    continue
                try:
                    connection.chdir(os.path.join(base_folder, folder))
                except IOError:
                    connection.mkdir(os.path.join(base_folder, folder))
                base_folder = os.path.join(base_folder, folder)

            full_remote_path = os.path.join(base_folder, filename)

            connection.putfo(
                file_obj,
                full_remote_path
            )
            return full_remote_path

    def print_order(self, order):
        for line in order.product_orders.all():
            record_data = FINNA.get_record(line.record_finna_id)
            record = record_data["records"][0]
            #get croped img
            photo = get_cropped_full_res_file(record["title"], line)
            printing_preset = self.get_printing_preset(line)
            # Replace scandic letters from image name to prevent problems with sftp upload
            image_name = self.strip_scandic_letters(os.path.basename(photo.edited_image.name))
            job_base_folder = os.path.join(
                ("o%s%s%s" % (printing_preset, ("%s" % line.pk).zfill(6), order.orderer_name)),
            )
            # upload image
            image_upload_path = os.path.join(
                job_base_folder,
                "IMAGES"
            )
            full_remote_path = self.upload(photo.edited_image, image_name, image_upload_path)

            # generate and upload DPOF file
            dpof_upload_path = os.path.join(
                job_base_folder,
                "MISC"
            )
            dpof = self.generate_dpof(line, image_name)
            self.upload(StringIO(dpof), "AUTPRINT.MRK", dpof_upload_path)
            return True

    def get_printing_preset(self, line):
        """
        A configuration for a printing job including all color settings, paper, size.
        Provided and manageable by a customer.
        :param line: Ordered photo
        :return: Int
        """
        printer_presets = line.user.profile.get_printer_presets
        return printer_presets.get(line.product_type.name, 0)

    def generate_dpof(self, line, image_name):
        return DPOF_TEMPLATE.format(
            datetime_stamp=timezone.now(),
            username=line.user,
            print_settings_preset=self.get_printing_preset(line),
            orderline_id=line.pk,
            amount=line.amount,
            img_source=image_name,
            file_name=image_name
        )

    def strip_scandic_letters(self, image_name):
        scandic_letters = [
            (u"Ä", u"A"),
            (u"ä", u"a"),
            (u"Ö", u"O"),
            (u"ö", u"o"),
        ]
        for scandic, char in scandic_letters:
            image_name = image_name.replace(scandic, char)
        return image_name
