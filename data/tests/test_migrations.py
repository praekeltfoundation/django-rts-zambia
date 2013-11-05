from django.test import TransactionTestCase
from data.models import (HeadTeacher, SchoolData,
                         TeacherPerformanceData, LearnerPerformanceData,
                         HeadTeacherDuplicateStore, SchoolDataDuplicateStore)
from django.core.management import call_command
from south.migration import Migrations


class TestDuplicatesDataMigration(TransactionTestCase):
    """
    Testing to see if the migration removes and stores the duplicates.
    """
    fixtures = ['test_migration_hierarchy.json', 'test_data_migration.json']
    start_migration = "0014_delete_none_field"
    dest_migration = "0015_delete_duplicates"
    django_application = "data"

    def setUp(self):
        super(TestDuplicatesDataMigration, self).setUp()
        migrations = Migrations(self.django_application)
        self.start_orm = migrations[self.start_migration].orm()
        self.dest_orm = migrations[self.dest_migration].orm()

        # Ensure the migration history is up-to-date with a fake migration.
        # The other option would be to use the south setting for these tests
        # so that the migrations are used to setup the test db.
        call_command('migrate', self.django_application, fake=True,
                     verbosity=0)

        # Then migrate back to the start migration.
        call_command('migrate', self.django_application, self.start_migration,
                     verbosity=0)

    def tearDown(self):
        # Leave the db in the final state so that the test runner doesn't
        # error when truncating the database.
        call_command('migrate', self.django_application, verbosity=0)

    def migrate_to_dest(self):
        call_command('migrate', self.django_application, self.dest_migration,
                     verbosity=0)

    def test_fixtures_loaded(self):
        head_teacher = HeadTeacher.objects.filter(emis__emis=2525).all()
        self.assertEqual(len(head_teacher), 4)

        self.migrate_to_dest()
        head_teacher = HeadTeacher.objects.filter(emis__emis=2525).all()
        self.assertEqual(len(head_teacher), 1)

        ht_dup = HeadTeacherDuplicateStore.objects.filter(emis__emis=2525).all()
        self.assertEqual(len(ht_dup), 3)
        [self.assertGreater(head_teacher[0].id, obj.origin_id) for obj in ht_dup]


class TestRemoveNoneDataMigration(TransactionTestCase):
    """
    Testing to see if the migration removes and stores the duplicates.
    """
    fixtures = ['test_migration_hierarchy.json', 'test_data_migration.json']
    start_migration = "0013_delete_teacherperfomance_learnerperformance_data"
    dest_migration = "0014_delete_none_field"
    django_application = "data"

    def setUp(self):
        super(TestRemoveNoneDataMigration, self).setUp()
        migrations = Migrations(self.django_application)
        self.start_orm = migrations[self.start_migration].orm()
        self.dest_orm = migrations[self.dest_migration].orm()

        # Ensure the migration history is up-to-date with a fake migration.
        # The other option would be to use the south setting for these tests
        # so that the migrations are used to setup the test db.
        call_command('migrate', self.django_application, fake=True,
                     verbosity=0)

        # Then migrate back to the start migration.
        call_command('migrate', self.django_application, self.start_migration,
                     verbosity=0)

    def tearDown(self):
        # Leave the db in the final state so that the test runner doesn't
        # error when truncating the database.
        call_command('migrate', self.django_application, verbosity=0)

    def migrate_to_dest(self):
        call_command('migrate', self.django_application, self.dest_migration,
                     verbosity=0)

    def test_fixtures_loaded(self):
        head_teacher = HeadTeacher.objects.filter(emis__emis=None).all()
        self.assertEqual(len(head_teacher), 45)

        self.migrate_to_dest()
        head_teacher = HeadTeacher.objects.filter(emis__emis=None).all()
        self.assertEqual(len(head_teacher), 0)


class TestRemovePerfomanceDataMigration(TransactionTestCase):
    """
    Testing to see if the migration removes and stores the duplicates.
    """
    fixtures = ['test_migration_hierarchy.json', 'test_data_migration.json']
    start_migration = "0012_auto__add_headteacherduplicatestore__add_schooldataduplicatestore"
    dest_migration = "0013_delete_teacherperfomance_learnerperformance_data"
    django_application = "data"

    def setUp(self):
        super(TestRemovePerfomanceDataMigration, self).setUp()
        migrations = Migrations(self.django_application)
        self.start_orm = migrations[self.start_migration].orm()
        self.dest_orm = migrations[self.dest_migration].orm()

        # Ensure the migration history is up-to-date with a fake migration.
        # The other option would be to use the south setting for these tests
        # so that the migrations are used to setup the test db.
        call_command('migrate', self.django_application, fake=True,
                     verbosity=0)

        # Then migrate back to the start migration.
        call_command('migrate', self.django_application, self.start_migration,
                     verbosity=0)

    def tearDown(self):
        # Leave the db in the final state so that the test runner doesn't
        # error when truncating the database.
        call_command('migrate', self.django_application, verbosity=0)

    def migrate_to_dest(self):
        call_command('migrate', self.django_application, self.dest_migration,
                     verbosity=0)

    def test_fixtures_loaded(self):
        head_data = TeacherPerformanceData.objects.all()
        learner_data = LearnerPerformanceData.objects.all()
        self.assertEqual(len(head_data), 1612)
        self.assertEqual(len(learner_data), 86)

        self.migrate_to_dest()
        head_data = TeacherPerformanceData.objects.all()
        learner_data = LearnerPerformanceData.objects.all()
        self.assertEqual(len(head_data), 0)
        self.assertEqual(len(learner_data), 0)
