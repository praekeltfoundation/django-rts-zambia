# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Schools.school_id'
        db.delete_column(u'hierarchy_schools', 'school_id_id')

        # Adding field 'Schools.zone_id'
        db.add_column(u'hierarchy_schools', 'zone_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='zone_id ', to=orm['hierarchy.Zones']),
                      keep_default=False)


        # Changing field 'Zones.district_id'
        db.alter_column(u'hierarchy_zones', 'district_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Districts']))

    def backwards(self, orm):
        # Adding field 'Schools.school_id'
        db.add_column(u'hierarchy_schools', 'school_id',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='school_id ', to=orm['hierarchy.Schools']),
                      keep_default=False)

        # Deleting field 'Schools.zone_id'
        db.delete_column(u'hierarchy_schools', 'zone_id_id')


        # Changing field 'Zones.district_id'
        db.alter_column(u'hierarchy_zones', 'district_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Zones']))

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
            'zone_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'zone_id '", 'to': u"orm['hierarchy.Zones']"})
        },
        u'hierarchy.zones': {
            'Meta': {'object_name': 'Zones'},
            'district_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_id '", 'to': u"orm['hierarchy.Districts']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['hierarchy']