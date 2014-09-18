# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchoolMonitoringData'
        db.create_table(u'data_schoolmonitoringdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school_improvement_plan', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('no_improvement_plan', self.gf('django.db.models.fields.CharField')(max_length=29, null=True, blank=True)),
            ('teaching', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('learner_assessment', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('learning_materials', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('learner_attendance', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('instructional_time', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('struggling_learners', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('support_ovcs', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('classroom_observation_ht', self.gf('django.db.models.fields.CharField')(max_length=18, null=True, blank=True)),
            ('learner_performance_ht', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('summary_worksheet', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('emis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hierarchy.School'])),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.HeadTeacher'], null=True, blank=True)),
            ('created_by_da', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.DistrictAdminUser'], null=True, blank=True)),
        ))
        db.send_create_signal(u'data', ['SchoolMonitoringData'])


    def backwards(self, orm):
        # Deleting model 'SchoolMonitoringData'
        db.delete_table(u'data_schoolmonitoringdata')


    models = {
        u'data.academicachievementcode': {
            'Meta': {'object_name': 'AcademicAchievementCode'},
            'achievement': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'data.districtadminuser': {
            'Meta': {'object_name': 'DistrictAdminUser'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.District']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_number': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
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
        u'data.headteacherduplicatestore': {
            'Meta': {'object_name': 'HeadTeacherDuplicateStore'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']", 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_zonal_head': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'msisdn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'origin_id': ('django.db.models.fields.IntegerField', [], {}),
            'zonal_head_name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'data.inboundsms': {
            'Meta': {'object_name': 'InboundSMS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'data.learnerperformancedata': {
            'Meta': {'object_name': 'LearnerPerformanceData'},
            'below_minimum_results': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']", 'null': 'True', 'blank': 'True'}),
            'created_by_da': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.DistrictAdminUser']", 'null': 'True', 'blank': 'True'}),
            'desirable_results': ('django.db.models.fields.IntegerField', [], {}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minimum_results': ('django.db.models.fields.IntegerField', [], {}),
            'outstanding_results': ('django.db.models.fields.IntegerField', [], {}),
            'phonetic_awareness': ('django.db.models.fields.IntegerField', [], {}),
            'reading_comprehension': ('django.db.models.fields.IntegerField', [], {}),
            'total_number_pupils': ('django.db.models.fields.IntegerField', [], {}),
            'vocabulary': ('django.db.models.fields.IntegerField', [], {}),
            'writing_diction': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data.schooldata': {
            'Meta': {'object_name': 'SchoolData'},
            'boys': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'boys_g2': ('django.db.models.fields.IntegerField', [], {}),
            'classrooms': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'girls': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'girls_g2': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'teachers': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g1': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g2': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data.schooldataduplicatestore': {
            'Meta': {'object_name': 'SchoolDataDuplicateStore'},
            'boys_g2': ('django.db.models.fields.IntegerField', [], {}),
            'classrooms': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacherDuplicateStore']"}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'girls_g2': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'origin_id': ('django.db.models.fields.IntegerField', [], {}),
            'teachers': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g1': ('django.db.models.fields.IntegerField', [], {}),
            'teachers_g2': ('django.db.models.fields.IntegerField', [], {})
        },
        u'data.schoolmonitoringdata': {
            'Meta': {'object_name': 'SchoolMonitoringData'},
            'classroom_observation_ht': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']", 'null': 'True', 'blank': 'True'}),
            'created_by_da': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.DistrictAdminUser']", 'null': 'True', 'blank': 'True'}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructional_time': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'learner_assessment': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'learner_attendance': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'learner_performance_ht': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'learning_materials': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'no_improvement_plan': ('django.db.models.fields.CharField', [], {'max_length': '29', 'null': 'True', 'blank': 'True'}),
            'school_improvement_plan': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'struggling_learners': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'summary_worksheet': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'support_ovcs': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'}),
            'teaching': ('django.db.models.fields.CharField', [], {'max_length': '18', 'null': 'True', 'blank': 'True'})
        },
        u'data.teacherperformancedata': {
            'Meta': {'object_name': 'TeacherPerformanceData'},
            'academic_level': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.AcademicAchievementCode']"}),
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'attitudes_and_beliefs': ('django.db.models.fields.IntegerField', [], {}),
            'classroom_environment_score': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']", 'null': 'True', 'blank': 'True'}),
            'created_by_da': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.DistrictAdminUser']", 'null': 'True', 'blank': 'True'}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'g2_pupils_present': ('django.db.models.fields.IntegerField', [], {}),
            'g2_pupils_registered': ('django.db.models.fields.IntegerField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pupil_engagement_score': ('django.db.models.fields.IntegerField', [], {}),
            'pupils_books_number': ('django.db.models.fields.IntegerField', [], {}),
            'pupils_materials_score': ('django.db.models.fields.IntegerField', [], {}),
            'reading_assessment': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'reading_lesson': ('django.db.models.fields.IntegerField', [], {}),
            'reading_total': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            't_l_materials': ('django.db.models.fields.IntegerField', [], {}),
            'training_subtotal': ('django.db.models.fields.IntegerField', [], {}),
            'ts_number': ('django.db.models.fields.IntegerField', [], {}),
            'years_experience': ('django.db.models.fields.CharField', [], {'max_length': '5'})
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
            'Meta': {'object_name': 'School'},
            'emis': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '8'}),
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