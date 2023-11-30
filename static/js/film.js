"use strict";


window.addEventListener("load", function() {
    var btnVisionne = document.getElementById('btnVisionne');
    var iElement = btnVisionne.querySelector('i');

    btnVisionne.addEventListener('mouseover', function() {
        if (iElement.classList.contains('bi-eye-fill')) {
            iElement.classList.remove('bi-eye-fill');
            iElement.classList.add('bi-eye-slash-fill');
        } else if (iElement.classList.contains('bi-eye-slash-fill')) {
            iElement.classList.remove('bi-eye-slash-fill');
            iElement.classList.add('bi-eye-fill');
            
        }
    });

    btnVisionne.addEventListener('mouseout', function() {
        if (iElement.classList.contains('bi-eye-fill')) {
            iElement.classList.remove('bi-eye-fill');
            iElement.classList.add('bi-eye-slash-fill');
        } else if (iElement.classList.contains('bi-eye-slash-fill')) {
            iElement.classList.remove('bi-eye-slash-fill');
            iElement.classList.add('bi-eye-fill');
        }
    });
});

window.addEventListener("load", initialize)