# -*- coding: utf-8 -*-
import os
from StringIO import StringIO

import paramiko
from django.utils import timezone

from hkm.image_utils import get_cropped_full_res_file
from hkm.finna import DEFAULT_CLIENT as FINNA


DPOF_TEMPLATE = u"""
[HDR]
GEN REV = 01.00
GEN CRT = "OrderConverter 1.33"-01.00
GEN DTM = {datetime_stamp}
USR NAM = "{username}"
USR TEL = ""
VUQ RGN = BGN
VUQ VNM = "SEIKO EPSON" -ATR "Print Info"
PRT PCH = {print_settings_preset}
VUQ RGN = END

[JOB]
PRT PID = {orderline_id}
PRT TYP = STD
PRT QTY = {amount}
IMG FMT = EXIF2 -J
<IMG SRC = "{img_source}">
VUQ RGN = BGN
VUQ VNM = "SEIKO EPSON" -ATR "Print Info"
VUQ VER = 01.00
PRT CVP1 = 1 -STR "10137_MIT_CK_FTP1 - Pasi Paavola"
PRT CVP2 = 1 -STR "{file_name}"
VUQ RGN = END

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
        self.client = client

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.client:
            self.client.close()
            self.client = None

    def upload(self, file_obj, filename, remote_path):
        base_folder = "/"
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
            line.record = record
            line.save()
            #get croped img
            photo = get_cropped_full_res_file(record["title"], line)
            printing_preset = self.get_printing_preset(line)
            job_base_folder = os.path.join(
                ("e%s%s" % (printing_preset, ("%s" % line.pk).zfill(6))),
            )
            # upload image
            image_upload_path = os.path.join(
                job_base_folder,
                "IMAGES"
            )
            full_remote_path = self.upload(photo.edited_image, os.path.basename(photo.edited_image.name), image_upload_path)

            # generate and upload DPOF file
            dpof_upload_path = os.path.join(
                job_base_folder,
                "MISC"
            )
            dpof = self.generate_dpof(photo, line, full_remote_path)
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
        return printer_presets["line.product_type.name"]

    def generate_dpof(self, photo, line, image_upload_path):
        return DPOF_TEMPLATE.format(
            datetime_stamp=timezone.now(),
            username=line.user,
            print_settings_preset=self.get_printing_preset(line),
            orderline_id=line.pk,
            amount=line.amount,
            img_source=image_upload_path,
            file_name=os.path.basename(photo.edited_image.name)
        )
