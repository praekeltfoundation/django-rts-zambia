# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AcademicAchievementCode.junior_secondary_school'
        db.delete_column(u'data_academicachievementcode', 'junior_secondary_school')

        # Deleting field 'AcademicAchievementCode.primary_school'
        db.delete_column(u'data_academicachievementcode', 'primary_school')

        # Deleting field 'AcademicAchievementCode.diploma'
        db.delete_column(u'data_academicachievementcode', 'diploma')

        # Deleting field 'AcademicAchievementCode.secondary_school'
        db.delete_column(u'data_academicachievementcode', 'secondary_school')

        # Deleting field 'AcademicAchievementCode.primary_school_teacher_diploma'
        db.delete_column(u'data_academicachievementcode', 'primary_school_teacher_diploma')

        # Deleting field 'AcademicAchievementCode.masters'
        db.delete_column(u'data_academicachievementcode', 'masters')

        # Deleting field 'AcademicAchievementCode.other'
        db.delete_column(u'data_academicachievementcode', 'other')

        # Deleting field 'AcademicAchievementCode.bachelors'
        db.delete_column(u'data_academicachievementcode', 'bachelors')

        # Deleting field 'AcademicAchievementCode.secondary_school_teacher_diploma'
        db.delete_column(u'data_academicachievementcode', 'secondary_school_teacher_diploma')

        # Deleting field 'AcademicAchievementCode.primary_school_teacher_certificate'
        db.delete_column(u'data_academicachievementcode', 'primary_school_teacher_certificate')

        # Adding field 'AcademicAchievementCode.achievement'
        db.add_column(u'data_academicachievementcode', 'achievement',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50),
                      keep_default=False)

        from django.core.management import call_command
        call_command('loaddata', 'academic_achievement_code.json')


    def backwards(self, orm):
        # Adding field 'AcademicAchievementCode.junior_secondary_school'
        db.add_column(u'data_academicachievementcode', 'junior_secondary_school',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.primary_school'
        db.add_column(u'data_academicachievementcode', 'primary_school',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.diploma'
        db.add_column(u'data_academicachievementcode', 'diploma',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.secondary_school'
        db.add_column(u'data_academicachievementcode', 'secondary_school',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.primary_school_teacher_diploma'
        db.add_column(u'data_academicachievementcode', 'primary_school_teacher_diploma',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.masters'
        db.add_column(u'data_academicachievementcode', 'masters',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.other'
        db.add_column(u'data_academicachievementcode', 'other',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.bachelors'
        db.add_column(u'data_academicachievementcode', 'bachelors',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.secondary_school_teacher_diploma'
        db.add_column(u'data_academicachievementcode', 'secondary_school_teacher_diploma',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Adding field 'AcademicAchievementCode.primary_school_teacher_certificate'
        db.add_column(u'data_academicachievementcode', 'primary_school_teacher_certificate',
                      self.gf('django.db.models.fields.IntegerField')(default=''),
                      keep_default=False)

        # Deleting field 'AcademicAchievementCode.achievement'
        db.delete_column(u'data_academicachievementcode', 'achievement')


    models = {
        u'data.academicachievementcode': {
            'Meta': {'object_name': 'AcademicAchievementCode'},
            'achievement': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        u'data.inboundsms': {
            'Meta': {'object_name': 'InboundSMS'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'data.learnerperfomancedata': {
            'Meta': {'object_name': 'LearnerPerfomanceData'},
            'below_minimum_results': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
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
        u'data.teacherperfomancedata': {
            'Meta': {'object_name': 'TeacherPerfomanceData'},
            'academic_level': ('django.db.models.fields.IntegerField', [], {}),
            'age': ('django.db.models.fields.IntegerField', [], {}),
            'attitudes_and_beliefs': ('django.db.models.fields.IntegerField', [], {}),
            'classroom_environment_score': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['data.HeadTeacher']"}),
            'emis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['hierarchy.School']"}),
            'g2_pupils_present': ('django.db.models.fields.IntegerField', [], {}),
            'g2_pupils_registered': ('django.db.models.fields.IntegerField', [], {}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_reading_score': ('django.db.models.fields.IntegerField', [], {}),
            'pupil_engagment_score': ('django.db.models.fields.IntegerField', [], {}),
            'pupils_books_number': ('django.db.models.fields.IntegerField', [], {}),
            'pupils_materials_score': ('django.db.models.fields.IntegerField', [], {}),
            'reading_lesson': ('django.db.models.fields.IntegerField', [], {}),
            't_l_materials': ('django.db.models.fields.IntegerField', [], {}),
            'training_subtotal': ('django.db.models.fields.IntegerField', [], {}),
            'years_experience': ('django.db.models.fields.IntegerField', [], {})
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
            'emis': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '5'}),
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