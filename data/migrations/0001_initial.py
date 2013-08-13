# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HeadTeacher'
        db.create_table(u'data_headteacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('msisdn', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')()),
            ('is_zonal_head', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('emis_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.School'], null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'data', ['HeadTeacher'])

        # Adding model 'SchoolData'
        db.create_table(u'data_schooldata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('emis_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.School'])),
            ('classrooms', self.gf('django.db.models.fields.IntegerField')()),
            ('teachers', self.gf('django.db.models.fields.IntegerField')()),
            ('teachers_g1', self.gf('django.db.models.fields.IntegerField')()),
            ('teachers_g2', self.gf('django.db.models.fields.IntegerField')()),
            ('boys_g2', self.gf('django.db.models.fields.IntegerField')()),
            ('girls_g2', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateField')()),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.HeadTeacher'])),
        ))
        db.send_create_signal(u'data', ['SchoolData'])


    def backwards(self, orm):
        # Deleting model 'HeadTeacher'
        db.delete_table(u'data_headteacher')

        # Deleting model 'SchoolData'
        db.delete_table(u'data_schooldata')


    models = {
        u'data.headteacher': {
            'Meta': {'object_name': 'HeadTeacher'},
            'created_at': ('django.db.models.fields.DateField', [], {}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'emis_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_zonal_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'data.schooldata': {
            'Meta': {'object_name': 'SchoolData'},
            'boys_g2': ('django.db.models.fields.IntegerField', [], {}),
            'classrooms': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            'emis_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'girls_g2': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teachers': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g1': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g2': ('django.db.models.fields.IntegerField', [], {})
        },
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
            'EMIS': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'Meta': {'object_name': 'School'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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

    complete_apps = ['data']