# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Schools'
        db.delete_table(u'hierarchy_schools')

        # Deleting model 'Provinces'
        db.delete_table(u'hierarchy_provinces')

        # Deleting model 'Districts'
        db.delete_table(u'hierarchy_districts')

        # Deleting model 'Zones'
        db.delete_table(u'hierarchy_zones')

        # Adding model 'School'
        db.create_table(u'hierarchy_school', (
            ('EMIS', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zone_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='zone_id ', to=orm['hierarchy.Zone'])),
        ))
        db.send_create_signal(u'hierarchy', ['School'])

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
            ('province_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='province_id ', to=orm['hierarchy.Province'])),
        ))
        db.send_create_signal(u'hierarchy', ['District'])

        # Adding model 'Zone'
        db.create_table(u'hierarchy_zone', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('district_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_id ', to=orm['hierarchy.District'])),
        ))
        db.send_create_signal(u'hierarchy', ['Zone'])


    def backwards(self, orm):
        # Adding model 'Schools'
        db.create_table(u'hierarchy_schools', (
            ('EMIS', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zone_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='zone_id ', to=orm['hierarchy.Zones'])),
        ))
        db.send_create_signal(u'hierarchy', ['Schools'])

        # Adding model 'Provinces'
        db.create_table(u'hierarchy_provinces', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hierarchy', ['Provinces'])

        # Adding model 'Districts'
        db.create_table(u'hierarchy_districts', (
            ('province_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='province_id ', to=orm['hierarchy.Provinces'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'hierarchy', ['Districts'])

        # Adding model 'Zones'
        db.create_table(u'hierarchy_zones', (
            ('district_id', self.gf('django.db.models.fields.related.ForeignKey')(related_name='district_id ', to=orm['hierarchy.Districts'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'hierarchy', ['Zones'])

        # Deleting model 'School'
        db.delete_table(u'hierarchy_school')

        # Deleting model 'Province'
        db.delete_table(u'hierarchy_province')

        # Deleting model 'District'
        db.delete_table(u'hierarchy_district')

        # Deleting model 'Zone'
        db.delete_table(u'hierarchy_zone')


    models = {
        u'hierarchy.district': {
            'Meta': {'object_name': 'District'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'province_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'province_id '", 'to': u"orm['hierarchy.Province']"})
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
            'zone_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zone_id '", 'to': u"orm['hierarchy.Zone']"})
        },
        u'hierarchy.zone': {
            'Meta': {'object_name': 'Zone'},
            'district_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_id '", 'to': u"orm['hierarchy.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['hierarchy']