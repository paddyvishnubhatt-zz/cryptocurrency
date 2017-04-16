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

function saveUser(user) {
    console.log(user);
    var data = {email: user.email, password : user.password};
    $.ajax({
      type: "PATCH",
      url: "/api/v1/set_user/" + user.identity,
      data: data
    });
}

function showUser(user) {
    var message ='<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-show-password/1.0.3/bootstrap-show-password.min.js"></script>';
    message += '<form><table class="table table-condensed" ><tbody>';
    var smsg = '<tr><td><label class="control-label col-sm-2" for="identity">User ID: </label></td>';
    smsg += '<td><input class="form-control" type="text" name="identity" id="identity" + value=' + user.identity + ' readonly></td></tr>';
    smsg += '<tr><td><label class="control-label col-sm-2" for="email">Email: </label></td>';
    smsg += '<td><input class="form-control" type="text" name="email" id="email" + value=' + user.email + ' > </td></tr>';
    smsg += '<tr><td><label class="control-label col-sm-2" for="password">Password: </label></td>';
    smsg += '<td><input class="form-control" type="password" name="password" id="password" data-toggle="password" value=' + user.password + ' ></td></tr>';

    message += smsg;
    message += "</tbody></table></form>";
    popupConfirm("User Settings (OK to confirm change)", message, function(){
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        var isChanged = false;
        if (user.email != email) {
            user.email = email;
            isChanged = true;
        }
        if (user.password != password) {
            user.password = password;
            isChanged = true;
        }
        if (isChanged) {
            saveUser(user);
        }
    })
}

