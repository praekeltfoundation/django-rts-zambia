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


function GoRtsZambiaSmsError(msg) {
    var self = this;
    self.msg = msg;

    self.toString = function() {
        return "<GoRtsZambiaError: " + self.msg + ">";
    };
}

function SMSEndState(name, text, next, handlers) {
    // State that mimicks the USSD behaviour when a USSD session ends
    // it fast forwards to the start of the InteractionMachine.
    // We need to do this because SMS doesn't have the Session capabities
    // that provide us this functionality when using USSD.
    var self = this;
    handlers = handlers || {};
    if(handlers.on_enter === undefined) {
        handlers.on_enter = function() {
            self.input_event('', function() {});
        };
    }
    EndState.call(self, name, text, next, handlers);
}

function GoRtsZambiaSms() {
    var self = this;

    self.post_headers = {
        'Content-Type': ['application/json']
    };

    // The first state to enter
    StateCreator.call(self, 'initial_state');

    // START Shared helpers

    self.send_sms = function(content, to_addr) {
        var sms_tag = im.config.sms_tag;
        if (!sms_tag) return success(true);
        im.log('outbound.send_to_tag with ' + content + ' and ' + to_addr);
        return im.api_request("outbound.send_to_tag", {
            to_addr: to_addr,
            content: content,
            tagpool: sms_tag[0],
            tag: sms_tag[1]
        });
    };

    self.make_send_sms_function = function(im, content, number) {
        // returns a function that when called sends the content string
        // as a message to the number provided.
        // Use this when you need to have SMSs sent out as part of
        // a Promise callback chain to prevent variable scoping problems.
        return function() {
            return self.send_sms(im, content, number);
        };
    };

    self.cms_get = function(path) {
        var url = im.config.cms_api_root + path;
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
        var url = im.config.cms_api_root + path;
        var p = im.api_request("http.post", {
            url: url,
            headers: self.post_headers,
            data: JSON.stringify(data)
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'POST', data, false);
            return json;
        });
        return p;
    };

    self.cms_put = function(path, data) {
        var url = im.config.cms_api_root + path;
        var p = im.api_request("http.put", {
            url: url,
            headers: self.post_headers,
            data: JSON.stringify(data)
        });
        p.add_callback(function(result) {
            var json = self.check_reply(result, url, 'PUT', data, false);
            return json;
        });
        return p;
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
            throw new GoRtsZambiaSmsError(error_msg);
        }
    };

    self.get_contact = function(im){
        var p = im.api_request('contacts.get_or_create', {
            delivery_class: 'ussd',
            addr: im.user_addr
        });
        return p;
    };

    // END Shared helpers

    // START CMS Interactions


    // END CMS Interactions

    self.add_creator('initial_state', function(state_name, im) {
        var p = self.get_contact(im);
        var response_state;
        p.add_callback(function(result) {
            if (result.contact["extras-rts_id"] === undefined) {
                return new FreeText(
                    state_name,
                    'not_registered',
                    im.config.output["not_registered"]);
            } else {
                return new FreeText(
                    state_name,
                    'thanks',
                    im.config.output["not_registered"]);
            }
        });
        return p;
    });

    self.add_creator('not_registered', function(state_name, im) {
        return new SMSEndState(
            state_name,
            im.config.output[state_name],
            'initial_state');
    });

    self.add_creator('thanks', function(state_name, im) {
        return new SMSEndState(
            state_name,
            im.config.output[state_name],
            'initial_state',
                {
                    on_enter: function(){
                        var p = self.get_contact(im);
                        p.add_callback(function(result) {
                            return self.cms_get(
                                "data/headteacher/?emis__emis=" +
                                result.contact["extras-rts_emis"] +
                                "&is_zonal_head=true");
                        });
                        p.add_callback(function(result) {
                            if (result.msisdn) {
                                var to_addr = result.msisdn;
                                var content = im.get_user_answer('initial_state');
                                return self.send_sms(content, to_addr);
                            }
                        });
                        return p;
                    }
                }
            );
    });

}

// launch app
var states = new GoRtsZambiaSms();
var im = new InteractionMachine(api, states);
im.attach();
 
