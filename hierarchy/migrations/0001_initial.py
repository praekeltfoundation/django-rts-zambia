# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Provinces'
        db.create_table(u'hierarchy_provinces', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hierarchy', ['Provinces'])

        # Adding model 'Districts'
        db.create_table(u'hierarchy_districts', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('province_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='province_id ', to=orm['hierarchy.Provinces'])),
        ))
        db.send_create_signal(u'hierarchy', ['Districts'])

        # Adding model 'Zones'
        db.create_table(u'hierarchy_zones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('district_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_id ', to=orm['hierarchy.Zones'])),
        ))
        db.send_create_signal(u'hierarchy', ['Zones'])

        # Adding model 'Schools'
        db.create_table(u'hierarchy_schools', (
            ('EMIS', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('school_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='school_id ', to=orm['hierarchy.Schools'])),
        ))
        db.send_create_signal(u'hierarchy', ['Schools'])


    def backwards(self, orm):
        # Deleting model 'Provinces'
        db.delete_table(u'hierarchy_provinces')

        # Deleting model 'Districts'
        db.delete_table(u'hierarchy_districts')

        # Deleting model 'Zones'
        db.delete_table(u'hierarchy_zones')

        # Deleting model 'Schools'
        db.delete_table(u'hierarchy_schools')


    models = {
        u'hierarchy.districts': {
            'Meta': {'object_name': 'Districts'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'province_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'province_id '", 'to': u"orm['hierarchy.Provinces']"})
        },
        u'hierarchy.provinces': {
            'Meta': {'object_name': 'Provinces'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'hierarchy.schools': {
            'EMIS': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'Meta': {'object_name': 'Schools'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'school_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'school_id '", 'to': u"orm['hierarchy.Schools']"})
        },
        u'hierarchy.zones': {
            'Meta': {'object_name': 'Zones'},
            'district_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_id '", 'to': u"orm['hierarchy.Zones']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['hierarchy']