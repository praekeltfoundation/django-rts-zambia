# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Province'
        db.create_table(u'hierarchy_province', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hierarchy', ['Province'])

        # Adding model 'District'
        db.create_table(u'hierarchy_district', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Province'])),
        ))
        db.send_create_signal(u'hierarchy', ['District'])

        # Adding model 'Zone'
        db.create_table(u'hierarchy_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.District'])),
        ))
        db.send_create_signal(u'hierarchy', ['Zone'])

        # Adding model 'School'
        db.create_table(u'hierarchy_school', (
            ('EMIS', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Zone'])),
        ))
        db.send_create_signal(u'hierarchy', ['School'])


    def backwards(self, orm):
        # Deleting model 'Province'
        db.delete_table(u'hierarchy_province')

        # Deleting model 'District'
        db.delete_table(u'hierarchy_district')

        # Deleting model 'Zone'
        db.delete_table(u'hierarchy_zone')

        # Deleting model 'School'
        db.delete_table(u'hierarchy_school')


    models = {
        u'hierarchy.district': {
            'Meta': {'object_name': 'District'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.Province']"})
        },
        u'hierarchy.province': {
            'Meta': {'object_name': 'Province'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hierarchy.school': {
            'EMIS': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'School'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.Zone']"})
        },
        u'hierarchy.zone': {
            'Meta': {'object_name': 'Zone'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['hierarchy']