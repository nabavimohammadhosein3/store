$('input[id]').addClass('form-control');
$('input[for]').addClass('form-label');
$('input[id=id_password1], input[id=id_password2]').attr('type', 'password');
$('input[id] ~ .invalid-feedback').prev().addClass('is-invalid');
$('.form-group').addClass('mb-3');

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

if ($('.paid .card').length == 0){
    $('.paid').text('no eny products...');
}
if ($('.pend .card').length == 0){
    $('.pend').text('no eny products...');
}
$('#logout').click(function (e) { 
    e.preventDefault();
    eraseCookie('jwt-access');
    eraseCookie('jwt-refresh');
    window.location.replace('/account/login/');
});

$('#purchase').click(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "PUT",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        url: "/buy/1/",
        data: {},
        success: function (response) {
            console.log(response);
            if (response.error == 'login') {
                window.location.href = '/account/login/'
            }else{
                window.location.reload()
            }
        }
    });
});

$('button[cid]').click(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "DELETE",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        url: "/buy/"+$(this).attr('cid')+"/",
        data: {},
        success: function (response) {
            console.log(response);
            if (response.error == 'login') {
                window.location.href = '/account/login/'
            }else{
                window.location.reload()
            }
        }
    });
});