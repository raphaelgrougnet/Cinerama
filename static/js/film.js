"use strict";


window.addEventListener("load", function() {
    var btnVisionne = document.getElementById('btnVisionne');
    var iElement = btnVisionne.querySelector('i');

    btnVisionne.addEventListener('mouseover', function() {
        if (iElement.classList.contains('bi-eye-fill')) {
            iElement.classList.remove('bi-eye-fill');
            iElement.classList.add('bi-eye-slash-fill');
            iElement.classList.remove('text-info');

        } else if (iElement.classList.contains('bi-eye-slash-fill')) {
            iElement.classList.remove('bi-eye-slash-fill');
            iElement.classList.add('bi-eye-fill');
            iElement.classList.add('text-info');

            
        }
    });

    btnVisionne.addEventListener('mouseout', function() {
        if (iElement.classList.contains('bi-eye-fill')) {
            iElement.classList.remove('bi-eye-fill');
            iElement.classList.add('bi-eye-slash-fill');
            iElement.classList.remove('text-info');
        } else if (iElement.classList.contains('bi-eye-slash-fill')) {
            iElement.classList.remove('bi-eye-slash-fill');
            iElement.classList.add('bi-eye-fill');
            iElement.classList.add('text-info');

        }
    });
});

window.addEventListener("load", function() {
    var btnLikes = document.getElementsByClassName('btn-like');
    var btnDislikes = document.getElementsByClassName('btn-dislike');
    
    Array.from(btnLikes).forEach(function(btnLike) {
        var iElementLike = btnLike.querySelector('i');

        btnLike.addEventListener('mouseover', function() {
            if (iElementLike.classList.contains('bi-hand-thumbs-up')) {
                iElementLike.classList.remove('bi-hand-thumbs-up');
                iElementLike.classList.add('bi-hand-thumbs-up-fill');
            } else if (iElementLike.classList.contains('bi-hand-thumbs-up-fill')) {
                iElementLike.classList.remove('bi-hand-thumbs-up-fill');
                iElementLike.classList.add('bi-hand-thumbs-up');
            }
        });

        btnLike.addEventListener('mouseout', function() {
            if (iElementLike.classList.contains('bi-hand-thumbs-up')) {
                iElementLike.classList.remove('bi-hand-thumbs-up');
                iElementLike.classList.add('bi-hand-thumbs-up-fill');
            } else if (iElementLike.classList.contains('bi-hand-thumbs-up-fill')) {
                iElementLike.classList.remove('bi-hand-thumbs-up-fill');
                iElementLike.classList.add('bi-hand-thumbs-up');
            }
        });
    });

    Array.from(btnDislikes).forEach(function(btnDislike) {
        var iElementDislike = btnDislike.querySelector('i');

        btnDislike.addEventListener('mouseover', function() {
            if (iElementDislike.classList.contains('bi-hand-thumbs-down')) {
                iElementDislike.classList.remove('bi-hand-thumbs-down');
                iElementDislike.classList.add('bi-hand-thumbs-down-fill');
            } else if (iElementDislike.classList.contains('bi-hand-thumbs-down-fill')) {
                iElementDislike.classList.remove('bi-hand-thumbs-down-fill');
                iElementDislike.classList.add('bi-hand-thumbs-down');
            }
        });

        btnDislike.addEventListener('mouseout', function() {
            if (iElementDislike.classList.contains('bi-hand-thumbs-down')) {
                iElementDislike.classList.remove('bi-hand-thumbs-down');
                iElementDislike.classList.add('bi-hand-thumbs-down-fill');
            } else if (iElementDislike.classList.contains('bi-hand-thumbs-down-fill')) {
                iElementDislike.classList.remove('bi-hand-thumbs-down-fill');
                iElementDislike.classList.add('bi-hand-thumbs-down');
            }
        });
    });
});

window.addEventListener("load", initialize)