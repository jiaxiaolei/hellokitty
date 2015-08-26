# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rootport'
        db.create_table(u'torrentkitty_rootport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'torrentkitty', ['Rootport'])

        # Adding model 'Resources'
        db.create_table(u'torrentkitty_resources', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'torrentkitty', ['Resources'])


    def backwards(self, orm):
        # Deleting model 'Rootport'
        db.delete_table(u'torrentkitty_rootport')

        # Deleting model 'Resources'
        db.delete_table(u'torrentkitty_resources')


    models = {
        u'torrentkitty.resources': {
            'Meta': {'object_name': 'Resources'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        u'torrentkitty.rootport': {
            'Meta': {'object_name': 'Rootport'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['torrentkitty']