# -*- coding: utf-8 -*-

from django.apps import AppConfig


class DefaultConfig(AppConfig):
    name = "hkm"
    verbose_name = "hkm"

    def ready(self):
        import hkm.auditlog_signals  # noqa
