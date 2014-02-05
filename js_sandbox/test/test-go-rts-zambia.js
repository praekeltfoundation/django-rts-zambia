var fs = require("fs");
var assert = require("assert");
var vumigo = require("vumigo_v01");
var app = require("../lib/go-rts-zambia");

// This just checks that you hooked you InteractionMachine
// up to the api correctly and called im.attach();
describe("test_api", function() {
    it("should exist", function() {
        assert.ok(app.api);
    });
    it("should have an on_inbound_message method", function() {
        assert.ok(app.api.on_inbound_message);
    });
    it("should have an on_inbound_event method", function() {
        assert.ok(app.api.on_inbound_event);
    });
});

var test_fixtures_full = [
    'test/fixtures/get_hierarchy.json',
    'test/fixtures/put_registration_update_msisdn.json',
    'test/fixtures/put_registration_update_emis.json',
    'test/fixtures/post_registration_headteacher.json',
    'test/fixtures/post_registration_headteacher_zonal.json',
    'test/fixtures/post_registration_school.json',
    'test/fixtures/post_registration_school_update.json',
    'test/fixtures/post_registration_school_manage_update_data.json',
    'test/fixtures/post_performance_teacher.json',
    'test/fixtures/post_performance_learner_boys.json',
    'test/fixtures/post_performance_learner_girls.json',
    'test/fixtures/get_headteacher_filter_emis.json'
];

var tester;

describe("When using the USSD line as an unrecognised MSISDN", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it('should tell us whether a date string is acceptable', function(done) {
        var state_creator = app.api.im.state_creator;
        assert.equal(
            state_creator.check_and_parse_date('11091980').toISOString(),
            new Date(1980,8,11).toISOString());
        assert.equal(
            state_creator.check_and_parse_date('11th Sept 1980'),
            false);
        assert.equal(
            state_creator.check_and_parse_date('2013-08-01'),
            false);
        done();
    });

    // first test should always start 'null, null' because we haven't
    // started interacting yet
    it("first display navigation menu", function (done) {
        var p = tester.check_state({
            user: null,
            content: null,
            next_state: "initial_state",
            response: "^Welcome to the Zambia School Gateway! What would you like to do\\?[^]" +
                    "1. Register as a new user\\.[^]" +
                    "2. Change my school\\.[^]" +
                    "3. Change my primary cell phone number\\.$"
        });
        p.then(done, done);
    });

    it("selecting to register should ask for EMIS", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_emis",
            response: "^Please enter your school's EMIS number. " +
                "This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("entering valid EMIS should thank user", function (done) {
        var user = {
            current_state: 'reg_emis',
            answers: {
                initial_state: 'reg_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "0001",
            next_state: "reg_emis_validator",
            response: "^Thanks for claiming this EMIS. Redial this number if you ever " +
                "change cellphone number to reclaim the EMIS and continue to receive " +
                "SMS updates.[^]" +
                "1. Continue$"
        });
        p.then(done, done);
    });


    it("choosing to continue should ask for School Name", function (done) {
        var user = {
            current_state: 'reg_emis_validator',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_school_name",
            response: "^Please enter the name of your school, e.g. Kapililonga$"
        });
        p.then(done, done);
    });

    it("entering invalid EMIS twice should exit", function (done) {
        var user = {
            current_state: 'reg_emis_try_2',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '000A',
                reg_emis_error: 'reg_emis_try_2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "000B",
            next_state: "reg_exit_emis",
            response: "^We don't recognise your EMIS number\\. Please send a" +
                " SMS with the words EMIS ERROR to 739 and your DEST will" +
                " contact you to resolve the problem\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering invalid EMIS and choosing to exit should tell send SMS", function (done) {
        var user = {
            current_state: 'reg_emis_error',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '000A'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_exit_emis",
            response: "^We don't recognise your EMIS number\\. Please send a" +
                " SMS with the words EMIS ERROR to 739 and your DEST will" +
                " contact you to resolve the problem\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering invalid EMIS and choosing to reenter should ask EMIS", function (done) {
        var user = {
            current_state: 'reg_emis_error',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '000A'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_emis_try_2",
            response: "^Please enter your school's EMIS number. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("entering School Name should ask for users name", function (done) {
        var user = {
            current_state: 'reg_school_name',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "School One",
            next_state: "reg_first_name",
            response: "^Please enter your FIRST name.$"
        });
        p.then(done, done);
    });

    it("entering name should ask for users surname", function (done) {
        var user = {
            current_state: 'reg_first_name',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Jack",
            next_state: "reg_surname",
            response: "^Now please enter your SURNAME.$"
        });
        p.then(done, done);
    });

    it("entering suname should ask for users date of birth", function (done) {
        var user = {
            current_state: 'reg_surname',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Black",
            next_state: "reg_date_of_birth",
            response: "^Please enter your date of birth. Start with the day, followed by " +
                "the month and year, e.g. 27111980$"
        });
        p.then(done, done);
    });

    it("entering valid date of birth should ask for users gender", function (done) {
        var user = {
            current_state: 'reg_date_of_birth',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "11091980",
            next_state: "reg_gender",
            response: "^What is your gender\\?[^]" +
            "1. Female[^]" +
            "2. Male$"
        });
        p.then(done, done);
    });

    it("entering invalid date of birth should error", function (done) {
        var user = {
            current_state: 'reg_date_of_birth',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "11 Sep 1980",
            next_state: "reg_date_of_birth",
            response: "^Please enter your date of birth formatted DDMMYYYY$"
        });
        p.then(done, done);
    });

    it("entering gender should ask for boys number", function (done) {
        var user = {
            current_state: 'reg_gender',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_boys",
            response: "^How many boys do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("entering boys number in school should ask for girls number", function (done) {
        var user = {
            current_state: 'reg_school_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "50",
            next_state: "reg_school_girls",
            response: "^How many girls do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid boys number in school should error", function (done) {
        var user = {
            current_state: 'reg_school_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "fifty",
            next_state: "reg_school_boys",
            response: "^Please provide a number value for how many boys you have in your school\\.$"
        });
        p.then(done, done);
    });

    it("entering girls number in school should ask for classroom number", function (done) {
        var user = {
            current_state: 'reg_school_girls',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "51",
            next_state: "reg_school_classrooms",
            response: "^How many classrooms do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid girls number in school should error", function (done) {
        var user = {
            current_state: 'reg_school_girls',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "fifty",
            next_state: "reg_school_girls",
            response: "^Please provide a number value for how many girls you have in your school\\.$"
        });
        p.then(done, done);
    });

    it("entering school classrooms should ask for teachers number", function (done) {
        var user = {
            current_state: 'reg_school_classrooms',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "reg_school_teachers",
            response: "^How many teachers are presently working in your school, including " +
                "the head teacher\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid school classrooms number should error", function (done) {
        var user = {
            current_state: 'reg_school_classrooms',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "five",
            next_state: "reg_school_classrooms",
            response: "^Please provide a number value for how many classrooms you have in your school\\.$"
        });
        p.then(done, done);
    });

    it("entering invalid school classrooms number starting with number should error", function (done) {
        var user = {
            current_state: 'reg_school_classrooms',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "12dd",
            next_state: "reg_school_classrooms",
            response: "^Please provide a number value for how many classrooms you have in your school\\.$"
        });
        p.then(done, done);
    });

    it("entering teachers number should ask for G1 teachers number", function (done) {
        var user = {
            current_state: 'reg_school_teachers',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "reg_school_teachers_g1",
            response: "^How many teachers teach Grade 1 local language\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "five",
            next_state: "reg_school_teachers",
            response: "^Please provide a number value for how many teachers in total you have in your school\\.$"
        });
        p.then(done, done);
    });

    it("entering teachers G1 number should ask for G2 teachers number", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g1',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_teachers_g2",
            response: "^How many teachers teach Grade 2 local language\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers G1 number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g1',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "two",
            next_state: "reg_school_teachers_g1",
            response: "^Please provide a number value for how many teachers teach G1 local language literacy\\.$"
        });
        p.then(done, done);
    });

    it("entering teachers G2 number should ask for G2 boys number", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g2',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_students_g2_boys",
            response: "^How many boys are ENROLLED in Grade 2 at your school\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers G2 number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g2',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "two",
            next_state: "reg_school_teachers_g2",
            response: "^Please provide a number value for how many teachers teach G2 local language literacy\\.$"
        });
        p.then(done, done);
    });

    it("entering student boys G2 number should ask for G2 girls number", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "10",
            next_state: "reg_school_students_g2_girls",
            response: "^How many girls are ENROLLED in Grade 2 at your school\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid student boys G2 number should error", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "ten",
            next_state: "reg_school_students_g2_boys",
            response: "^Please provide a number value for the total number of G2 boys enrolled\\.$"
        });
        p.then(done, done);
    });

    it("entering student girls G2 number should ask for zonal head", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_girls',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "11",
            next_state: "reg_zonal_head",
            response: "^Are you a Zonal Head Teacher\\?[^]" +
                    "1. Yes[^]" +
                    "2. No$"
        });
        p.then(done, done);
    });

    it("entering invalid student girls G2 number should error", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_girls',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "eleven",
            next_state: "reg_school_students_g2_girls",
            response: "^Please provide a number value for the total number of G2 girls enrolled\\.$"
        });
        p.then(done, done);
    });

    it("saying not zonal head should ask for zonal head name", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10',
                reg_school_students_g2_girls: '11'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_zonal_head_name",
            response: "^Please enter the name and surname of your ZONAL HEAD TEACHER.$"
        });
        p.then(done, done);
    });

    it("saying are zonal head should thank long and close", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10',
                reg_school_students_g2_girls: '11'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_thanks_zonal_head",
            response: "^Well done! You are now registered as a Zonal Head" +
                " Teacher\\. When you are ready, dial in to start" +
                " reporting\\. You will also receive monthly SMS's from" +
                " your zone\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering name of zonal head should thank and close", function (done) {
        var user = {
            current_state: 'reg_zonal_head_name',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_emis_validator: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11091980',
                reg_gender: 'male',
                reg_school_boys: '50',
                reg_school_girls: '51',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10',
                reg_school_students_g2_girls: '11',
                reg_zonal_head: 'reg_zonal_head_name'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Jim Carey",
            next_state: "reg_thanks_head_teacher",
            response: "^Congratulations! You are now registered as a user of" +
                " the Gateway! Please dial in again when you are ready to" +
                " start reporting on teacher and learner performance\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("selecting to change primary number should ask for EMIS", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "3",
            next_state: "manage_change_msisdn_emis",
            response: "^Please enter the school's EMIS number that you are currently registered " +
                "with. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("entering valid EMIS should thank the user and exit", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis',
            answers: {
                initial_state: 'manage_change_msisdn_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "0001",
            next_state: "manage_change_msisdn_emis_validator",
            response: "^Thank you! Your cell phone number is now the official" +
                " number that your school will use to communicate with the" +
                " Gateway\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering invalid EMIS should ask for reenter or exit", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis',
            answers: {
                initial_state: 'manage_change_msisdn_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "000A",
            next_state: "manage_change_msisdn_emis_error",
            response: "^There is a problem with the EMIS number you" +
                " have entered\\.[^]" +
                "1. Try again[^]" +
                "2. Exit$"
        });
        p.then(done, done);
    });

    it("entering invalid EMIS and choosing to exit should tell send SMS", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis_error',
            answers: {
                initial_state: 'manage_change_msisdn_confirm',
                manage_change_msisdn_emis_lookup: '000A'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_exit_emis",
            response: "^We don't recognise your EMIS number\\. Please send" +
                " a SMS with the words EMIS ERROR to 739 and your DEST will" +
                " contact you to resolve the problem\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("when changing MSISDN entering invalid EMIS and choosing to reenter should ask EMIS", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis_error',
            answers: {
                initial_state: 'manage_change_msisdn_emis',
                manage_change_msisdn_emis: '000A'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "manage_change_msisdn_emis_try_2",
            response: "^Please enter the school's EMIS number that you are currently registered with. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("selecting to change school should ask to change MSISDN first", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "manage_change_emis_error",
            response: "^Your cell phone number is unrecognised. Please associate your new number with " +
                "your old EMIS first before requesting to change school.[^]" +
                "1. Main menu.[^]" +
                "2. Exit.$"
        });
        p.then(done, done);
    });

});


describe("When using the USSD line as an recognised MSISDN to change school", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("selecting to change school should ask for EMIS", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "3",
            next_state: "manage_change_emis",
            response: "^Please enter your school's EMIS number. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("entering valid EMIS should confirm claim", function (done) {
        var user = {
            current_state: 'manage_change_emis',
            answers: {
                initial_state: 'manage_change_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2334",
            next_state: "manage_change_emis_validator",
            response: "^Thanks for claiming this EMIS. Redial this number if you ever change cellphone " +
                    "number to reclaim the EMIS and continue to receive SMS updates.[^]" +
                    "1. Continue$"
        });
        p.then(done, done);
    });

    it("choosing to continue after switching EMIS should ask for School classrooms", function (done) {
        var user = {
            current_state: 'manage_change_emis_validator',
            answers: {
                initial_state: 'manage_change_emis',
                manage_change_emis: "2334"
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_school_boys",
            response: "^How many boys do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("saying are zonal head after association with new school should thank long and close", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'manage_change_emis',
                manage_change_emis: '2334',
                manage_change_emis_validator: '2334',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2',
                reg_school_teachers_g2: '2',
                reg_school_students_g2_boys: '10',
                reg_school_students_g2_girls: '11',
                reg_school_boys: '50',
                reg_school_girls: '51'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_thanks_zonal_head",
            response: "^Well done! You are now registered as a Zonal Head" +
                " Teacher\\. When you are ready, dial in to start" +
                " reporting\\. You will also receive monthly SMS's from" +
                " your zone\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

});



describe("When using the USSD line as an recognised MSISDN to report on teachers", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    // first test should always start 'null, null' because we haven't
    // started interacting yet
    it("first display navigation menu", function (done) {
        var p = tester.check_state({
            user: null,
            content: null,
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance\\.[^]" +
                    "3. Change my school\\.[^]" +
                    "4. Update my school’s registration data\\.$"
        });
        p.then(done, done);
    });

    it("selecting to report on teacher performance should ask for teacher TS number", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "perf_teacher_ts_number",
            response: "^Please enter the teacher's TS number\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher TS number incorrectly should ask for teacher TS number again", function (done) {
        var user = {
            current_state: 'perf_teacher_ts_number',
            answers: {
                initial_state: 'perf_teacher_ts_number'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "One Hundred and Six",
            next_state: "perf_teacher_ts_number",
            response: "^Please provide a number value for the teacher's TS number\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher TS number should ask for gender", function (done) {
        var user = {
            current_state: 'perf_teacher_ts_number',
            answers: {
                initial_state: 'perf_teacher_ts_number'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "106",
            next_state: "perf_teacher_gender",
            response: "^What is the gender of the teacher\\?[^]" +
            "1. Male[^]" +
            "2. Female$"
        });
        p.then(done, done);
    });

    it("entering teacher gender should ask for age", function (done) {
        var user = {
            current_state: 'perf_teacher_gender',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "perf_teacher_age",
            response: "^Please enter the teacher's age in years e\\.g\\. 26\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher age incorrectly should ask for age again", function (done) {
        var user = {
            current_state: 'perf_teacher_age',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "One",
            next_state: "perf_teacher_age",
            response: "^Please provide a number value for the teacher's age\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher age should ask for academic achievement", function (done) {
        var user = {
            current_state: 'perf_teacher_age',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "30",
            next_state: "perf_teacher_academic_level",
            response: "^What is the teacher's highest education level\\?[^]" +
            "1. Gr 7[^]" +
            "2. Gr 9[^]" +
            "3. Gr 12[^]" +
            "4. PTC[^]" +
            "5. PTD[^]" +
            "6. Dip Ed[^]" +
            "7. Other diploma[^]" +
            "8. BA Degree[^]" +
            "9. MA Degree[^]" +
            "10. Other$"
        });
        p.then(done, done);
    });

    it("entering academic achievement should ask for years experience", function (done) {
        var user = {
            current_state: 'perf_teacher_academic_level',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "3",
            next_state: "perf_teacher_years_experience",
            response: "^How many years of teaching experience does this teacher have\\?[^]" +
                "1. 0 - 3 years[^]" +
                "2. 4 - 8 years[^]" +
                "3. 9 - 12 years[^]" +
                "4. 13 years or more$"
        });
        p.then(done, done);
    });

    it("entering years experience should ask G2 pupils present", function (done) {
        var user = {
            current_state: 'perf_teacher_years_experience',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "perf_teacher_g2_pupils_present",
            response: "^How many children were PRESENT during the observed lesson\\?$"
        });
        p.then(done, done);
    });


    it("entering G2 pupils present incorrectly should ask G2 pupils present again", function (done) {
        var user = {
            current_state: 'perf_teacher_g2_pupils_present',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "forty",
            next_state: "perf_teacher_g2_pupils_present",
            response: "^Please provide a number value for pupils present\\.$"
        });
        p.then(done, done);
    });

    it("entering G2 pupils present should ask G2 pupils registered", function (done) {
        var user = {
            current_state: 'perf_teacher_g2_pupils_present',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "40",
            next_state: "perf_teacher_g2_pupils_registered",
            response: "^How many children are ENROLLED in the Grade 2 class that was observed\\?$"
        });
        p.then(done, done);
    });

    it("entering G2 pupils registered incorrectly should ask G2 pupils registered again", function (done) {
        var user = {
            current_state: 'perf_teacher_g2_pupils_registered',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "fifty",
            next_state: "perf_teacher_g2_pupils_registered",
            response: "^Please provide a number value for pupils enrolled\\.$"
        });
        p.then(done, done);
    });

    it("entering G2 pupils registered should ask classroom environment score", function (done) {
        var user = {
            current_state: 'perf_teacher_g2_pupils_registered',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "50",
            next_state: "perf_teacher_classroom_environment_score",
            response: "^Enter the subtotal that the teacher achieved during the classroom observation for Section 2 \\(Classroom Environment\\)\\.$"
        });
        p.then(done, done);
    });

    it("entering classroom environment score incorrectly should ask classroom environment score again", function (done) {
        var user = {
            current_state: 'perf_teacher_classroom_environment_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "great",
            next_state: "perf_teacher_classroom_environment_score",
            response: "^Please provide a number value for the Classroom Environment subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering classroom environment score should ask T&L Materials Score", function (done) {
        var user = {
            current_state: 'perf_teacher_classroom_environment_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "10",
            next_state: "perf_teacher_t_l_materials",
            response: "^Enter the subtotal that the teacher achieved during the classroom " +
                "observation for Section 3 \\(Teaching and Learning Materials\\)\\.$"
        });
        p.then(done, done);
    });

    it("entering T&L Materials Score incorrectly should ask T&L Materials Score again", function (done) {
        var user = {
            current_state: 'perf_teacher_t_l_materials',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "rubbish",
            next_state: "perf_teacher_t_l_materials",
            response: "^Please provide a number value for the Teaching and Learning Materials subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering T&L Materials Score should ask Pupil Books Number", function (done) {
        var user = {
            current_state: 'perf_teacher_t_l_materials',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "perf_teacher_pupils_books_number",
            response: "^Enter the number of learners' books \\(text books\\) for literacy that " +
                "were available in the classroom during the lesson observation.$"
        });
        p.then(done, done);
    });

    it("entering Pupil Books Number incorrectly should ask Pupil Books Number again", function (done) {
        var user = {
            current_state: 'perf_teacher_pupils_books_number',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "fab",
            next_state: "perf_teacher_pupils_books_number",
            response: "^Please provide a number value for number of learners' books\\.$"
        });
        p.then(done, done);
    });

    it("entering Pupil Books Number should ask Learner Materials number", function (done) {
        var user = {
            current_state: 'perf_teacher_pupils_books_number',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "90",
            next_state: "perf_teacher_pupils_materials_score",
            response: "^Enter the subtotal that the teacher achieved during the classroom observation " +
            "for Section 4 \\(Learner Materials\\)\\.$"
        });
        p.then(done, done);
    });

    it("entering Learner Materials number incorrectly should ask Learner Materials number again", function (done) {
        var user = {
            current_state: 'perf_teacher_pupils_materials_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "score is seventy five",
            next_state: "perf_teacher_pupils_materials_score",
            response: "^Please provide a number value for the Learner Materials subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering Learner Materials number should ask Time on Task", function (done) {
        var user = {
            current_state: 'perf_teacher_pupils_materials_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "75",
            next_state: "perf_teacher_reading_lesson",
            response: "^Enter the subtotal that the teacher achieved during the classroom " +
                "observation for Section 5 \\(Time on Task and Reading Practice\\)$"
        });
        p.then(done, done);
    });

    it("entering Time on Task subtotal incorrectly should ask Time on Task again", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_lesson',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "forty five mins",
            next_state: "perf_teacher_reading_lesson",
            response: "^Please provide a number value for the Time on Task and Reading Practice subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering Time on Task subtotal should ask pupil engagement score", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_lesson',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "45",
            next_state: "perf_teacher_pupil_engagement_score",
            response: "^Enter the subtotal that the teacher achieved during the " +
                "classroom observation for Section 6 \\(Learner Engagement\\)$"
        });
        p.then(done, done);
    });

it("entering pupil engagement score subtotal incorrectly should ask pupil engagement score again", function (done) {
        var user = {
            current_state: 'perf_teacher_pupil_engagement_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "low",
            next_state: "perf_teacher_pupil_engagement_score",
            response: "^Please provide a number value for the Learner Engagement subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering pupil engagement score subtotal should ask attitudes and beliefs", function (done) {
        var user = {
            current_state: 'perf_teacher_pupil_engagement_score',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "22",
            next_state: "perf_teacher_attitudes_and_beliefs",
            response: "^Enter the subtotal that the teacher achieved during the interview " +
                "on Section 7.1. \\(Teacher Attitudes and Beliefs\\)$"
        });
        p.then(done, done);
    });

    it("entering attitudes and beliefs subtotal incorrectly should ask attitudes and beliefs again", function (done) {
        var user = {
            current_state: 'perf_teacher_attitudes_and_beliefs',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "great",
            next_state: "perf_teacher_attitudes_and_beliefs",
            response: "^Please provide a number value for the Teacher Attitudes and Beliefs subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering attitudes and beliefs subtotal should ask teacher training subtotal", function (done) {
        var user = {
            current_state: 'perf_teacher_attitudes_and_beliefs',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "17",
            next_state: "perf_teacher_training_subtotal",
            response: "^Enter the subtotal that the teacher achieved during the interview on " +
                "Section 7.2. \\(Teacher Training\\)$"
        });
        p.then(done, done);
    });

    it("entering teacher training subtotal incorrectly should ask teacher training subtotal again", function (done) {
        var user = {
            current_state: 'perf_teacher_training_subtotal',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "five",
            next_state: "perf_teacher_training_subtotal",
            response: "^Please provide a number value for the Teacher Training interview subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher training subtotal should ask Reading Assessment", function (done) {
        var user = {
            current_state: 'perf_teacher_training_subtotal',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "perf_teacher_reading_assessment",
            response: "^Enter the subtotal that the teacher achieved during the interview " +
                "on Section 7.3. \\(Reading Assessment\\).$"
        });
        p.then(done, done);
    });

    it("entering reading assessment subtotal incorrectly should ask reading assessment subtotal again", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_assessment',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17',
                perf_teacher_training_subtotal: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "seven",
            next_state: "perf_teacher_reading_assessment",
            response: "^Please provide a number value for the Reading Assessment subtotal\\.$"
        });
        p.then(done, done);
    });

    it("entering Reading Assessment subtotal should ask Readers total", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_assessment',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17',
                perf_teacher_training_subtotal: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "7",
            next_state: "perf_teacher_reading_total",
            response: "^According to your assessment records, how many of the pupils in the class " +
                "that was observed have broken through\\/can read\\?$"
        });
        p.then(done, done);
    });

    it("entering reader total incorrectly should ask readers total again", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_total',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17',
                perf_teacher_training_subtotal: '5',
                perf_teacher_reading_assessment: '7'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "nine",
            next_state: "perf_teacher_reading_total",
            response: "^Please provide a number value for the pupils in the class that have broken " +
                "through\\/can read\\.$"
        });
        p.then(done, done);
    });

    it("entering Readers total show success and options", function (done) {
        var user = {
            current_state: 'perf_teacher_reading_total',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17',
                perf_teacher_training_subtotal: '5',
                perf_teacher_reading_assessment: '7'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "9",
            next_state: "perf_teacher_completed",
            response: "^Congratulations, you have finished reporting on this teacher\\.[^]" +
                "1. Add another teacher\\.[^]" +
                "2. Go back to the main menu\\.[^]" +
                "3. Exit\\.$"
        });
        p.then(done, done);
    });


});

describe("When using the USSD line as an recognised MSISDN - completed Teacher review", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1,
                    "rts_last_save_performance_teacher": "106"
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("selecting to report on another teacher performance should ask for teacher TS number", function (done) {
        var user = {
            current_state: 'perf_teacher_completed',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "perf_teacher_ts_number",
            response: "^Please enter the teacher's TS number\\.$"
        });
        p.then(done, done);
    });

    it("selecting to go to main menu should show it", function (done) {
        var user = {
            current_state: 'perf_teacher_completed',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance\\.[^]" +
                    "3. Change my school\\.[^]" +
                    "4. Update my school’s registration data\\.$"
        });
        p.then(done, done);
    });

    it("selecting to go to exit should thank and close", function (done) {
        var user = {
            current_state: 'perf_teacher_completed',
            answers: {
                initial_state: 'perf_teacher_ts_number',
                perf_teacher_ts_number: '106',
                perf_teacher_gender: 'female',
                perf_teacher_age: '30',
                perf_teacher_academic_level: '3',
                perf_teacher_years_experience: '0-3',
                perf_teacher_g2_pupils_present: '40',
                perf_teacher_g2_pupils_registered: '50',
                perf_teacher_classroom_environment_score: '10',
                perf_teacher_t_l_materials: '5',
                perf_teacher_pupils_books_number: '90',
                perf_teacher_pupils_materials_score: '75',
                perf_teacher_reading_lesson: '45',
                perf_teacher_pupil_engagement_score: '22',
                perf_teacher_attitudes_and_beliefs: '17'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "3",
            next_state: "end_state",
            response: "^Goodbye! Thank you for using the Gateway\\.$",
            continue_session: false
        });
        p.then(done, done);
    });

});

describe("When using the USSD line as an recognised MSISDN to report on learners", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    // first test should always start 'null, null' because we haven't
    // started interacting yet
    it("first display navigation menu", function (done) {
        var p = tester.check_state({
            user: null,
            content: null,
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance\\.[^]" +
                    "3. Change my school\\.[^]" +
                    "4. Update my school’s registration data\\.$"
        });
        p.then(done, done);
    });

    it("selecting to report on learner performance should ask for total boys", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "perf_learner_boys_total",
            response: "^How many boys took part in the learner assessment\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys incorrectly should ask for total boys again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_total',
            answers: {
                initial_state: 'perf_learner_boys_total'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Fifty two",
            next_state: "perf_learner_boys_total",
            response: "^Please provide a number value for total boys assessed\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys should ask for total girls", function (done) {
        var user = {
            current_state: 'perf_learner_boys_total',
            answers: {
                initial_state: 'perf_learner_boys_total'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "52",
            next_state: "perf_learner_girls_total",
            response: "^How many girls took part in the learner assessment\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls incorrectly should ask for total girls again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_total',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "forty two",
            next_state: "perf_learner_girls_total",
            response: "^Please provide a number value for total girls assessed\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls should ask for boys phonics", function (done) {
        var user = {
            current_state: 'perf_learner_girls_total',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: "52"
            }
        };
        var p = tester.check_state({
            user: user,
            content: "42",
            next_state: "perf_learner_boys_phonetic_awareness",
            response: "^How many boys achieved at least 4 out of 6 correct answers " +
                "for Section 1 \\(Phonics and Phonemic Awareness\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering boys phonics incorrectly should ask for total boys phonics again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_phonetic_awareness',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "lots",
            next_state: "perf_learner_boys_phonetic_awareness",
            response: "^Please provide a number value for total boys achieving 4 out of 6 correct answers for Phonics and Phonemic Awareness\\.$"
        });
        p.then(done, done);
    });

    it("entering boys phonics should ask for total girls phonics", function (done) {
        var user = {
            current_state: 'perf_learner_boys_phonetic_awareness',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "31",
            next_state: "perf_learner_girls_phonetic_awareness",
            response: "^How many girls achieved at least 4 out of 6 correct answers " +
                "for Section 1 \\(Phonics and Phonemic Awareness\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering girls phonics incorrectly should ask for total girls phonics again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_phonetic_awareness',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "loads",
            next_state: "perf_learner_girls_phonetic_awareness",
            response: "^Please provide a number value for total girls achieving 4 out of 6 correct answers for Phonics and Phonemic Awareness\\.$"
        });
        p.then(done, done);
    });

    it("entering girls phonics should ask for total boys vocabulary", function (done) {
        var user = {
            current_state: 'perf_learner_girls_phonetic_awareness',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "32",
            next_state: "perf_learner_boys_vocabulary",
            response: "^How many boys achieved at least 3 out of 6 correct " +
                "answers for Section 2 \\(Vocabulary\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys vocabulary incorrectly should ask for total boys vocabulary again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_vocabulary',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "less",
            next_state: "perf_learner_boys_vocabulary",
            response: "^Please provide a number value for total boys achieving 3 out of 6 correct answers for Vocabulary\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys vocabulary should ask for total girls vocabulary", function (done) {
        var user = {
            current_state: 'perf_learner_boys_vocabulary',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "33",
            next_state: "perf_learner_girls_vocabulary",
            response: "^How many girls achieved at least 3 out of 6 correct " +
                "answers for Section 2 \\(Vocabulary\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls vocabulary incorrectly should ask for total girls vocabulary again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_vocabulary',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "lesser",
            next_state: "perf_learner_girls_vocabulary",
            response: "^Please provide a number value for total girls achieving 3 out of 6 correct answers for Vocabulary\\.$"
        });
        p.then(done, done);
    });

    it("entering girls vocabulary should ask for total boys comprehension", function (done) {
        var user = {
            current_state: 'perf_learner_girls_vocabulary',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "34",
            next_state: "perf_learner_boys_reading_comprehension",
            response: "^How many boys achieved at least 2 out of 4 correct answers " +
                "for Section 3 \\(Comprehension\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys comprehension incorrectly should ask for total boys comprehension again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_reading_comprehension',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "lessly",
            next_state: "perf_learner_boys_reading_comprehension",
            response: "^Please provide a number value for total boys achieving 2 out of 4 correct answers for Comprehension\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys comprehension should ask for total girls comprehension", function (done) {
        var user = {
            current_state: 'perf_learner_boys_reading_comprehension',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "35",
            next_state: "perf_learner_girls_reading_comprehension",
            response: "^How many girls achieved at least 2 out of 4 correct answers " +
                "for Section 3 \\(Comprehension\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls comprehension incorrectly should ask for total girls comprehension again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_reading_comprehension',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "lesser",
            next_state: "perf_learner_girls_reading_comprehension",
            response: "^Please provide a number value for total girls achieving 2 out of 4 correct answers for Comprehension\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls comprehension should ask for total boys writing", function (done) {
        var user = {
            current_state: 'perf_learner_girls_reading_comprehension',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "36",
            next_state: "perf_learner_boys_writing_diction",
            response: "^How many boys achieved at least 2 out of 4 correct answers " +
                "for Section 4 \\(Writing\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys writing incorrectly should ask for total boys writing again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_writing_diction',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greater",
            next_state: "perf_learner_boys_writing_diction",
            response: "^Please provide a number value for total boys achieving 2 out of 4 correct answers for Writing\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys writing should ask for total girls writing", function (done) {
        var user = {
            current_state: 'perf_learner_boys_writing_diction',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "37",
            next_state: "perf_learner_girls_writing_diction",
            response: "^How many girls achieved at least 2 out of 4 correct answers " +
                "for Section 4 \\(Writing\\)\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls writing incorrectly should ask for total girls writing again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_writing_diction',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greatest",
            next_state: "perf_learner_girls_writing_diction",
            response: "^Please provide a number value for total girls achieving 2 out of 4 correct answers for Writing\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls comprehension should ask for total boys outstanding results", function (done) {
        var user = {
            current_state: 'perf_learner_girls_writing_diction',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "38",
            next_state: "perf_learner_boys_outstanding_results",
            response: "^In total, how many boys achieved 16 out of 20 or more\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys outstanding results incorrectly should ask for total boys outstanding results again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_outstanding_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greater",
            next_state: "perf_learner_boys_outstanding_results",
            response: "^Please provide a number value for total boys achieving 16 out of 20 or more\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys outstanding results should ask for total girls outstanding results", function (done) {
        var user = {
            current_state: 'perf_learner_boys_outstanding_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "39",
            next_state: "perf_learner_girls_outstanding_results",
            response: "^In total, how many girls achieved 16 out of 20 or more\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls outstanding results incorrectly should ask for total girls outstanding results again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_outstanding_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greatest",
            next_state: "perf_learner_girls_outstanding_results",
            response: "^Please provide a number value for total girls achieving 16 out of 20 or more\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls outstanding results should ask for total boys desirable results", function (done) {
        var user = {
            current_state: 'perf_learner_girls_outstanding_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
            }
        };
        var p = tester.check_state({
            user: user,
            content: "40",
            next_state: "perf_learner_boys_desirable_results",
            response: "^In total, how many boys achieved between 12 and 15 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys desirable results incorrectly should ask for total boys desirable results again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_desirable_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greater",
            next_state: "perf_learner_boys_desirable_results",
            response: "^Please provide a number value for total boys achieving between 12 and 15 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys desirable results should ask for total girls desirable results", function (done) {
        var user = {
            current_state: 'perf_learner_boys_desirable_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
            }
        };
        var p = tester.check_state({
            user: user,
            content: "41",
            next_state: "perf_learner_girls_desirable_results",
            response: "^In total, how many girls achieved between 12 and 15 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls desirable results incorrectly should ask for total girls desirable results again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_desirable_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greatest",
            next_state: "perf_learner_girls_desirable_results",
            response: "^Please provide a number value for total girls achieving between 12 and 15 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls desirable results should ask for total boys minimum results", function (done) {
        var user = {
            current_state: 'perf_learner_girls_desirable_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "42",
            next_state: "perf_learner_boys_minimum_results",
            response: "^In total, how many boys achieved between 8 and 11 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys minimum results incorrectly should ask for total boys minimum results again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42'

            }
        };
        var p = tester.check_state({
            user: user,
            content: "greater",
            next_state: "perf_learner_boys_minimum_results",
            response: "^Please provide a number value for total boys achieving between 8 and 11 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys desirable results should ask for total girls desirable results", function (done) {
        var user = {
            current_state: 'perf_learner_boys_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "43",
            next_state: "perf_learner_girls_minimum_results",
            response: "^In total, how many girls achieved between 8 and 11 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls minimum results incorrectly should ask for total girls minimum results again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greatest",
            next_state: "perf_learner_girls_minimum_results",
            response: "^Please provide a number value for total girls achieving between 8 and 11 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering total girls minimum results should ask for total boys below minimum results", function (done) {
        var user = {
            current_state: 'perf_learner_girls_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "44",
            next_state: "perf_learner_boys_below_minimum_results",
            response: "^In total, how many boys achieved between 0 and 7 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total boys below minimum results incorrectly should ask for total boys below minimum results again", function (done) {
        var user = {
            current_state: 'perf_learner_boys_below_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greatering",
            next_state: "perf_learner_boys_below_minimum_results",
            response: "^Please provide a number value for total boys achieving between 0 and 7 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering total boys below minimum results should ask for total girls below minimum results", function (done) {
        var user = {
            current_state: 'perf_learner_boys_below_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "45",
            next_state: "perf_learner_girls_below_minimum_results",
            response: "^In total, how many girls achieved between 0 and 7 out of 20\\?$"
        });
        p.then(done, done);
    });

    it("entering total girls below minimum results incorrectly should ask for total girls below minimum results again", function (done) {
        var user = {
            current_state: 'perf_learner_girls_below_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44',
                perf_learner_boys_below_minimum_results: '45'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "greating",
            next_state: "perf_learner_girls_below_minimum_results",
            response: "^Please provide a number value for total girls achieving between 0 and 7 out of 20\\.$"
        });
        p.then(done, done);
    });

    it("entering teacher training subtotal should ask show success and options", function (done) {
        var user = {
            current_state: 'perf_learner_girls_below_minimum_results',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44',
                perf_learner_boys_below_minimum_results: '45'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "46",
            next_state: "perf_learner_completed",
            response: "^Congratulations. You have finished reporting on the learner assessment.[^]" +
                "1. Go back to the main menu\\.[^]" +
                "2. Exit\\.$"
        });
        p.then(done, done);
    });
});

describe("When using the USSD line as an recognised MSISDN - completed Learner review", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1,
                    "rts_last_save_performance_teacher": "106",
                    "rts_last_save_performance_learner": "true"
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("selecting to go to main menu should show it", function (done) {
        var user = {
            current_state: 'perf_learner_completed',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44',
                perf_learner_boys_below_minimum_results: '45',
                perf_learner_girls_below_minimum_results: '46'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance\\.[^]" +
                    "3. Change my school\\.[^]" +
                    "4. Update my school’s registration data\\.$"
        });
        p.then(done, done);
    });

    it("selecting to go to exit should thank and close", function (done) {
        var user = {
            current_state: 'perf_learner_completed',
            answers: {
                initial_state: 'perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44',
                perf_learner_boys_below_minimum_results: '45',
                perf_learner_girls_below_minimum_results: '46'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "end_state",
            response: "^Goodbye! Thank you for using the Gateway\\.$",
            continue_session: false
        });
        p.then(done, done);
    });
});


describe("When using the USSD line as a recognised MSISDN to update the school data from the manage_update_school_data state", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_emis": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("it should select display choice to continue update the school registration data", function (done) {
        var user = {
            current_state: 'initial_state'
        };
        var p = tester.check_state({
            user: user,
            content: "4",
            next_state: "manage_update_school_data",
            response: "^You'll now be asked to re-enter key school details to " +
                        "ensure the records are accurate. Enter 1 to continue."
        });
        p.then(done, done);
    });

    it("on continue pressed should redirect to reg_school_boys state", function (done) {
        var user = {
            current_state: 'manage_update_school_data',
            answers: {
                initial_state: 'manage_update_school_data'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_school_boys",
            response: "^How many boys do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("saying are zonal head after association with new school should thank long and close", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'manage_update_school_data',
                reg_school_boys: '100',
                reg_school_girls: '101',
                reg_school_classrooms: '10',
                reg_school_teachers: '15',
                reg_school_teachers_g1: '5',
                reg_school_teachers_g2: '4',
                reg_school_students_g2_boys: '55',
                reg_school_students_g2_girls: '60'

            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "reg_thanks_zonal_head",
            response: "^Well done! You are now registered as a Zonal Head" +
                " Teacher\\. When you are ready, dial in to start" +
                " reporting\\. You will also receive monthly SMS's from" +
                " your zone\\.$",
            continue_session: false
        });
        p.then(done, done);
    });
});

describe("When a district admin is using the USSD line as a recognised MSISDN to add teacher performance data", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_district_official_id_number": 1,
                    "rts_district_official_district_id": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("first display navigation menu", function (done) {
        var p = tester.check_state({
            user: null,
            content: null,
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance.$"
        });
        p.then(done, done);
    });

    it("on selecting to report on teacher perfomance should ask for for EMIS", function (done) {

        var user = {
            current_state: 'initial_state'
        };

        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "add_emis_perf_teacher_ts_number",
            response: "^Please enter the school's EMIS number that you would like to report on. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("on adding correct emis should go on to ask about the teachers TS number", function (done) {

        var user = {
            current_state: 'add_emis_perf_teacher_ts_number',
        };

        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "perf_teacher_ts_number",
            response: "^Please enter the teacher's TS number.$"
        });
        p.then(done, done);
    });

    it("on adding wrong emis should go on to ask for the emis number again", function (done) {

        var user = {
            current_state: 'add_emis_perf_teacher_ts_number',
        };

        var p = tester.check_state({
            user: user,
            content: "7197871",
            next_state: "add_emis_perf_teacher_ts_number",
            response: "^The emis does not exist, please try again. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });
});


describe.only("When a district admin is using the USSD line as a recognised MSISDN to add learner performance data", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_short_code: "1234",
                    cms_api_root: 'http://qa/api/v1/'
                });

                var dummy_contact = {
                    key: "f953710a2472447591bd59e906dc2c26",
                    surname: "Trotter",
                    user_account: "test-0-user",
                    bbm_pin: null,
                    msisdn: "+1234567",
                    created_at: "2013-04-24 14:01:41.803693",
                    gtalk_id: null,
                    dob: null,
                    groups: null,
                    facebook_id: null,
                    twitter_handle: null,
                    email_address: null,
                    name: "Rodney"
                };

                api.add_contact(dummy_contact);
                api.update_contact_extras(dummy_contact, {
                    "rts_id": 2,
                    "rts_district_official_id_number": 1,
                    "rts_district_official_district_id": 1
                });

                fixtures.forEach(function (f) {
                    api.load_http_fixture(f);
                });
            },
            async: true
        });
    });

    it("first display navigation menu", function (done) {
        var p = tester.check_state({
            user: null,
            content: null,
            next_state: "initial_state",
            response: "^What would you like to do\\?[^]" +
                    "1. Report on teacher performance\\.[^]" +
                    "2. Report on learner performance.$"
        });
        p.then(done, done);
    });

    it("on selecting to report on learner perfomance should ask for for EMIS", function (done) {

        var user = {
            current_state: 'initial_state'
        };

        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "add_emis_perf_learner_boys_total",
            response: "^Please enter the school's EMIS number that you would like to report on. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("on adding correct emis should go on to ask about the teachers TS number", function (done) {

        var user = {
            current_state: 'add_emis_perf_learner_boys_total',
        };

        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "perf_learner_boys_total",
            response: "^How many boys took part in the learner assessment\\?$"
        });
        p.then(done, done);
    });

    it("on adding wrong emis should go on to ask for the emis number again", function (done) {

        var user = {
            current_state: 'add_emis_perf_learner_boys_total',
            answers : {
                initial_state: "add_emis_perf_learner_boys_total"
            }
        };

        var p = tester.check_state({
            user: user,
            content: "7197871",
            next_state: "add_emis_perf_learner_boys_total",
            response: "^The emis does not exist, please try again. This should have 4-6 digits e.g 4351.$"
        });
        p.then(done, done);
    });

    it("selecting to go to exit should thank and close", function (done) {
        // Should go straight to the end state of the system
        var user = {
            current_state: 'perf_learner_completed',
            answers: {
                initial_state: 'add_emis_perf_learner_boys_total',
                perf_learner_boys_total: '52',
                perf_learner_girls_total: '42',
                perf_learner_boys_phonetic_awareness: '31',
                perf_learner_girls_phonetic_awareness: '32',
                perf_learner_boys_vocabulary: '33',
                perf_learner_girls_vocabulary: '34',
                perf_learner_boys_reading_comprehension: '35',
                perf_learner_girls_reading_comprehension: '36',
                perf_learner_boys_writing_diction: '37',
                perf_learner_girls_writing_diction: '38',
                perf_learner_boys_outstanding_results: '39',
                perf_learner_girls_outstanding_results: '40',
                perf_learner_boys_desirable_results: '41',
                perf_learner_girls_desirable_results: '42',
                perf_learner_boys_minimum_results: '43',
                perf_learner_girls_minimum_results: '44',
                perf_learner_boys_below_minimum_results: '45',
                perf_learner_girls_below_minimum_results: '46'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "end_state",
            response: "^Goodbye! Thank you for using the Gateway\\.$",
            continue_session: false
        });
        p.then(done, done);
    });
});
