#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/2/19 上午11:56
# software: PyCharm
# project: lingzhi-engine
from rest_framework import serializers

from account.models import User
from vuln.models.hook_strategy import HookStrategy


class SinkSerialize(serializers.ModelSerializer):
    class Meta:
        model = HookStrategy
        fields = ['value']


class HookRuleSerialize(serializers.ModelSerializer):
    USER = dict()
    rule_type = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = HookStrategy
        fields = ['id', 'rule_type', 'value', 'source', 'target', 'inherit', 'track', 'update_time', 'user']

    # fixme 修改策略类型获取方式，解决重复查询的问题
    def get_rule_type(self, obj):
        rule_type = obj.type.first()
        if rule_type:
            return rule_type.name
        else:
            return 'Unknown'

    def get_user(self, obj):
        if obj.created_by not in self.USER:
            temp_user = User.objects.filter(id=obj.created_by).first()
            self.USER[obj.created_by] = temp_user.get_username() if temp_user else ''
        return self.USER[obj.created_by]
