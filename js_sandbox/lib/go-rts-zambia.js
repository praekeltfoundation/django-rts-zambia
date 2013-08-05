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

function VumiGoSkeleton() {
    var self = this;
    // The first state to enter
    StateCreator.call(self, 'initial_state');

    // Shared creators
    self.make_emis_error_state = function(state_name) {
        return new ChoiceState(
            state_name,
            function(choice) {
                return choice.value;
            },
            "Sorry!\nThat is not a EMIS we recognise. Make sure you have " +
            "entered the number correctly.",
            [
                new Choice("reg_emis", "Try again"),
                new Choice("reg_exit_emis", "Exit")
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
                new Choice("manage_change_msisdn", "Change my primary mobile number")
            ]
        );
    });

    self.add_state(new FreeText(
        "reg_emis",
        "reg_school_name",
        "What is your school EMIS number?"
    ));

    self.add_creator('reg_school_name', function(state_name, im) {
        var EMIS = parseInt(im.get_user_answer('reg_emis'));
        // TODO: Validate EMIS properly
        if (EMIS === 1) {
            // EMIS valid
            return new FreeText(
                state_name,
                "reg_first_name",
                "What is your school name?"
            );
        } else {
            // Invalid EMIS - request again
            return self.make_emis_error_state('reg_emis_error');
        }
    });

    self.add_state(self.make_emis_error_state('reg_emis_error'));

    self.add_creator('reg_exit_emis', function(state_name, im) {
        return new EndState(
            state_name,
            "There seems to be a problem with the EMIS number. Please send a SMS " +
            "with the code EMIS ERROR to " + im.config.sms_short_code + " " +
            "and your district officer will be in touch.",
            "initial_state"
        );
    });

    self.add_state(new EndState(
        "end_state",
        "Thank you and bye bye!",
        "initial_state"
    ));
}

// launch app
var states = new VumiGoSkeleton();
var im = new InteractionMachine(api, states);
im.attach();
 
