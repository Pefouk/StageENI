function sauvegarder(lien) {
    $.ajax({
        url: lien,
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data.error !== 1) {
                let doc = document.getElementById(data.id + '-p');
                if (data.save !== 1) {
                    doc.className = "far fa-star fa-3x"
                } else {
                    doc.className = "fas fa-star fa-3x"
                }
            }
        }
    });
}

function administrateurprofil(lien, pseudo) {
    $.ajax({
        url: lien,
        type: "POST",
        dataType: 'json',
        success: function (data) {
            if (data.error !== 1) {
                let doc = document.getElementById(pseudo + '-admin')
                let check = document.getElementById(pseudo + '-check')

                console.log(check);
                if (data.admin === 1) {
                    doc.textContent = 'Retirer les droits administrateurs'
                } else {
                    doc.textContent = 'Donner les droits administrateurs'
                }
            }
        }
    });
}

function sabonner(lien) {
    $.ajax({
        url: lien,
        type: "POST",
        dataType: 'json',
        success: function (data) {
            let doc = document.getElementById('abonnement');
            console.log(data);
            if (data.abonnement === 1) {
                doc.innerText = "Se désabonner"
            } else {
                doc.innerText = "S'abonner"
            }
        }
    })
}

function desactiverOnglets() {
    let docs = document.getElementsByClassName('onglet');
    for (let doc of docs) {
        if (doc.classList.contains('active'))
            doc.classList.remove('active');
    }
}

function chargerOnglet(lien, type) {
    let doc = document.getElementById(type);
    if (!doc.classList.contains('active')) {
        desactiverOnglets();
        doc.classList.add('active');
        doc = document.getElementById('publications');
        doc.remove();
        $.ajax({
            url: lien,
            type: "POST",
            dataType: "html",
            success: function (data) {
                document.getElementById('onglets').insertAdjacentHTML("afterend", data);
            }
        })
    }
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