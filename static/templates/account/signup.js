$('input[id]').addClass('form-control');
$('input[for]').addClass('form-label');
$('input[id=id_password1], input[id=id_password2]').attr('type', 'password');
$('input[id] ~ .invalid-feedback').prev().addClass('is-invalid');
$('.form-group').addClass('mb-3');

