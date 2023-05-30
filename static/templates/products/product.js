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

$('.buy').click(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin',
        url: "/buy/1/",
        data: {'id': window.location.pathname.slice(1,-1).slice(window.location.pathname.slice(1,-1).indexOf('/')+1)},
        success: function (response) {
            if (response.error == 'login') {
                window.location.href = '/account/login/'
            }else{
                window.location.reload()
            }
        }
    });
});

$('form button').click(function (e) { 
    e.preventDefault();
    $.ajax({
        type: "POST",
        headers: {'X-CSRFToken': csrftoken},
        url: "/comment/1/",
        mode: 'same-origin',
        data: {'text': $('textarea').val(), 'id': window.location.pathname.slice(1,-1).slice(window.location.pathname.slice(1,-1).indexOf('/')+1)},
        success: function (response) {
            if (response.error != 'empty') {
                if (response.error == 'login') {
                    window.location.href = '/account/login/'
                }else{
                    window.location.reload()
                }  
            } 
        }
    });
});

$('.delete').click(function (e) { 
    e.preventDefault();
    console.log($(this).attr('cid'));
    $.ajax({
        type: "DELETE",
        headers: {'X-CSRFToken': csrftoken},
        url: "/comment/"+$(this).attr('cid')+"/",
        mode: 'same-origin',
        data: {},
        success: function (response) {
            if (response.error == 'login') {
                window.location.href = '/account/login/'
            }else{
                window.location.reload()
            }  
        }
    });
});