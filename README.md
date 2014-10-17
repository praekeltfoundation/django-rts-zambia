# django-rts-zambia

Django backend for go-rts-zambia

## URI for API
### Hierarchy
Province

- `<base_url>/api/v1/province/<id>/`
- `<base_url>/api/v1/province/<id>/`

District

- `<base_url>/api/v1/district/<id>/`
- `<base_url>/api/v1/district/<id>/`

Zone

- `<base_url>/api/v1/zone/<id>/`
- `<base_url>/api/v1/zone/<id>/`

School

- `<base_url>/api/v1/school/<id>/`
- `<base_url>/api/v1/school/<id>/`
- `<base_url>/api/v1/school/emis/<emis>/` (school by emis)

### Data
Head Teacher

- `<base_url>/api/v1/data/headteacher/`
- `<base_url>/api/v1/data/headteacher/<id>/`
- `<base_url>/api/v1/data/headteacher/emis/<emis>/` (to be used to post data)
- `<base_url>/api/v1/data/headteacher/?emis__emis=4817` (filter for specific teacher emis [GET])

School Data

- `<base_url>/api/v1/data/school/`
- `<base_url>/api/v1/data/school/<id>/`

Academic Achievement Code

- `<base_url>/api/v1/data/achievement/`
- `<base_url>/api/v1/data/achievement/<id>/`

Learner Performance

- `<base_url>/api/v1/data/learnerperformance/`
- `<base_url>/api/v1/data/learnerperformance/<id>/`

Teacher Performance

- `<base_url>/api/v1/data/teacherperformance/`
- `<base_url>/api/v1/data/teacherperformance/<id>/`

SMS

- `<base_url>/api/v1/data/sms/`
- `<base_url>/api/v1/data/sms/<id>/`