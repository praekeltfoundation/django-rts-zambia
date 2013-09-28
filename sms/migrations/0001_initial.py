# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SendSMS'
        db.create_table(u'sms_sendsms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sms', self.gf('django.db.models.fields.CharField')(max_length=160)),
            ('total_sent', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('replies', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('district', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.District'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sms', ['SendSMS'])

        # Adding model 'SMSZones'
        db.create_table(u'sms_smszones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.Zone'])),
            ('send_sms', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms.SendSMS'])),
            ('num_sent', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'sms', ['SMSZones'])

        # Adding model 'TempSMSZones'
        db.create_table(u'sms_tempsmszones', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('temp_sms', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms.SendSMS'])),
        ))
        db.send_create_signal(u'sms', ['TempSMSZones'])


    def backwards(self, orm):
        # Deleting model 'SendSMS'
        db.delete_table(u'sms_sendsms')

        # Deleting model 'SMSZones'
        db.delete_table(u'sms_smszones')

        # Deleting model 'TempSMSZones'
        db.delete_table(u'sms_tempsmszones')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        u'hierarchy.zone': {
            'Meta': {'object_name': 'Zone'},
            'district': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'district_id'", 'to': u"orm['hierarchy.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sms.sendsms': {
            'Meta': {'object_name': 'SendSMS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.District']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'replies': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sms': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'total_sent': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'sms.smszones': {
            'Meta': {'object_name': 'SMSZones'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_sent': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'send_sms': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms.SendSMS']"}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.Zone']"})
        },
        u'sms.tempsmszones': {
            'Meta': {'object_name': 'TempSMSZones'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temp_sms': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sms.SendSMS']"})
        }
    }

    complete_apps = ['sms']