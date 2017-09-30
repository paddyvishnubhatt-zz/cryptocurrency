
//var environment="10.0.2.2:8080";
//var proto="https";
//var environment ="daranalysis-200000.appspot.com";

function ok (value) {}
function fail (error) {}

var current_token;
var username;
var password;
var proto;
var environment;

var token_sent = false;

function onResume() {
	// get any notification variables for use in your app
	window.FirebasePlugin.onNotificationOpen(function(notification){
		//Check if notification exists then do something with the payload vars
		var str = JSON.stringify(notification);
    	console.log("***** Javascript.onResume **** : " + str);
	});
}

function updateToken() {
	if (current_token == undefined) {
		return;
	}
	console.log("******* UpdateToken ******** " + current_token);
	// Check local cache for any change and then only call GAE (else too expensive!)
    var data = {"token" : current_token};
	var url = proto + "://" + environment;
    $.ajax({
    	type: "POST",
    	url: url + "/api/v1/update_token",
    	data: data
    });
}

var app = {
    // Application Constructor
    initialize: function() {
        document.addEventListener('deviceready', this.onDeviceReady.bind(this), false);
    },

    // deviceready Event Handler
    // Bind any cordova events here. Common events are:
    // 'pause', 'resume', etc.
    onDeviceReady: function() {
        this.receivedEvent('deviceready');
        var str 		= device.platform;
		console.log(" *** " + str);
		var url = proto + "://" + environment;
		
		plugins.appPreferences.fetch('username_preference').then(function(result) {
			username = result;
		}, fail);
		plugins.appPreferences.fetch('password_preference').then(function(result) {
			password = result;
		}, fail);
		plugins.appPreferences.fetch('proto_preference').then(function(result) {
			proto = result;
		}, fail);
		plugins.appPreferences.fetch('environment_preference').then(function(result) {
			environment = result;
		}, fail);
		setTimeout(function() {
			console.log(" *** " + username + ", " + password + ", " + proto + ", " + environment);
			if (str == "iOS") {
				url = proto + "://" + username + ":" + password + "@" + environment; 
			}
			console.log(url);
			ref = window.open(url, '_blank', 'location=no,toolbar=no');
			ref.addEventListener( "loadstop", function() {
				if (!token_sent) {
					updateToken();
					token_sent = true;
				}
			});
			// e.g TokenRefresh, onNotificationOpen etc
			window.FirebasePlugin.onTokenRefresh(function(token){
				//Do something with the token server-side if it exists
				if (current_token != token) {
					current_token = token;
					updateToken();
				}
			});
		}, 2000);

	    // get any notification variables for use in your app
   		window.FirebasePlugin.onNotificationOpen(function(notification){
    		//Check if notification exists then do something with the payload vars
    		var str = JSON.stringify(notification);
    		console.log("***** Javascript.onNotificationopen **** : " + str);
    	});

    	document.addEventListener("resume", onResume, false); 
    },

    // Update DOM on a Received Event
    receivedEvent: function(id) {
        //var parentElement = document.getElementById(id);
        //var listeningElement = parentElement.querySelector('.listening');
        //var receivedElement = parentElement.querySelector('.received');

        //listeningElement.setAttribute('style', 'display:none;');
        //receivedElement.setAttribute('style', 'display:block;');

        console.log('Received Event: ' + id);
    },

};

app.initialize();



