#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/1/13 下午7:14
# software: PyCharm
# project: lingzhi-agent-server
from django.db import models
from django.utils.translation import gettext_lazy as _

from vuln.models.hook_type import HookType


class PermissionsMixin(models.Model):
    type = models.ManyToManyField(
        HookType,
        verbose_name=_('type'),
        blank=True,
        help_text=_(
            'The department this user belongs to. A user will get all permissions '
            'granted to each of their department.'
        ),
        related_name="strategies",
        related_query_name="strategy",
    )

    class Meta:
        abstract = True


class HookStrategy(PermissionsMixin):
    value = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    target = models.CharField(max_length=255, blank=True, null=True)
    inherit = models.CharField(max_length=255, blank=True, null=True)
    track = models.CharField(max_length=5, blank=True, null=True)
    create_time = models.IntegerField(blank=True, null=True)
    update_time = models.IntegerField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True, )
    enable = models.IntegerField(max_length=1, blank=True, null=False, default=1)

    class Meta:
        managed = False
        db_table = 'iast_hook_strategy'
