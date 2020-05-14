function sauvegarder(lien, username) {
    $.ajax({
        url: lien,
        data: {
            'username': username,
        },
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data.error !== 1) {
                let doc = document.getElementById(data.id + '-p');
                console.log(doc);
                if (data.save !== 1) {
                    doc.className = "far fa-star fa-3x"
                } else {
                    doc.className = "fas fa-star fa-3x"
                }
            }
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}