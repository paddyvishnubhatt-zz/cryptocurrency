function popup(title, message) {

    BootstrapDialog.show({
    size: BootstrapDialog.SIZE_NORMAL,
    title: title,
    message: message,
    buttons: [{
            label: 'Close',
            action: function(dialogItself){
                dialogItself.close();
            }
        }]
    });
}

function popupConfirm(title, message, functionPointer) {

    BootstrapDialog.confirm({
    size: BootstrapDialog.SIZE_NORMAL,
    title: title,
    type: BootstrapDialog.TYPE_WARNING,
    btnOKClass: 'btn-warning',
    message: message,
    closable: true,
    callback: function(result) {
        if(result) {
            functionPointer(result);
        }
    }
    });
}

function logout(){
        jQuery.ajax({
            type: "GET",
            url: "/",
            async: false,
            username: "logmeout",
            password: "123456",
            headers: { "Authorization": "Basic xxx" }
       })
        .done(function(){
            // If we don't get an error, we actually got an error as we expect an 401!
        })
        .fail(function(){
            // We expect to get an 401 Unauthorized error! In this case we are successfully
                // logged out and we redirect the user.
            window.location = "/";
        });
}