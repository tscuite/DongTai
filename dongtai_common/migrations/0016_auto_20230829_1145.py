# Generated by Django 3.2.20 on 2023-08-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dongtai_common", "0015_vul_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="bottom_stack",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="full_stack",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="language",
            field=models.CharField(blank=True, default="", max_length=10),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="param_name",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="pattern_uri",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="taint_position",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="taint_value",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AlterField(
            model_name="iastvulnerabilitymodel",
            name="top_stack",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
        migrations.AddIndex(
            model_name="iastvulnerabilitymodel",
            index=models.Index(
                fields=["http_method", "param_name", "pattern_uri", "project_id", "status_id", "strategy_id"],
                name="iast_vulner_http_me_f84d4f_idx",
            ),
        ),
    ]
