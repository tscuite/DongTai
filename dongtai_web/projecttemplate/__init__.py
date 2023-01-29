from dongtai_common.models.project import (IastProject, IastProjectTemplate)
from rest_framework import serializers
from dongtai_common.endpoint import UserEndPoint, R, TalentAdminEndPoint
from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from dongtai_web.utils import extend_schema_with_envcheck, get_response_serializer

class PaginationSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(default=20,
                                         help_text=_('Number per page'))
    page = serializers.IntegerField(default=1, help_text=_('Page index'))

class ProjectTemplateCreateArgsSerializer(serializers.Serializer):
    template_name = serializers.CharField(help_text=_('The name of project'))
    scan_id = serializers.IntegerField(
        help_text=_("The id corresponding to the scanning strategy."))
    vul_validation = serializers.IntegerField(
        help_text="vul validation switch")
    data_gather = serializers.JSONField(help_text="data gather settings",
                                       required=False)
    data_gather_is_followglobal = serializers.IntegerField()
    blacklist_is_followglobal = serializers.IntegerField()
    blacklist = serializers.SerializerMethodField()

    def get_blacklist(self, obj):
        return []
    
    class Meta:
        model = IastProjectTemplate

def template_create(data, user):
    data['user_id'] = user.id
    IastProjectTemplate.objects.create(**data)


def template_update(pk, data, user):
    data['user_id'] = user.id
    IastProjectTemplate.objects.filter(pk=pk).update(**data)


class IastProjectTemplateView(TalentAdminEndPoint, viewsets.ViewSet):
    name = "api-v1-agent-project-template"
    description = _("project_template")

    @extend_schema_with_envcheck(request=ProjectTemplateCreateArgsSerializer,
                                 summary=_('Create project template'),
                                 description=_("Create project template"),
                                 tags=[_('projectemplate')])
    def create(self, request):
        ser = ProjectTemplateCreateArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        template_create(ser.data, request.user)
        return R.success()

    @extend_schema_with_envcheck(request=ProjectTemplateCreateArgsSerializer,
                                 summary=_('Update project template'),
                                 description=_("Update project template"),
                                 tags=[_('projectemplate')])
    def update(self, request, pk):
        ser = ProjectTemplateCreateArgsSerializer(data=request.data)
        try:
            if ser.is_valid(True):
                pass
        except ValidationError as e:
            return R.failure(data=e.detail)
        template_update(pk, ser.data, request.user)
        return R.success()

    @extend_schema_with_envcheck([PaginationSerializer],
                                 summary=_('List project template'),
                                 description=_("List project template"),
                                 tags=[_('projectemplate')])
    def list(self, request):
        ser = PaginationSerializer(data=request.GET)
        try:
            if ser.is_valid(True):
                page_size = ser.validated_data['page_size']
                page = ser.validated_data['page']
        except ValidationError as e:
            return R.failure(data=e.detail)
        summary, templates = self.get_paginator(
            IastProjectTemplate.objects.values().order_by('-latest_time').all(), page, page_size)
        return R.success(data={
            "templates": list(templates),
            "summary": summary
        })

    @extend_schema_with_envcheck(summary=_('delete project template'),
                                 description=_("delete project template"),
                                 tags=[_('projectemplate')])
    def delete(self, request, pk):
        IastProjectTemplate.objects.filter(pk=pk).delete()
        return R.success()

    @extend_schema_with_envcheck(summary=_('get project template'),
                                 description=_("get project template"),
                                 tags=[_('projectemplate')])
    def retrieve(self, request, pk):
        obj = IastProjectTemplate.objects.filter(pk=pk).first()
        if not obj:
            return R.failure()
        return R.success(data=ProjectTemplateCreateArgsSerializer(obj).data)
