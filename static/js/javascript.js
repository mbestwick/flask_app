// example AJAX call:

function successFunction (results) {
    alert(results);
}

function callBack (evt) {
    evt.preventDefault();

    var formInputs = {'user_id': $("#user").val()};

    $.get('/', formInputs, successFunction);
}

$("some-form").on('submit', callBack);