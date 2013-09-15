var fs = require("fs");
var assert = require("assert");
var vumigo = require("vumigo_v01");
var app = require("../lib/go-rts-zambia-sms");

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
];

var tester;

describe("When using the SMS line as an unrecognised MSISDN", function() {

    // These are used to mock API reponses
    // EXAMPLE: Response from google maps API
    var fixtures = test_fixtures_full;
    beforeEach(function() {
        tester = new vumigo.test_utils.ImTester(app.api, {
            custom_setup: function (api) {
                api.config_store.config = JSON.stringify({
                    sms_tag: ['pool', 'addr'],
                    ussd_line: "*120*888#",
                    cms_api_root: 'http://qa/api/v1/',
                    output: {
                        not_registered: "Sorry, we don't recognise your number. This SMS line " +
                            "is for Zambian Headteachers only. Headteachers, please register " +
                            "your number first. Dial *120*888#",
                        thanks: "Thanks! Bye!"
                    }
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

    it.only("reject with message", function (done) {
        var p = tester.check_state({
            user: null,
            content: 'Hi everyone!',
            next_state: "initial_state",
            response: "^Sorry, we don't recognise your number. This SMS line " +
                "is for Zambian Headteachers only. Headteachers, please register " +
                "your number first. Dial \\*120\\*888\\#$",
            continue_session: false
        });
        p.then(done, done);
    });

 
});
