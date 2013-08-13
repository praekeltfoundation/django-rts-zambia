# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SchoolData.emis_id'
        db.delete_column(u'data_schooldata', 'emis_id_id')

        # Adding field 'SchoolData.emis'
        db.add_column(u'data_schooldata', 'emis',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hierarchy.School']),
                      keep_default=False)

        # Adding field 'SchoolData.name'
        db.add_column(u'data_schooldata', 'name',
                      self.gf('django.db.models.fields.CharField')(default='name', max_length=100),
                      keep_default=False)


        # Changing field 'SchoolData.created_at'
        db.alter_column(u'data_schooldata', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Deleting field 'HeadTeacher.emis_id'
        db.delete_column(u'data_headteacher', 'emis_id_id')

        # Adding field 'HeadTeacher.zonal_head_name'
        db.add_column(u'data_headteacher', 'zonal_head_name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 8, 12, 0, 0), max_length=100),
                      keep_default=False)

        # Adding field 'HeadTeacher.emis'
        db.add_column(u'data_headteacher', 'emis',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.School'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'HeadTeacher.created_at'
        db.alter_column(u'data_headteacher', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):
        # Adding field 'SchoolData.emis_id'
        db.add_column(u'data_schooldata', 'emis_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hierarchy.School']),
                      keep_default=False)

        # Deleting field 'SchoolData.emis'
        db.delete_column(u'data_schooldata', 'emis_id')

        # Deleting field 'SchoolData.name'
        db.delete_column(u'data_schooldata', 'name')


        # Changing field 'SchoolData.created_at'
        db.alter_column(u'data_schooldata', 'created_at', self.gf('django.db.models.fields.DateField')())
        # Adding field 'HeadTeacher.emis_id'
        db.add_column(u'data_headteacher', 'emis_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.School'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'HeadTeacher.zonal_head_name'
        db.delete_column(u'data_headteacher', 'zonal_head_name')

        # Deleting field 'HeadTeacher.emis'
        db.delete_column(u'data_headteacher', 'emis_id')


        # Changing field 'HeadTeacher.created_at'
        db.alter_column(u'data_headteacher', 'created_at', self.gf('django.db.models.fields.DateField')())

    models = {
        u'data.headteacher': {
            'Meta': {'object_name': 'HeadTeacher'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_zonal_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'zonal_head_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.schooldata': {
            'Meta': {'object_name': 'SchoolData'},
            'boys_g2': ('django.db.models.fields.IntegerField', [], {}),
            'classrooms': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'girls_g2': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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