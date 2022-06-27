# Generated by Django 4.0.5 on 2022-06-27 08:49

import app.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abouttranslation',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='abouttranslation',
            name='cv',
        ),
        migrations.AddField(
            model_name='about',
            name='avatar',
            field=app.fields.WEBPField(default=0, upload_to='avatars/', verbose_name='Avatar'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='about',
            name='cv',
            field=models.FileField(default=0, upload_to='cv/', verbose_name='Curriculum Vitae'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='facebook_url',
            field=models.URLField(verbose_name='Facebook URL'),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='github_url',
            field=models.URLField(verbose_name='Github URL'),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='instagram_url',
            field=models.URLField(verbose_name='Instagram URL'),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='website_url',
            field=models.URLField(verbose_name='Website URL'),
        ),
    ]
