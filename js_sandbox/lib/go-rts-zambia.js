var vumigo = require("vumigo_v01");
var jed = require("jed");

if (typeof api === "undefined") {
    // testing hook (supplies api when it is not passed in by the real sandbox)
    var api = this.api = new vumigo.dummy_api.DummyApi();
}

var Promise = vumigo.promise.Promise;
var success = vumigo.promise.success;
var Choice = vumigo.states.Choice;
var ChoiceState = vumigo.states.ChoiceState;
var FreeText = vumigo.states.FreeText;
var EndState = vumigo.states.EndState;
var InteractionMachine = vumigo.state_machine.InteractionMachine;
var StateCreator = vumigo.state_machine.StateCreator;

function GoRtsZambiaError(msg) {
    var self = this;
    self.msg = msg;

    self.toString = function() {
        return "<GoRtsZambiaError: " + self.msg + ">";
    };
}

function GoRtsZambia() {
    var self = this;

    self.post_headers = {
        'Content-Type': ['application/x-www-form-urlencoded']
    };

    // The first state to enter
    StateCreator.call(self, 'initial_state');

    // START Shared helpers

    self.cms_get = function(path) {
        var url = im.config.cms_api_root + path + "?format=json";
        var p = im.api_request("http.get", {
            url: url,
            headers: self.headers
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'GET', null, false);
            return json;
        });
        return p;
    };

    self.cms_post = function(path, data) {
        var url = im.config.cms_api_root + path + "?format=json";
        data = self.url_encode(data);
        var p = im.api_request("http.post", {
            url: url,
            headers: self.post_headers,
            data: data
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'POST', data, false);
            return json;
        });
        return p;
    };

    self.url_encode = function(params) {
        var items = [];
        for (var key in params) {
            items[items.length] = (encodeURIComponent(key) + '=' +
                                   encodeURIComponent(params[key]));
        }
        return items.join('&');
    };

    self.check_reply = function(reply, url, method, data, ignore_error) {
        var error;
        if (reply.success && (reply.code >= 200 && reply.code < 300))  {
            if (reply.body) {
                var json = JSON.parse(reply.body);
                return json;
            } else {
                return null;
            }
        }
        else {
            error = reply.reason;
        }
        var error_msg = ("API " + method + " to " + url + " failed: " +
                         error);
        if (typeof data != 'undefined') {
            error_msg = error_msg + '; data: ' + JSON.stringify(data);
        }

        im.log(error_msg);
        if (!ignore_error) {
            throw new GoRtsZambiaError(error_msg);
        }
    };

    self.array_parse_ints = function(target){
        // returns false if fails to parse
        for (var i = 0; i < target.length; i++) {
            target[i] = parseInt(target[i],10);
            if (isNaN(target[i])) return false;
        }
        return target;
    };

    self.check_and_parse_date = function(date_string){
        // an opinionated data parser - expects "DD MM YYYY"
        // returns false if fails to parse
        var da = self.array_parse_ints(date_string.split(" "));
        if (da && da[0]<=31 && da[1] <= 12){
            da[1] = da[1]-1; // JS dates are 0-bound
            return new Date(da[2], da[1], da[0]);
        } else {
            return false;
        }
    };

    self.check_valid_emis = function(emis){
        // returns false if fails to find
        var numbers_only = new RegExp('^\\d+$');
        if (numbers_only.test(emis)){
            return im.config.array_emis.indexOf(parseInt(emis)) != -1;
        } else {
            return false;
        }        
    };

    // END Shared helpers

    // START CMS Interactions

    self.cms_registration = function(im) {
        var data = {
            emis: parseInt(im.get_user_answer('reg_emis')),
            school_name: im.get_user_answer('reg_school_name'),
            first_name: im.get_user_answer('reg_first_name'),
            surname: im.get_user_answer('reg_surname'),
            date_of_birth: im.get_user_answer('reg_date_of_birth'),
            gender: im.get_user_answer('reg_gender'),
            school_classrooms: parseInt(im.get_user_answer('reg_school_classrooms')),
            school_teachers: parseInt(im.get_user_answer('reg_school_teachers')),
            school_teachers_g1: parseInt(im.get_user_answer('reg_school_teachers_g1')),
            school_teachers_g2: parseInt(im.get_user_answer('reg_school_teachers_g2')),
            school_students_g2_boys: parseInt(im.get_user_answer('reg_school_students_g2_boys')),
            school_students_g2_girls: parseInt(im.get_user_answer('reg_school_students_g2_girls'))
        };
        if (im.get_user_answer('reg_zonal_head') == "reg_zonal_head_name") {
            data['zonal_head_name'] = im.get_user_answer('reg_zonal_head_name');
            data['zonal_head_self'] = false;
        } else {
            data['zonal_head_name'] = "self";
            data['zonal_head_self'] = true;
        }

        return self.cms_post("registration/", data);
    };

    self.cms_registration_update_msisdn = function(im) {
        var data = {
            emis: parseInt(im.get_user_answer('manage_change_msisdn_emis_lookup')),
            msisdn: im.user_addr
        };
        return self.cms_post("registration/msisdn/", data);
    };

    self.cms_hierarchy_load = function() {
        var p = self.cms_get("hierarchy/");
        p.add_callback(function(result){
            var array_emis = []
            for (var i=0;i<result.objects.length;i++){
                array_emis.push(result.objects[i].EMIS);
            }
            im.config.array_emis = array_emis;
        });
        return p;
    };

    // END CMS Interactions

    // START Shared creators

    self.error_state = function() {
        return new EndState(
            "end_state_error",
            "Sorry! Something went wrong. Please redial and try again.",
            "initial_state"
        );
    };

    self.make_emis_error_state = function(state_name, retry_state) {
        return new ChoiceState(
            state_name,
            function(choice) {
                return choice.value;
            },
            "Sorry!\nThat is not a EMIS we recognise. Make sure you have " +
            "entered the number correctly.",
            [
                new Choice(retry_state, "Try again"),
                new Choice("reg_exit_emis", "Exit")
            ]
        );
    };

    self.make_bad_data_state = function(state_name, next_state, expecting) {
        return new ChoiceState(
            state_name,
            next_state,
            "Sorry!\nThe information you entered is not what we were expecting.\n" +
            "We were expecting " + expecting,
            [
                new Choice("back", "Try again")
            ]
        );
    };

    // END Shared creators

    self.add_creator('initial_state', function(state_name, im) {
        return new ChoiceState(
            state_name,
            function(choice) {
                return choice.value;
            },
            "Welcome to the Gateway! What would you like to do?",
            [
                new Choice("reg_emis", "Register as a new user"),
                new Choice("manage_change_emis", "Change my school"),
                new Choice("manage_change_msisdn_emis_lookup", "Change my primary mobile number")
            ]
        );
    });

    self.add_state(new FreeText(
        "reg_emis",
        "reg_school_name",
        "What is your school EMIS number?"
    ));

    self.add_state(new FreeText(
        "manage_change_msisdn_emis_lookup",
        "manage_change_msisdn_confirm",
        "What is your school EMIS number?"
    ));

    self.add_creator('manage_change_msisdn_confirm', function(state_name, im) {
        var EMIS = im.get_user_answer('manage_change_msisdn_emis_lookup');
        if (self.check_valid_emis(EMIS)) {
            // EMIS valid
            return new EndState(
                state_name,
                "Thank you! We have now allocated your new contact mobile number " +
                "to your current school.",
                "initial_state",
                {
                    on_enter: function() {
                        var p = self.cms_registration_update_msisdn(im);
                        return p;
                    }
                }
            );
        } else {
            // Invalid EMIS - request again
            return self.make_emis_error_state('manage_change_msisdn_emis_error',
                'manage_change_msisdn_emis_lookup');
        }
    });

    self.add_state(self.make_emis_error_state('manage_change_msisdn_emis_error',
        'manage_change_msisdn_emis_lookup'));

    self.add_creator('reg_school_name', function(state_name, im) {
        var EMIS = im.get_user_answer('reg_emis');
        // TODO: Validate EMIS properly
        if (self.check_valid_emis(EMIS)) {
            // EMIS valid
            return new FreeText(
                state_name,
                "reg_first_name",
                "What is your school name?"
            );
        } else {
            // Invalid EMIS - request again
            return self.make_emis_error_state('reg_emis_error', 'reg_emis');
        }
    });

    self.add_state(self.make_emis_error_state('reg_emis_error', 'reg_emis'));

    

    self.add_creator('reg_exit_emis', function(state_name, im) {
        return new EndState(
            state_name,
            "There seems to be a problem with the EMIS number. Please send a SMS " +
            "with the code EMIS ERROR to " + im.config.sms_short_code + " " +
            "and your district officer will be in touch.",
            "initial_state"
        );
    });

    self.add_state(new FreeText(
        "reg_first_name",
        "reg_surname",
        "What is your name?"
    ));

    self.add_state(new FreeText(
        "reg_surname",
        "reg_date_of_birth",
        "What is your surname?"
    ));

    self.add_state(new FreeText(
        "reg_date_of_birth",
        "reg_gender",
        "What is your date of birth? (example 21 07 1980)",
        function(content) {
            // check that the value provided is date format we expect
            return self.check_and_parse_date(content);
        },
        "Please enter your date of birth formatted DD MM YYYY"
    ));

    self.add_state(new ChoiceState(
        'reg_gender',
        'reg_school_classrooms',
        "What is your gender?",
        [
            new Choice("female", "Female"),
            new Choice("male", "Male")
        ]
    ));

    self.add_state(new FreeText(
        "reg_school_classrooms",
        "reg_school_teachers",
        "How many classrooms do you have in your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for how many classrooms you have in your school'
    ));


    self.add_state(new FreeText(
        "reg_school_teachers",
        "reg_school_teachers_g1",
        "How many teachers in total do you have in your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for how many teachers in total do you have in your school'
    ));

    self.add_state(new FreeText(
        "reg_school_teachers_g1",
        "reg_school_teachers_g2",
        "How many teachers teach G1 local language literacy?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for how many teachers teach G1 local language literacy'
    ));

    self.add_state(new FreeText(
        "reg_school_teachers_g2",
        "reg_school_students_g2_boys",
        "How many teachers teach G2 local language literacy?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for how many teachers teach G2 local language literacy'
    ));

    self.add_state(new FreeText(
        "reg_school_students_g2_boys",
        "reg_school_students_g2_girls",
        "Total number of G2 boys registered/enrolled?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for total number of G2 boys registered/enrolled'
    ));

    self.add_state(new FreeText(
        "reg_school_students_g2_girls",
        "reg_zonal_head",
        "Total number of G2 girls registered/enrolled?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return !Number.isNaN(parseInt(content));
        },
        'Please provide a number value for total number of G2 girls registered/enrolled'
    ));

    self.add_state(new ChoiceState(
        'reg_zonal_head',
        function(choice) {
            return choice.value;
        },
        "Are you a Zonal Head?",
        [
            new Choice("reg_thanks_zonal_head", "Yes"),
            new Choice("reg_zonal_head_name", "No")
        ]
    ));

    self.add_state(new FreeText(
        "reg_zonal_head_name",
        "reg_thanks_head_teacher",
        "What is the name and surname of your Zonal Head?"
    ));

    self.add_creator('reg_thanks_head_teacher', function(state_name, im) {
        // Log the users data
        var p = self.cms_registration(im);
        // Generate the EndState
        p.add_callback(function(result) {
            return new EndState(
                state_name,
                "Thank you for registering! When you are ready you can dial in again " +
                "to start reporting.",
                "initial_state"
            );
        });
        return p;
    });

    self.add_creator('reg_thanks_zonal_head', function(state_name, im) {
        // Log the users data
        var p = self.cms_registration(im);
        // Generate the EndState
        p.add_callback(function(result) {
            return new EndState(
                state_name,
                "Thank you for registering! When you are ready you can dial in again " +
                "to start reporting. You will also start receiving the monthly SMS's " +
                "from your Headteachers.",
                "initial_state"
            );
        });
        return p;
    });

    self.add_state(new EndState(
        "end_state",
        "Thank you and bye bye!",
        "initial_state"
    ));

    self.on_config_read = function(event){
        // Run calls out to the APIs to load dynamic states
        return self.cms_hierarchy_load();
    };
}

// launch app
var states = new GoRtsZambia();
var im = new InteractionMachine(api, states);
im.attach();
 
