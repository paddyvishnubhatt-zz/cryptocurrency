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