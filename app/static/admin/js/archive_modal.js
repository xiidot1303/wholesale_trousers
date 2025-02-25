document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('archive-modal');
    var btn = document.createElement('button');
    btn.innerHTML = 'Open Modal';
    btn.onclick = function() {
        modal.style.display = 'block';
    };
    document.querySelector('.object-tools').appendChild(btn);

    var span = document.getElementsByClassName('close')[0];
    span.onclick = function() {
        modal.style.display = 'none';
    };

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    document.getElementById('archive-form').onsubmit = function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        }).then(response => response.json()).then(data => {
            if (data.success) {
                modal.style.display = 'none';
            }
        });
    };
});