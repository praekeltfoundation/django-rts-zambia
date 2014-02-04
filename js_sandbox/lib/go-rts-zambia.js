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
var PaginatedChoiceState = vumigo.states.PaginatedChoiceState;
var FreeText = vumigo.states.FreeText;
var EndState = vumigo.states.EndState;
var InteractionMachine = vumigo.state_machine.InteractionMachine;
var StateCreator = vumigo.state_machine.StateCreator;
var JsonApi = vumigo.http_api.JsonApi;

Date.prototype.yyyymmdd = function() {
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
};

function GoRtsZambiaError(msg) {
    var self = this;
    self.msg = msg;

    self.toString = function() {
        return "<GoRtsZambiaError: " + self.msg + ">";
    };
}

function GoRtsZambia() {
    var self = this;

    self.headers = {
        'Content-Type': ['application/json']
    };

    // The first state to enter
    StateCreator.call(self, 'initial_state');

    // START Shared helpers

    self.log_result = function() {
        return function (result) {
            var p = im.log('Got result ' + JSON.stringify(result));
            p.add_callback(function() { return result; });
            return p;
        };
    };

    self.cms_get = function(path) {
        var json_api = new JsonApi(im);
        var url = im.config.cms_api_root + path;
        return json_api.get(url);
    };

    self.cms_post = function(path, data) {
        var json_api = new JsonApi(im);
        var url = im.config.cms_api_root + path;
        return json_api.post(url, {data: data, headers: self.headers});
    };

    self.cms_put = function(path, data) {
        var json_api = new JsonApi(im);
        var url = im.config.cms_api_root + path;
        return json_api.put(url, {data: data, headers: self.headers});
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
        // an opinionated data parser - expects "DDMMYYYY"
        // returns false if fails to parse
        if (date_string.length != 8) return false;
        var da = [date_string.slice(0,2)];
        da.push(date_string.slice(2,4));
        da.push(date_string.slice(4));
        da = self.array_parse_ints(da);
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

    self.check_valid_number = function(input){
        // an attempt to solve the insanity or JavaScript numbers
        var numbers_only = new RegExp('^\\d+$');
        if (input !== '' && numbers_only.test(input) && !Number.isNaN(Number(input))){
            return true;
        } else {
            return false;
        }
    };

    self.registration_data_school_collect = function(){
        var school_data = {
            "name": im.get_user_answer('reg_school_name'),
            "classrooms": parseInt(im.get_user_answer('reg_school_classrooms')),
            "teachers": parseInt(im.get_user_answer('reg_school_teachers')),
            "teachers_g1": parseInt(im.get_user_answer('reg_school_teachers_g1')),
            "teachers_g2": parseInt(im.get_user_answer('reg_school_teachers_g2')),
            "boys_g2": parseInt(im.get_user_answer('reg_school_students_g2_boys')),
            "girls_g2": parseInt(im.get_user_answer('reg_school_students_g2_girls')),
            "boys": parseInt(im.get_user_answer('reg_school_boys')),
            "girls": parseInt(im.get_user_answer('reg_school_girls'))
        };

        return school_data;
    };

    self.registration_data_headteacher_collect = function(){
        var headteacher_data = {
            "first_name": im.get_user_answer('reg_first_name'),
            "last_name": im.get_user_answer('reg_surname'),
            "msisdn": im.user_addr,
            "date_of_birth": self.check_and_parse_date(im.get_user_answer('reg_date_of_birth')).yyyymmdd(),
            "gender": im.get_user_answer('reg_gender'),
            "emis": "/api/v1/school/emis/" + parseInt(im.get_user_answer('reg_emis_validator')) + "/"
        };
        if (im.get_user_answer('reg_zonal_head') == "reg_zonal_head_name") {
            headteacher_data['zonal_head_name'] = im.get_user_answer('reg_zonal_head_name');
            headteacher_data['is_zonal_head'] = false;
        } else {
            headteacher_data['zonal_head_name'] = "self";
            headteacher_data['is_zonal_head'] = true;
        }
        return headteacher_data;
    };

    self.registration_district_admin_collect = function(){
        var district_admin_data = {
            "first_name": im.get_user_answer("reg_district_official_first_name"),
            "last_name": im.get_user_answer("reg_district_official_surname"),
            "date_of_birth": self.check_and_parse_date(im.get_user_answer('reg_district_official_dob')).yyyymmdd(),
            "district": "/api/v1/district/" + im.get_user_answer("reg_district_official") +"/",
            "id_number": im.get_user_answer("reg_district_official_id_number")
        };
        return district_admin_data;
    };


    self.performance_data_teacher_collect = function(emis, id){
        var data = {
            "ts_number": im.get_user_answer('perf_teacher_ts_number'),
            "gender": im.get_user_answer('perf_teacher_gender'),
            "age": im.get_user_answer('perf_teacher_age'),
            "years_experience": im.get_user_answer('perf_teacher_years_experience'),
            "g2_pupils_present": im.get_user_answer('perf_teacher_g2_pupils_present'),
            "g2_pupils_registered": im.get_user_answer('perf_teacher_g2_pupils_registered'),
            "classroom_environment_score": im.get_user_answer('perf_teacher_classroom_environment_score'),
            "t_l_materials": im.get_user_answer('perf_teacher_t_l_materials'),
            "pupils_materials_score": im.get_user_answer('perf_teacher_pupils_materials_score'),
            "pupils_books_number": im.get_user_answer('perf_teacher_pupils_books_number'),
            "reading_lesson": im.get_user_answer('perf_teacher_reading_lesson'),
            "pupil_engagement_score": im.get_user_answer('perf_teacher_pupil_engagement_score'),
            "attitudes_and_beliefs": im.get_user_answer('perf_teacher_attitudes_and_beliefs'),
            "training_subtotal": im.get_user_answer('perf_teacher_training_subtotal'),
            "academic_level": "/api/v1/data/achievement/" + im.get_user_answer('perf_teacher_academic_level') + "/",
            "reading_assessment": im.get_user_answer('perf_teacher_reading_assessment'),
            "reading_total": im.get_user_answer('perf_teacher_reading_total'),
            "emis": "/api/v1/school/emis/" + emis + "/",
            "created_by": "/api/v1/data/headteacher/" + id + "/"
        };

        return data;
    };

    self.performance_data_learner_collect = function(emis, id){
        var data_boys = {
            "gender": "boys",
            "total_number_pupils": im.get_user_answer('perf_learner_boys_total'),
            "phonetic_awareness": im.get_user_answer('perf_learner_boys_phonetic_awareness'),
            "vocabulary": im.get_user_answer('perf_learner_boys_vocabulary'),
            "reading_comprehension": im.get_user_answer('perf_learner_boys_reading_comprehension'),
            "writing_diction": im.get_user_answer('perf_learner_boys_writing_diction'),
            "outstanding_results": im.get_user_answer('perf_learner_boys_outstanding_results'),
            "desirable_results": im.get_user_answer('perf_learner_boys_desirable_results'),
            "minimum_results": im.get_user_answer('perf_learner_boys_minimum_results'),
            "below_minimum_results": im.get_user_answer('perf_learner_boys_below_minimum_results'),
            "emis": "/api/v1/school/emis/" + emis + "/",
            "created_by": "/api/v1/data/headteacher/" + id + "/"
        };

        var data_girls = {
            "gender": "girls",
            "total_number_pupils": im.get_user_answer('perf_learner_girls_total'),
            "phonetic_awareness": im.get_user_answer('perf_learner_girls_phonetic_awareness'),
            "vocabulary": im.get_user_answer('perf_learner_girls_vocabulary'),
            "reading_comprehension": im.get_user_answer('perf_learner_girls_reading_comprehension'),
            "writing_diction": im.get_user_answer('perf_learner_girls_writing_diction'),
            "outstanding_results": im.get_user_answer('perf_learner_girls_outstanding_results'),
            "desirable_results": im.get_user_answer('perf_learner_girls_desirable_results'),
            "minimum_results": im.get_user_answer('perf_learner_girls_minimum_results'),
            "below_minimum_results": im.get_user_answer('perf_learner_girls_below_minimum_results'),
            "emis": "/api/v1/school/emis/" + emis + "/",
            "created_by": "/api/v1/data/headteacher/" + id + "/"
        };

        return [data_boys, data_girls];
    };

    self.get_contact = function(im){
        var p = im.api_request('contacts.get_or_create', {
            delivery_class: 'ussd',
            addr: im.user_addr
        });
        return p;
    };

    self.clear_contact_extra = function(extra){
        var fields = {};
        fields[extra] = "";
        var p = self.get_contact(im);
        p.add_callback(function(result) {
            return im.api_request('contacts.update_extras', {
                key: result.contact.key,
                fields: fields
            });
        });
        return p;
    };

    // END Shared helpers

    // START CMS Interactions

    self.cms_registration = function(im) {
        var headteacher_data;
        var headteacher_id;

        // get the contact
        var p_c = self.get_contact(im);
        p_c.add_callback(function(result) {
            var contact = result.contact;
            var p_ht;
            if (im.get_user_answer('initial_state') == 'manage_change_emis') {
                // Update current headteacher EMIS only
                headteacher_id = contact['extras-rts_id'];
                headteacher_data = {
                    emis: "/api/v1/school/emis/" + parseInt(im.get_user_answer('manage_change_emis_validator')) + "/"
                };
                p_ht = self.cms_put("data/headteacher/" + headteacher_id + "/", headteacher_data);

            } else if (im.get_user_answer('initial_state') == 'manage_update_school_data') {
                var p = self.get_contact(im);
                p_ht = self.cms_get("data/headteacher/?emis__emis=" + contact["extras-rts_emis"]);
            } else {
                // create new headteacher
                headteacher_data = self.registration_data_headteacher_collect();
                p_ht = self.cms_post("data/headteacher/", headteacher_data);
            }
            // Use the results
            p_ht.add_callback(function(result){
                headteacher_id = result.id;
                var emis = result.emis.emis;
                var school_data = self.registration_data_school_collect();
                school_data["created_by"] = "/api/v1/data/headteacher/" + headteacher_id + "/";
                school_data["emis"] = "/api/v1/school/emis/" + emis + "/";
                var p_school = self.cms_post("data/school/", school_data);
                p_school.add_callback(function(){
                    var fields = {
                        "rts_id": JSON.stringify(headteacher_id),
                        "rts_emis": JSON.stringify(emis)
                    };
                    var p_extra = im.api_request('contacts.update_extras', {
                        key: contact.key,
                        fields: fields
                    });
                    p_extra.add_callback(function(result) {
                        if (result.success === true){
                            var contact = result.contact;
                            contact['name'] = im.get_user_answer('reg_first_name');
                            contact['surname'] = im.get_user_answer('reg_surname');
                            return im.api_request('contacts.update', {
                                key: result.contact.key,
                                fields: contact
                            });
                        } else {
                            var p_log = im.log(result);
                            return p_log;
                        }
                    });
                    return p_extra;
                });
                return p_school;
            });
            return p_ht;
        });
        return p_c;
    };

    self.cms_district_admin_registration = function(im){
        var district_admin_data = self.registration_district_admin_collect();
        return self.cms_post("district_admin/", district_admin_data)
    };

    self.cms_registration_update_msisdn = function(im) {
        var emis = parseInt(im.get_user_answer('manage_change_msisdn_emis'));
        var p = self.cms_get("data/headteacher/?emis__emis=" + emis);
        p.add_callback(function(result){
            var headteacher_id = result.id;
            var data = {
                msisdn: im.user_addr
            };
            return self.cms_put("data/headteacher/" + headteacher_id + "/", data);
        });
        return p;
    };

    self.cms_hierarchy_load = function() {
        var p = self.cms_get("hierarchy/");
        p.add_callback(function(result){
            var array_emis = []
            for (var i=0;i<result.objects.length;i++){
                array_emis.push(result.objects[i].emis);
            }
            im.config.array_emis = array_emis;
        });
        return p;
    };

    self.cms_district_load = function () {
        var p = self.cms_get("district/");
        p.add_callback(function(result){
            var districts_json = result.objects;
            im.config.districts_json = districts_json;
        });
        return p;
    };

    self.cms_performance_teacher = function(im) {
        var p = self.get_contact(im);
        p.add_callback(function(result) {
            var emis = parseInt(result.contact["extras-rts_emis"]);
            var id = parseInt(result.contact["extras-rts_id"]);
            // Need to ensure no double save
            var contact_key = result.contact.key;
            if (parseInt(result.contact["extras-rts_last_save_performance_teacher"]) != parseInt(im.get_user_answer('perf_teacher_ts_number'))) {
                var data = self.performance_data_teacher_collect(emis, id);
                var p_tp = self.cms_post("data/teacherperformance/", data);

                p_tp.add_callback(function(contact_key) {
                    return im.api_request('contacts.update_extras', {
                        key: result.contact.key,
                        fields: {
                            "rts_last_save_performance_teacher": JSON.stringify(im.get_user_answer('perf_teacher_ts_number'))
                        }
                    });
                });
                return p_tp;
            }
        });
        return p;
    };

    self.cms_performance_learner = function(im) {
        var p = self.get_contact(im);
        p.add_callback(function(result) {
            var emis = result.contact["extras-rts_emis"];
            var id = result.contact["extras-rts_id"];
            var data = self.performance_data_learner_collect(emis, id);
            var data_boys = data[0];
            var data_girls = data[1];
            // Need to ensure no double save
            var contact_key = result.contact.key;
            if (result.contact["extras-rts_last_save_performance_learner"] != 'true') {
                var p_lp_boys = self.cms_post("data/learnerperformance/", data_boys);
                p_lp_boys.add_callback(function(){
                    var p_lp_girls = self.cms_post("data/learnerperformance/", data_girls);
                    p_lp_girls.add_callback(function() {
                        return im.api_request('contacts.update_extras', {
                            key: contact_key,
                            fields: {
                                "rts_last_save_performance_learner": 'true'
                            }
                        });
                    });
                    return p_lp_girls;
                });
                return p_lp_boys;
            }
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
            "There is a problem with the EMIS number you have entered.",
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
        var p = self.get_contact(im);

        p.add_callback(function(result) {
            if (result.contact["extras-rts_id"] === undefined){
                // unrecognised user
                return new ChoiceState(
                    state_name,
                    function(choice) {
                        return choice.value;
                    },
                    "Welcome to the Zambia School Gateway! Options:",
                    [
                        new Choice("reg_emis", "Register as Head Teacher"),
                        new Choice("reg_district_official", "Register as District Official"),
                        new Choice("manage_change_emis_error", "Change my school"),
                        new Choice("manage_change_msisdn_emis", "Change my primary cell number")
                    ]
                );
            } else {
                // recognised user
                return new ChoiceState(
                    state_name,
                    function(choice) {
                        return choice.value;
                    },
                    "What would you like to do?",
                    [
                        new Choice("perf_teacher_ts_number", "Report on teacher performance."),
                        new Choice("perf_learner_boys_total", "Report on learner performance."),
                        new Choice("manage_change_emis", "Change my school."),
                        new Choice("manage_update_school_data", "Update my school’s registration data.")

                    ]
                );
            }
        });
        return p;
    });

// District official
/********************************************************************************************/
    self.add_creator('reg_district_official', function(state_name, im){
        var choices = [];

        districts_json = im.config.districts_json;
        districts_json.sort(function(a, b){
                                return ((a.name < b.name) ?
                                        -1 : ((a.name > b.name) ? 1 : 0)); });

        for (var i=0; i<districts_json.length; i++){
            var district = districts_json[i];
            choices[i] = new Choice(district.id, district.name);
        }
        return new PaginatedChoiceState(state_name,
                                        "reg_district_official_first_name",
                                        "Please enter your district name.",
                                        choices,
                                        null,
                                        null,
                                        {});
    });

    self.add_state(new FreeText(
        "reg_district_official_first_name",
        "reg_district_official_surname",
        "Please enter your FIRST name."
    ));

    self.add_state(new FreeText(
        "reg_district_official_surname",
        "reg_district_official_id_number",
        "Now please enter your SURNAME."
    ));

    self.add_state(new FreeText(
        "reg_district_official_id_number",
        "reg_district_official_dob",
        "Please enter your ID number."
    ));

    self.add_state(new FreeText(
        "reg_district_official_dob",
        "reg_thanks_district_admin",
        "Please enter your date of birth. Start with the day,"+
        " followed by the month and year, e.g. 27111980.",
        function(content) {
            // check that the value provided is date format we expect
            return self.check_and_parse_date(content);
        },
        "Please enter your date of birth formatted DDMMYYYY"
    ));

    self.add_state(new EndState(
            "reg_thanks_district_admin",
            "Congratulations! You are now registered as a user of the" +
            " Gateway! Please dial in again when you are ready to start" +
            " reporting on teacher and learner performance.",
            "initial_state",
            {
                on_enter: function(){
                    return self.cms_district_admin_registration(im);
                }
            }
        )
    );

/********************************************************************************************/

    self.add_state(new FreeText(
        "reg_emis",
        "reg_emis_validator",
        "Please enter your school's EMIS number. This should have 4-6 digits e.g 4351."
    ));

    self.add_state(new FreeText(
        "reg_emis_try_2",
        "reg_emis_validator",
        "Please enter your school's EMIS number. This should have 4-6 digits e.g 4351."
    ));

    self.add_creator('reg_emis_validator', function(state_name, im){
        var EMIS;
        if (im.get_user_answer('reg_emis_try_2')) {
            EMIS = im.get_user_answer('reg_emis_try_2');
        } else {
            EMIS = im.get_user_answer('reg_emis');
        }
        if (self.check_valid_emis(EMIS)) { // EMIS valid
            return new ChoiceState(
                "reg_emis_validator",
                "reg_school_name",
                "Thanks for claiming this EMIS. Redial this number if you ever change cellphone " +
                    "number to reclaim the EMIS and continue to receive SMS updates.",
                [
                    new Choice(EMIS, "Continue")
                ]
            );
        } else {
            if (im.get_user_answer('reg_emis_try_2')) { // Second failure - force exit
                return new EndState(
                    "reg_exit_emis",
                    "We don't recognise your EMIS number. Please send a SMS with" +
                    " the words EMIS ERROR to 739 and your DEST will contact you" +
                    " to resolve the problem.",
                    "initial_state"
                );
            } else { // First invalid EMIS - request again
                return new ChoiceState(
                    "reg_emis_error",
                    function(choice) {
                        return choice.value;
                    },
                    "There is a problem with the EMIS number you have entered.",
                    [
                        new Choice("reg_emis_try_2", "Try again"),
                        new Choice("reg_exit_emis", "Exit")
                    ]
                );
            }
        }
    });

    self.add_state(new ChoiceState(
        "reg_emis_error",
        function(choice) {
            return choice.value;
        },
        "There is a problem with the EMIS number you have entered.",
        [
            new Choice("reg_emis_try_2", "Try again"),
            new Choice("reg_exit_emis", "Exit")
        ]
    ));

    self.add_state(new FreeText(
        "manage_change_msisdn_emis",
        "manage_change_msisdn_emis_validator",
        "Please enter the school's EMIS number that you are currently registered with. This should have 4-6 digits e.g 4351."
    ));

    self.add_state(new FreeText(
        "manage_change_msisdn_emis_try_2",
        "manage_change_msisdn_emis_validator",
        "Please enter the school's EMIS number that you are currently registered with. This should have 4-6 digits e.g 4351."
    ));

    self.add_state(new ChoiceState(
        "manage_change_emis_error",
        function(choice) {
                return choice.value;
            },
        "Your cell phone number is unrecognised. Please associate your new number with " +
        "your old EMIS first before requesting to change school.",
        [
            new Choice("initial_state", "Main menu."),
            new Choice("end_state", "Exit.")
        ]
    ));

    self.add_creator('manage_change_msisdn_emis_validator', function(state_name, im) {
        var EMIS;
        if (im.get_user_answer('manage_change_msisdn_emis_try_2')) {
            EMIS = im.get_user_answer('manage_change_msisdn_emis_try_2');
        } else {
            EMIS = im.get_user_answer('manage_change_msisdn_emis');
        }
        if (self.check_valid_emis(EMIS)) {
            // EMIS valid
            return new EndState(
                state_name,
                "Thank you! Your cell phone number is now the official number" +
                " that your school will use to communicate with the Gateway.",
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
            if (im.get_user_answer('reg_emis_try_2')) { // Second failure - force exit
                return new EndState(
                    "reg_exit_emis",
                    "We don't recognise your EMIS number. Please send a SMS with" +
                    " the words EMIS ERROR to 739 and your DEST will contact you" +
                    " to resolve the problem.",
                    "initial_state"
                );
            } else { // First invalid EMIS - request again
                return new ChoiceState(
                    "manage_change_msisdn_emis_error",
                    function(choice) {
                        return choice.value;
                    },
                    "There is a problem with the EMIS number you have entered.",
                    [
                        new Choice("manage_change_msisdn_emis_try_2", "Try again"),
                        new Choice("reg_exit_emis", "Exit")
                    ]
                );
            }
        }
    });

    self.add_state(new ChoiceState(
        "manage_change_msisdn_emis_error",
        function(choice) {
            return choice.value;
        },
        "There is a problem with the EMIS number you have entered.",
        [
            new Choice("manage_change_msisdn_emis_try_2", "Try again"),
            new Choice("reg_exit_emis", "Exit")
        ]
    ));

    self.add_state(new ChoiceState(
        "manage_update_school_data",
        function(choice) {
            return choice.value;
        },
        "You'll now be asked to re-enter key school details to ensure the records are accurate. Enter 1 to continue.",
        [
            new Choice("reg_school_boys", "Continue")
        ]
    ));

    self.add_state(new FreeText(
        "manage_change_emis",
        "manage_change_emis_validator",
        "Please enter your school's EMIS number. This should have 4-6 digits e.g 4351."
    ));

    self.add_state(new FreeText(
        "manage_change_emis_try_2",
        "manage_change_emis_validator",
        "Please enter your school's EMIS number. This should have 4-6 digits e.g 4351."
    ));

    self.add_creator('manage_change_emis_validator', function(state_name, im){
        var EMIS;
        if (im.get_user_answer('manage_change_emis_try_2')) {
            EMIS = im.get_user_answer('manage_change_emis_try_2');
        } else {
            EMIS = im.get_user_answer('manage_change_emis');
        }
        if (self.check_valid_emis(EMIS)) { // EMIS valid
            return new ChoiceState(
                "manage_change_emis_validator",
                "reg_school_boys",
                "Thanks for claiming this EMIS. Redial this number if you ever change cellphone " +
                    "number to reclaim the EMIS and continue to receive SMS updates.",
                [
                    new Choice(EMIS, "Continue")
                ]
            );
        } else {
            if (im.get_user_answer('manage_change_emis_try_2')) { // Second failure - force exit
                return new EndState(
                    "reg_exit_emis",
                    "We don't recognise your EMIS number. Please send a SMS with" +
                    " the words EMIS ERROR to 739 and your DEST will contact you" +
                    " to resolve the problem.",
                    "initial_state"
                );
            } else { // First invalid EMIS - request again
                return new ChoiceState(
                    "manage_change_emis_enter_error",
                    function(choice) {
                        return choice.value;
                    },
                    "There is a problem with the EMIS number you have entered.",
                    [
                        new Choice("manage_change_emis_try_2", "Try again"),
                        new Choice("reg_exit_emis", "Exit")
                    ]
                );
            }
        }
    });

    self.add_state(new ChoiceState(
        "manage_change_emis_enter_error",
        function(choice) {
            return choice.value;
        },
        "There is a problem with the EMIS number you have entered.",
        [
            new Choice("manage_change_emis_try_2", "Try again"),
            new Choice("reg_exit_emis", "Exit")
        ]
    ));


    self.add_state(new EndState(
        "reg_exit_emis",
        "We don't recognise your EMIS number. Please send a SMS with" +
        " the words EMIS ERROR to 739 and your DEST will contact you" +
        " to resolve the problem.",
        "initial_state"
    ));

    self.add_state(new FreeText(
        "reg_school_name",
        "reg_first_name",
        "Please enter the name of your school, e.g. Kapililonga"
    ));

    self.add_state(new FreeText(
        "reg_first_name",
        "reg_surname",
        "Please enter your FIRST name."
    ));

    self.add_state(new FreeText(
        "reg_surname",
        "reg_date_of_birth",
        "Now please enter your SURNAME."
    ));

    self.add_state(new FreeText(
        "reg_date_of_birth",
        "reg_gender",
        "Please enter your date of birth. Start with the day, followed by " +
            "the month and year, e.g. 27111980",
        function(content) {
            // check that the value provided is date format we expect
            return self.check_and_parse_date(content);
        },
        "Please enter your date of birth formatted DDMMYYYY"
    ));

    self.add_state(new ChoiceState(
        'reg_gender',
        'reg_school_boys',
        "What is your gender?",
        [
            new Choice("female", "Female"),
            new Choice("male", "Male")
        ]
    ));

    self.add_state(new FreeText(
        "reg_school_boys",
        "reg_school_girls",
        "How many boys do you have in your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many boys you have in your school.'
    ));

    self.add_state(new FreeText(
        "reg_school_girls",
        "reg_school_classrooms",
        "How many girls do you have in your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many girls you have in your school.'
    ));

    self.add_state(new FreeText(
        "reg_school_classrooms",
        "reg_school_teachers",
        "How many classrooms do you have in your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many classrooms you have in your school.'
    ));

    self.add_state(new FreeText(
        "reg_school_teachers",
        "reg_school_teachers_g1",
        "How many teachers are presently working in your school, including the head teacher?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many teachers in total you have in your school.'
    ));

    self.add_state(new FreeText(
        "reg_school_teachers_g1",
        "reg_school_teachers_g2",
        "How many teachers teach Grade 1 local language?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many teachers teach G1 local language literacy.'
    ));

    self.add_state(new FreeText(
        "reg_school_teachers_g2",
        "reg_school_students_g2_boys",
        "How many teachers teach Grade 2 local language?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for how many teachers teach G2 local language literacy.'
    ));

    self.add_state(new FreeText(
        "reg_school_students_g2_boys",
        "reg_school_students_g2_girls",
        "How many boys are ENROLLED in Grade 2 at your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for the total number of G2 boys enrolled.'
    ));

    self.add_state(new FreeText(
        "reg_school_students_g2_girls",
        "reg_zonal_head",
        "How many girls are ENROLLED in Grade 2 at your school?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for the total number of G2 girls enrolled.'
    ));

    self.add_state(new ChoiceState(
        'reg_zonal_head',
        function(choice) {
            return choice.value;
        },
        "Are you a Zonal Head Teacher?",
        [
            new Choice("reg_thanks_zonal_head", "Yes"),
            new Choice("reg_zonal_head_name", "No")
        ]
    ));

    self.add_state(new FreeText(
        "reg_zonal_head_name",
        "reg_thanks_head_teacher",
        "Please enter the name and surname of your ZONAL HEAD TEACHER."
    ));

    self.add_state(new EndState(
            "reg_thanks_head_teacher",
            "Congratulations! You are now registered as a user of the" +
            " Gateway! Please dial in again when you are ready to start" +
            " reporting on teacher and learner performance.",
            "initial_state",
            {
                on_enter: function(){
                    return self.cms_registration(im);
                }
            }
        )
    );

    self.add_state(new EndState(
            "reg_thanks_zonal_head",
            "Well done! You are now registered as a Zonal Head Teacher." +
            " When you are ready, dial in to start reporting. You will" +
            " also receive monthly SMS's from your zone.",
            "initial_state",
            {
                on_enter: function(){
                    return self.cms_registration(im);
                }
            }
        )
    );

    /////////////////////////////////////////////////////////////////
    // Start of Performance Management - Teachers
    /////////////////////////////////////////////////////////////////

    self.add_state(new FreeText(
        "perf_teacher_ts_number",
        "perf_teacher_gender",
        "Please enter the teacher's TS number.",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the teacher's TS number.",
        {
            on_enter: function(){
                var p = self.clear_contact_extra("rts_last_save_performance_teacher");
                return p;
            }
        }
    ));

    self.add_state(new ChoiceState(
        'perf_teacher_gender',
        'perf_teacher_age',
        "What is the gender of the teacher?",
        [
            new Choice("male", "Male"),
            new Choice("female", "Female")
        ]
    ));

    self.add_state(new FreeText(
        "perf_teacher_age",
        "perf_teacher_academic_level",
        "Please enter the teacher's age in years e.g. 26.",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the teacher's age."
    ));

    self.add_state(new ChoiceState(
        "perf_teacher_academic_level",
        "perf_teacher_years_experience",
        "What is the teacher's highest education level?",
        [
            new Choice("1", "Gr 7"),
            new Choice("2", "Gr 9"),
            new Choice("3", "Gr 12"),
            new Choice("4", "PTC"),
            new Choice("5", "PTD"),
            new Choice("6", "Dip Ed"),
            new Choice("7", "Other diploma"),
            new Choice("8", "BA Degree"),
            new Choice("9", "MA Degree"),
            new Choice("10", "Other"),
        ]
    ));

    self.add_state(new ChoiceState(
        "perf_teacher_years_experience",
        "perf_teacher_g2_pupils_present",
        "How many years of teaching experience does this teacher have?",
        [
            new Choice("0-3", "0 - 3 years"),
            new Choice("4-8", "4 - 8 years"),
            new Choice("9-12", "9 - 12 years"),
            new Choice("13+", "13 years or more"),
        ]
    ));

    self.add_state(new FreeText(
        "perf_teacher_g2_pupils_present",
        "perf_teacher_g2_pupils_registered",
        "How many children were PRESENT during the observed lesson?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for pupils present.'
    ));

    self.add_state(new FreeText(
        "perf_teacher_g2_pupils_registered",
        "perf_teacher_classroom_environment_score",
        "How many children are ENROLLED in the Grade 2 class that was observed?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for pupils enrolled.'
    ));

    self.add_state(new FreeText(
        "perf_teacher_classroom_environment_score",
        "perf_teacher_t_l_materials",
        "Enter the subtotal that the teacher achieved during the classroom " +
            "observation for Section 2 (Classroom Environment).",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for the Classroom Environment subtotal.'
    ));

    self.add_state(new FreeText(
        "perf_teacher_t_l_materials",
        "perf_teacher_pupils_books_number",
        "Enter the subtotal that the teacher achieved during the classroom " +
            "observation for Section 3 (Teaching and Learning Materials).",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        'Please provide a number value for the Teaching and Learning Materials subtotal.'
    ));

    self.add_state(new FreeText(
        "perf_teacher_pupils_books_number",
        "perf_teacher_pupils_materials_score",
        "Enter the number of learners' books (text books) for literacy that were " +
            "available in the classroom during the lesson observation.",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for number of learners' books."
    ));

    self.add_state(new FreeText(
        "perf_teacher_pupils_materials_score",
        "perf_teacher_reading_lesson",
        "Enter the subtotal that the teacher achieved during the classroom observation " +
            "for Section 4 (Learner Materials).",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Learner Materials subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_reading_lesson",
        "perf_teacher_pupil_engagement_score",
        "Enter the subtotal that the teacher achieved during the classroom observation " +
            "for Section 5 (Time on Task and Reading Practice)",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Time on Task and Reading Practice subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_pupil_engagement_score",
        "perf_teacher_attitudes_and_beliefs",
        "Enter the subtotal that the teacher achieved during the classroom observation " +
            "for Section 6 (Learner Engagement)",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Learner Engagement subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_attitudes_and_beliefs",
        "perf_teacher_training_subtotal",
        "Enter the subtotal that the teacher achieved during the interview on Section " +
            "7.1. (Teacher Attitudes and Beliefs)",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Teacher Attitudes and Beliefs subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_training_subtotal",
        "perf_teacher_reading_assessment",
        "Enter the subtotal that the teacher achieved during the interview on Section " +
            "7.2. (Teacher Training)",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Teacher Training interview subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_reading_assessment",
        "perf_teacher_reading_total",
        "Enter the subtotal that the teacher achieved during the interview " +
            "on Section 7.3. (Reading Assessment).",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the Reading Assessment subtotal."
    ));

    self.add_state(new FreeText(
        "perf_teacher_reading_total",
        "perf_teacher_completed",
        "According to your assessment records, how many of the pupils in the class " +
            "that was observed have broken through/can read?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for the pupils in the class that have broken " +
            "through/can read."
    ));

    self.add_creator('perf_teacher_completed', function(state_name, im) {
        // Log the users data
        var p = self.cms_performance_teacher(im);
        // Generate the EndState
        p.add_callback(function(result) {
            return new ChoiceState(
                state_name,
                function(choice) {
                        return choice.value;
                    },
                "Congratulations, you have finished reporting on this teacher.",
                [
                    new Choice("perf_teacher_ts_number", "Add another teacher."),
                    new Choice("initial_state", "Go back to the main menu."),
                    new Choice("end_state", "Exit.")
                ]
            );
        });
        return p;
    });


    /////////////////////////////////////////////////////////////////
    // Start of Performance Management - Learners
    /////////////////////////////////////////////////////////////////

    self.add_state(new FreeText(
        "perf_learner_boys_total",
        "perf_learner_girls_total",
        "How many boys took part in the learner assessment?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys assessed.",
        {
            on_enter: function(){
                var p = self.clear_contact_extra("rts_last_save_performance_learner");
                return p;
            }
        }
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_total",
        "perf_learner_boys_phonetic_awareness",
        "How many girls took part in the learner assessment?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls assessed."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_phonetic_awareness",
        "perf_learner_girls_phonetic_awareness",
        "How many boys achieved at least 4 out of 6 correct answers for Section " +
            "1 (Phonics and Phonemic Awareness)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving 4 out of 6" +
        " correct answers for Phonics and Phonemic Awareness."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_phonetic_awareness",
        "perf_learner_boys_vocabulary",
        "How many girls achieved at least 4 out of 6 correct answers for Section " +
            "1 (Phonics and Phonemic Awareness)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving 4 out of 6" +
        " correct answers for Phonics and Phonemic Awareness."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_vocabulary",
        "perf_learner_girls_vocabulary",
        "How many boys achieved at least 3 out of 6 correct answers for Section 2 (Vocabulary)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving 3 out of 6" +
        " correct answers for Vocabulary."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_vocabulary",
        "perf_learner_boys_reading_comprehension",
        "How many girls achieved at least 3 out of 6 correct answers for Section 2 (Vocabulary)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving 3 out of 6" +
        " correct answers for Vocabulary."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_reading_comprehension",
        "perf_learner_girls_reading_comprehension",
        "How many boys achieved at least 2 out of 4 correct answers for Section 3 (Comprehension)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving 2 out of 4" +
        " correct answers for Comprehension."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_reading_comprehension",
        "perf_learner_boys_writing_diction",
        "How many girls achieved at least 2 out of 4 correct answers for Section 3 (Comprehension)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving 2 out of 4" +
        " correct answers for Comprehension."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_writing_diction",
        "perf_learner_girls_writing_diction",
        "How many boys achieved at least 2 out of 4 correct answers for Section 4 (Writing)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving 2 out of 4" +
        " correct answers for Writing."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_writing_diction",
        "perf_learner_boys_outstanding_results",
        "How many girls achieved at least 2 out of 4 correct answers for Section 4 (Writing)?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving 2 out of 4" +
        " correct answers for Writing."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_outstanding_results",
        "perf_learner_girls_outstanding_results",
        "In total, how many boys achieved 16 out of 20 or more?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving 16 out of 20 or more."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_outstanding_results",
        "perf_learner_boys_desirable_results",
        "In total, how many girls achieved 16 out of 20 or more?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving 16 out of 20 or more."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_desirable_results",
        "perf_learner_girls_desirable_results",
        "In total, how many boys achieved between 12 and 15 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving between 12 and 15 out of 20."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_desirable_results",
        "perf_learner_boys_minimum_results",
        "In total, how many girls achieved between 12 and 15 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving between 12 and 15 out of 20."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_minimum_results",
        "perf_learner_girls_minimum_results",
        "In total, how many boys achieved between 8 and 11 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving between 8 and 11 out of 20."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_minimum_results",
        "perf_learner_boys_below_minimum_results",
        "In total, how many girls achieved between 8 and 11 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving between 8 and 11 out of 20."
    ));

    self.add_state(new FreeText(
        "perf_learner_boys_below_minimum_results",
        "perf_learner_girls_below_minimum_results",
        "In total, how many boys achieved between 0 and 7 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total boys achieving between 0 and 7 out of 20."
    ));

    self.add_state(new FreeText(
        "perf_learner_girls_below_minimum_results",
        "perf_learner_completed",
        "In total, how many girls achieved between 0 and 7 out of 20?",
        function(content) {
            // check that the value provided is actually decimal-ish.
            return self.check_valid_number(content);
        },
        "Please provide a number value for total girls achieving between 0 and 7 out of 20."
    ));

    self.add_creator('perf_learner_completed', function(state_name, im) {
        // Log the users data
        var p = self.cms_performance_learner(im);
        // Generate the EndState
        p.add_callback(function(result) {
            return new ChoiceState(
                state_name,
                function(choice) {
                        return choice.value;
                    },
                "Congratulations. You have finished reporting on the learner assessment.",
                [
                    new Choice("initial_state", "Go back to the main menu."),
                    new Choice("end_state", "Exit.")
                ]
            );
        });
        return p;
    });


    /////////////////////////////////////////////////////////////////
    // End of Performance Management - Learners
    /////////////////////////////////////////////////////////////////

    self.add_state(new EndState(
        "end_state",
        "Goodbye! Thank you for using the Gateway.",
        "initial_state"
    ));

    self.on_config_read = function(event){
        // Run calls out to the APIs to load dynamic states
        var p = new Promise();
        p.add_callback(self.cms_hierarchy_load);
        p.add_callback(self.cms_district_load);
        p.callback();
        return p;
    };
}

// launch app
var states = new GoRtsZambia();
var im = new InteractionMachine(api, states);
im.attach();
