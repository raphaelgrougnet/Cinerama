document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('submit_commentaire').value.trim() === '' || document.getElementById('submit_commentaire').value.trim().length < 5) {
        document.getElementById('submit_commentaire').setAttribute('disabled', 'disabled');
    }

    document.getElementById('commentaire').addEventListener('input', function() {
        let bouton = document.getElementById('submit_commentaire');
        if (this.value.trim() === '' || this.value.trim().length < 5) {
            bouton.setAttribute('disabled', "disabled");
            
        } else {
            bouton.removeAttribute('disabled');
        }
    });
});