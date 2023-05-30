$('.navbar form button[type=submit]').click(function (e) { 
    e.preventDefault();
    window.location.href = '/search/?search='+$('.navbar form input').val()
});