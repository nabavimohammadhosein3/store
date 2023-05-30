function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
        var expires = "; expires=" + date.toGMTString();
    } else {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function replace(url){
    window.location.replace(url)
}

$('#loginform').submit(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        url: "/account/login/",
        data:
            {
            'username': $('#username').val(),
            'password': $('#password').val(),
            },
        success: function (response) {
            if (response.error == 'correct'){
                $.ajax({
                    type: "POST",
                    headers: {'X-CSRFToken': csrftoken},
                    mode: 'same-origin',
                    url: "/account/token/",
                    data:
                        {
                        'username': $('#username').val(),
                        'password': $('#password').val(),
                        },
                    success: function (response) {
                        eraseCookie('jwt-access');
                        eraseCookie('jwt-refresh');
                        createCookie('jwt-access', response.access, (1/24));
                        createCookie('jwt-refresh', response.refresh, (1/24));
                        replace('/account/');
                    }
                });
            }else{
                $('.alert').removeClass('d-none');
                $('.alert').addClass('d-block');
            }
        }
    });
});