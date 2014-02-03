# Python
from datetime import datetime
import random

# Project
from hierarchy.models import (Province, District, Zone, School)
from data.models import (HeadTeacher, SchoolData, TeacherPerformanceData,
                         LearnerPerformanceData, InboundSMS,
                         AcademicAchievementCode)


NAMES = ['Aaliyah', 'Abayomi', 'Abebe', 'Abebi', 'Abena', 'Abeo', 'Ada']
SURNAMES = ['Azikiwe', 'Awolowo', 'Bello', 'Balewa', 'Akintola', 'Okotie-Eboh']
PROVINCE_NAMES = ['Central', 'Eastern', 'Lusaka', 'Muchinga', 'Northern', 'Southern', 'Western']
DISTRICT_NAMES = ['Chibombo', 'Kabwe', 'Kapiri Mposhi', 'Mkushi', 'Mumbwa']
ZONE_NAMES = ['zone_1', 'zone_1', 'zone_3', 'zone_4', 'zone_5', 'zone_6', 'zone_7', 'zone_8']
SCHOOL_NAMES = ['Baluba', 'Boyole', 'Buntungwa', 'Burma Road', 'Kansumbi', 'Mikomfwa', 'Zambezi']
ACHIEVEMENTS = ["highschool", "degree", "diploma", "masters"]
MESSAGES = ["Message 1", "Message 2", "Message 3"]


def random_name():
    return random.choice(NAMES)


def random_surname():
    return random.choice(SURNAMES)


def random_full_name():
    return '%s %s' % (random_name(), random_surname())


def random_province_name():
    return random.choice(PROVINCE_NAMES)


def random_district_name():
    return random.choice(DISTRICT_NAMES)


def random_zone_name():
    return random.choice(ZONE_NAMES)


def random_school_name():
    return random.choice(SCHOOL_NAMES)


def random_emis_value():
    return random.randint(1000, 9999)


def random_msisdn_value():
    return str(int(random.randint(1e10, 9e10)))


def random_achievement():
    return random.choice(ACHIEVEMENTS)


def random_message():
    return random.choice(MESSAGES)


def random_district():
    return create_district(random_district_name(), create_province("province"))


def random_datetime():
    year = random.randint(1960, 2000)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return datetime(year, month, day)



def create_province(name=random_province_name()):
    province, _ = Province.objects.get_or_create(name=name)
    return province


def create_district(name=random_district_name(), province=None):
    if not province:
        province = create_province()

    district, _ = District.objects.get_or_create(province=province, name=name)
    return district


def create_zone(name=random_zone_name(), district=None):
    if not district:
        district = create_district()

    zone, _ = Zone.objects.get_or_create(district=district, name=name)
    return zone


def create_school(name=random_school_name(),
                  emis=random_emis_value(),
                  zone=None):
    if not zone:
        zone = create_zone()

    school, _ = School.objects.get_or_create(emis=emis, zone=zone, name=name)
    return school


def create_academic_level(achievement=random_achievement()):
    level, _ = AcademicAchievementCode.objects.get_or_create(achievement=achievement)
    return level


def create_headteacher(first_name=random_name(),
                       last_name=random_surname(),
                       msisdn=random_msisdn_value(),
                       date_of_birth=random_datetime().date(),
                       emis=None,
                       is_zonal_head=random.choice([True, False]),
                       gender=random.choice(["male", "female"])):

    if not emis:
        emis = create_school()

    data = {"first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "msisdn": msisdn,
            "date_of_birth": date_of_birth,
            "is_zonal_head": is_zonal_head,
            "emis": emis}
    headteacher, _ = HeadTeacher.objects.get_or_create(**data)
    return headteacher


def create_school_data(emis=None,
                       name=random_name(),
                       classrooms=random.randint(1, 10),
                       teachers=random.randint(1, 10),
                       teachers_g1=random.randint(1, 10),
                       teachers_g2=random.randint(1, 10),
                       boys_g2=random.randint(1, 10),
                       girls_g2=random.randint(1, 10),
                       created_by=None):

    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    data = {"emis": emis,
            "name": name,
            "classrooms": classrooms,
            "teachers": teachers,
            "teachers_g1": teachers_g1,
            "teachers_g2": teachers_g2,
            "boys_g2": boys_g2,
            "girls_g2": girls_g2,
            "created_by": created_by}

    schooldata, _ = SchoolData.objects.get_or_create(**data)
    return schooldata


def create_teacher_perfomance_data(gender=random.choice(["male", "female"]),
                                   age=random.randint(20, 60),
                                   years_experience=random.randint(1, 60),
                                   g2_pupils_present=random.randint(20, 60),
                                   g2_pupils_registered=random.randint(20, 60),
                                   classroom_environment_score=random.randint(20, 60),
                                   t_l_materials=random.randint(20, 60),
                                   pupils_materials_score=random.randint(20, 60),
                                   pupils_books_number=random.randint(20, 60),
                                   reading_lesson=random.randint(20, 60),
                                   pupil_engagement_score=random.randint(20, 60),
                                   attitudes_and_beliefs=random.randint(20, 60),
                                   training_subtotal=random.randint(20, 60),
                                   ts_number=random.randint(20, 60),
                                   reading_assessment=random.randint(20, 60),
                                   reading_total=random.randint(20, 60),
                                   academic_level=None,
                                   emis=None,
                                   created_by=None):

    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    if not academic_level:
        academic_level = create_academic_level()

    data = {"gender": gender,
            "age": age,
            "years_experience": years_experience,
            "g2_pupils_present": g2_pupils_present,
            "g2_pupils_registered": g2_pupils_registered,
            "classroom_environment_score": classroom_environment_score,
            "t_l_materials": t_l_materials,
            "pupils_materials_score": pupils_materials_score,
            "pupils_books_number": pupils_books_number,
            "reading_lesson": reading_lesson,
            "pupil_engagement_score": pupil_engagement_score,
            "attitudes_and_beliefs": attitudes_and_beliefs,
            "training_subtotal": training_subtotal,
            "ts_number": ts_number,
            "reading_assessment": reading_assessment,
            "reading_total": reading_total,
            "emis": emis,
            "academic_level": academic_level,
            "created_by": created_by}

    teacher_per, _ = TeacherPerformanceData.objects.get_or_create(**data)
    return teacher_per


def create_learner_perfomance_data(gender=random.choice(["male", "female"]),
                                   total_number_pupils=random.randint(1, 60),
                                   phonetic_awareness=random.randint(20, 60),
                                   vocabulary=random.randint(20, 60),
                                   reading_comprehension=random.randint(20, 60),
                                   writing_diction=random.randint(20, 60),
                                   below_minimum_results=random.randint(20, 60),
                                   minimum_results=random.randint(20, 60),
                                   desirable_results=random.randint(20, 60),
                                   outstanding_results=random.randint(20, 60),
                                   emis=None,
                                   created_by=None):
    if not emis:
        emis = create_school()

    if not created_by:
        created_by = create_headteacher()

    data = {"gender": gender,
            "total_number_pupils": total_number_pupils,
            "phonetic_awareness": phonetic_awareness,
            "vocabulary": vocabulary,
            "reading_comprehension": reading_comprehension,
            "writing_diction": writing_diction,
            "below_minimum_results": below_minimum_results,
            "minimum_results": minimum_results,
            "desirable_results": desirable_results,
            "outstanding_results": outstanding_results,
            "emis": emis,
            "created_by": created_by}

    learner_per, _ = LearnerPerformanceData.objects.get_or_create(**data)
    return learner_per


def create_inbound_sms(message=random_message(),
                       created_by=None):

    if not created_by:
        created_by = create_headteacher()

    data = {"message": message,
            "created_by": created_by}
    inbound_sms, _ = InboundSMS.objects.get_or_create(**data)
    return inbound_sms
