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
    'test/fixtures/post_registration.json',
    'test/fixtures/post_registration_zonalhead.json',
    'test/fixtures/get_hierarchy.json',
    'test/fixtures/post_registration_update_msisdn.json',
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
                    cms_api_root: 'http://qa/api/'
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
            state_creator.check_and_parse_date('11 09 1980').toISOString(),
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
            response: "^Welcome to the Gateway! What would you like to do\\?[^]" +
                    "1. Register as a new user[^]" +
                    "2. Change my school[^]" +
                    "3. Change my primary mobile number$"
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
            response: "^What is your school EMIS number\\?$"
        });
        p.then(done, done);
    });

    it("entering valid EMIS should ask for School Name", function (done) {
        var user = {
            current_state: 'reg_emis',
            answers: {
                initial_state: 'reg_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "0001",
            next_state: "reg_school_name",
            response: "^What is your school name\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid EMIS should ask for reenter or exit", function (done) {
        var user = {
            current_state: 'reg_emis',
            answers: {
                initial_state: 'reg_emis'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "000A",
            next_state: "reg_emis_error",
            response: "^Sorry![^]That is not a EMIS we recognise. Make sure " +
                "you have entered the number correctly.[^]" +
                "1. Try again[^]" +
                "2. Exit$"
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
            response: "^There seems to be a problem with the EMIS number. " +
                "Please send a SMS with the code EMIS ERROR to 1234 " +
                "and your district officer will be in touch.$",
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
            next_state: "reg_emis",
            response: "^What is your school EMIS number\\?$"
        });
        p.then(done, done);
    });

    it("entering School Name should ask for users name", function (done) {
        var user = {
            current_state: 'reg_school_name',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "School One",
            next_state: "reg_first_name",
            response: "^What is your name\\?$"
        });
        p.then(done, done);
    });

    it("entering name should ask for users surname", function (done) {
        var user = {
            current_state: 'reg_first_name',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Jack",
            next_state: "reg_surname",
            response: "^What is your surname\\?$"
        });
        p.then(done, done);
    });

    it("entering suname should ask for users date of birth", function (done) {
        var user = {
            current_state: 'reg_surname',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "Black",
            next_state: "reg_date_of_birth",
            response: "^What is your date of birth\\? \\(example 21 07 1980\\)$"
        });
        p.then(done, done);
    });

    it("entering valid date of birth should ask for users gender", function (done) {
        var user = {
            current_state: 'reg_date_of_birth',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "11 09 1980",
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
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "11 Sep 1980",
            next_state: "reg_date_of_birth",
            response: "^Please enter your date of birth formatted DD MM YYYY$"
        });
        p.then(done, done);
    });

    it("entering gender should ask for school classrooms number", function (done) {
        var user = {
            current_state: 'reg_gender',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_classrooms",
            response: "^How many classrooms do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("entering school classrooms should ask for teachers number", function (done) {
        var user = {
            current_state: 'reg_school_classrooms',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "reg_school_teachers",
            response: "^How many teachers in total do you have in your school\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid school classrooms number should error", function (done) {
        var user = {
            current_state: 'reg_school_classrooms',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "five",
            next_state: "reg_school_classrooms",
            response: "^Please provide a number value for how many classrooms you have in your school$"
        });
        p.then(done, done);
    });

    it("entering teachers number should ask for G1 teachers number", function (done) {
        var user = {
            current_state: 'reg_school_teachers',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "5",
            next_state: "reg_school_teachers_g1",
            response: "^How many teachers teach G1 local language literacy\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "five",
            next_state: "reg_school_teachers",
            response: "^Please provide a number value for how many teachers in total do you have in your school$"
        });
        p.then(done, done);
    });

    it("entering teachers G1 number should ask for G2 teachers number", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g1',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5',
                reg_school_teachers: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_teachers_g2",
            response: "^How many teachers teach G2 local language literacy\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers G1 number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g1',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5',
                reg_school_teachers: '5'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "two",
            next_state: "reg_school_teachers_g1",
            response: "^Please provide a number value for how many teachers teach G1 local language literacy$"
        });
        p.then(done, done);
    });

    it("entering teachers G2 number should ask for G2 boys number", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g2',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "2",
            next_state: "reg_school_students_g2_boys",
            response: "^Total number of G2 boys registered/enrolled\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid teachers G2 number should error", function (done) {
        var user = {
            current_state: 'reg_school_teachers_g2',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
                reg_school_classrooms: '5',
                reg_school_teachers: '5',
                reg_school_teachers_g1: '2'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "two",
            next_state: "reg_school_teachers_g2",
            response: "^Please provide a number value for how many teachers teach G2 local language literacy$"
        });
        p.then(done, done);
    });

    it("entering student boys G2 number should ask for G2 girls number", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Total number of G2 girls registered/enrolled\\?$"
        });
        p.then(done, done);
    });

    it("entering invalid student boys G2 number should error", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_boys',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Please provide a number value for total number of G2 boys registered/enrolled$"
        });
        p.then(done, done);
    });

    it("entering student girls G2 number should ask for zonal head", function (done) {
        var user = {
            current_state: 'reg_school_students_g2_girls',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Are you a Zonal Head\\?[^]" +
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
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Please provide a number value for total number of G2 girls registered/enrolled$"
        });
        p.then(done, done);
    });

    it("saying not zonal head should ask for zonal head name", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^What is the name and surname of your Zonal Head\\?$"
        });
        p.then(done, done);
    });

    it("saying are zonal head should thank long and close", function (done) {
        var user = {
            current_state: 'reg_zonal_head',
            answers: {
                initial_state: 'reg_emis',
                reg_emis: '0001',
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Thank you for registering! When you are ready you can " +
            "dial in again to start reporting. You will also start receiving the " +
            "monthly SMS's from your Headteachers.$",
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
                reg_school_name: 'School One',
                reg_first_name: 'Jack',
                reg_surname: 'Black',
                reg_date_of_birth: '11-Sep-1980',
                reg_gender: 'male',
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
            response: "^Thank you for registering! When you are ready you can dial " +
            "in again to start reporting.$",
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
            next_state: "manage_change_msisdn_emis_lookup",
            response: "^What is your school EMIS number\\?$"
        });
        p.then(done, done);
    });

    it("entering valid EMIS should thank the user and exit", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis_lookup',
            answers: {
                initial_state: 'manage_change_msisdn_emis_lookup'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "0001",
            next_state: "manage_change_msisdn_confirm",
            response: "^Thank you! We have now allocated your new contact mobile number " +
            "to your current school.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering invalid EMIS should ask for reenter or exit", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis_lookup',
            answers: {
                initial_state: 'manage_change_msisdn_emis_lookup'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "000A",
            next_state: "manage_change_msisdn_emis_error",
            response: "^Sorry![^]That is not a EMIS we recognise. Make sure " +
                "you have entered the number correctly.[^]" +
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
            response: "^There seems to be a problem with the EMIS number. " +
                "Please send a SMS with the code EMIS ERROR to 1234 " +
                "and your district officer will be in touch.$",
            continue_session: false
        });
        p.then(done, done);
    });

    it("entering invalid EMIS and choosing to reenter should ask EMIS", function (done) {
        var user = {
            current_state: 'manage_change_msisdn_emis_error',
            answers: {
                initial_state: 'manage_change_msisdn_emis_lookup',
                manage_change_msisdn_emis_lookup: '000A'
            }
        };
        var p = tester.check_state({
            user: user,
            content: "1",
            next_state: "manage_change_msisdn_emis_lookup",
            response: "^What is your school EMIS number\\?$"
        });
        p.then(done, done);
    });

});

