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

describe("When using the USSD line as an unrecognised MSISDN", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = [
    ];

    var tester = new vumigo.test_utils.ImTester(app.api, {
        custom_setup: function (api) {
            api.config_store.config = JSON.stringify({
                sms_short_code: "1234"
            });
            fixtures.forEach(function (f) {
                api.load_http_fixture(f);
            });
        },
        async: true
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

});

