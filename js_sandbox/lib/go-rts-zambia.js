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
        "reg_schoolname",
        "What is your school EMIS number?"
    ));

    self.add_state(new EndState(
        "end_state",
        "Thank you and bye bye!",
        "first_state"
    ));
}

// launch app
var states = new VumiGoSkeleton();
var im = new InteractionMachine(api, states);
im.attach();
 
