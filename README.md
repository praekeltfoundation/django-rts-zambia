# go-rts-zambia


## Test JS Sandbox

    $ npm install mocha vumigo_v01 jed
    $ npm test

of if you want to have a constant test check running run the following (WARNING: config changes require this watcher restarted)

    $ ./node_modules/.bin/mocha -R spec --watch

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

- `<base_url>/api/v1/data/schooldata/`
- `<base_url>/api/v1/data/schooldata/<id>/`

Academic Achievement Code

- `<base_url>/api/v1/data/achievement/`
- `<base_url>/api/v1/data/achievement/<id>/`

Learner Perfomance

- `<base_url>/api/v1/data/learnerperfomance/`
- `<base_url>/api/v1/data/learnerperfomance/<id>/`

Teacher Perfomance

- `<base_url>/api/v1/data/teacherperfomance/`
- `<base_url>/api/v1/data/teacherperfomance/<id>/`

SMS

- `<base_url>/api/v1/data/sms/`
- `<base_url>/api/v1/data/sms/<id>/`