

function ok (value) {}
function fail (error) {}

var current_token;
var username;
var password;
var proto = "https";
var environment_name;
var environment;

var token_sent = false;

function launchApp(url) {
	console.log(" ****** launchApp");
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
	
	// get any notification variables for use in your app
   	window.FirebasePlugin.onNotificationOpen(function(notification){
    	//Check if notification exists then do something with the payload vars
    	var str = JSON.stringify(notification);
    	console.log("***** Javascript.onNotificationopen **** : " + str);
    });

   	document.addEventListener("resume", onResume, false); 
}

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
		plugins.appPreferences.fetch('username_preference').then(function(result) {
			username = result;
		}, fail);
		plugins.appPreferences.fetch('password_preference').then(function(result) {
			password = result;
		}, fail);
		plugins.appPreferences.fetch('environment_preference').then(function(result) {
			environment_name = result;
		}, fail);
		setTimeout(function() {
			if (environment_name == "purple") {
				proto = "http";
				environment = "localhost:8080";
			} else if (environment_name == "blue") {
				environment = "daranalysis-200000.appspot.com";
			} else if (environment_name == "red") {
				environment ="daranalysis-160000.appspot.com";
			} else if (environment_name == "yellow") {
				environment ="daranalysis-200000.appspot.com";
			} else if (environment_name == "amber") {
				environment ="daranalysis-200000.appspot.com";
			} else if (environment_name == "green") {
				environment ="daranalysis-200000.appspot.com";
			}
			console.log(" *** " + username + ", " + password + ", " + proto + ", " + environment);
			var url = proto + "://" + username + ":" + password + "@" + environment; 
			console.log(" ********* " + url);
			$.ajax({
				type: "GET",
				url: url,
				success: function(response, textStatus, xhr) {
					console.log(" ****** " + xhr.status);
					if (xhr.status == 404) {
						plugins.appPreferences.show();
					} else {
						url = proto + "://" + username + ":" + password + "@" + environment; 
						launchApp(url);
					}
				},
				error: function(xhr, textStatus) {
					console.log(xhr.status + ", " + textStatus);
					plugins.appPreferences.show();
				},
				timeout:3000
			});
		}, 2000);
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



