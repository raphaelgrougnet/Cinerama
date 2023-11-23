"use strict";
let numero = 0;
let controler = null;
const lstSuggestion = document.getElementById("listeSuggestions");
const searchbar = document.getElementById("search");
const divSuggestions = document.getElementById("divSuggestions");
const btnSearch = document.getElementById("btnSearch");
const chkName = document.getElementById("chkName");
const chkDate = document.getElementById("chkDate");
const chkNote = document.getElementById("chkNote");
let recherche = ""
const offset = 14

/**
 * Fonction qui permet de récupérer les suggestions de recherche
 * @returns {Promise<void>}
 */
async function recupererSuggestions(){
    ///Affiche le loader
    lstSuggestion.innerHTML = `
        <li class="d-flex justify-content-center"><div class="race-by"></div></li>
    `

    if (controler != null) {
        // Annuler la requête précédente, car on lancera une nouvelle requête
        // à chaque input et on ne veut plus le résultat de la requête précédente.
        controler.abort();
    }

    controler = new AbortController()

    ///Recuperation des suggestions
    let suggestions = await envoyerRequeteAjax("/api/recuperer-suggestions/" + searchbar.value, "GET", {}, controler);

    ///Affichage des suggestions
    ///S'il n'y a pas de suggestions
    if (suggestions.length === 0){
        ///Vide la liste de suggestions
        lstSuggestion.innerHTML = "";
        ///Création d'un li pour afficher qu'il n'y a pas de suggestions
        let li = document.createElement("li");
        li.innerText = "Aucune suggestion";
        lstSuggestion.appendChild(li);
    }
    else {
        ///Vide la liste de suggestions
        lstSuggestion.innerHTML = "";
        ///Création d'un li pour chaque suggestion
        for (let suggestion of suggestions){
            let li = document.createElement("li");
            let a = document.createElement("a");
            a.href = "/film/" + suggestion["_id"];
            a.innerText = suggestion["Title"];
            a.classList.add("stretched-link");
            li.appendChild(a);
            lstSuggestion.appendChild(li);
        }
    }

}

/**
 * Fonction qui permet de gérer l'input de la barre de recherche
 * @returns {Promise<void>}
 */
async function typeSearchHandler(){
    ///Si la recherche contient plus de 2 caractères
    if (searchbar.value.trim().length > 2){
        ///Affiche la div de suggestions
        divSuggestions.classList.remove("cacher");
        ///Recuperate les suggestions
        await recupererSuggestions();
    }
    else {
        ///Cache la div de suggestions
        divSuggestions.classList.add("cacher");
        ///Vide la liste de suggestions
        lstSuggestion.innerHTML = "";
    }
}

/**
 * Fonction qui permet de gérer le click sur le bouton de recherche
 * @returns {Promise<void>}
 */
async function clickSearchHandler(){
    divSuggestions.classList.add("cacher");
    lstSuggestion.innerHTML = "";
    recherche = searchbar.value;
    numero = 0;
    let stringParms = "";
    if (chkName.checked){
        stringParms += "&name=true";
    }
    if (chkDate.checked){
        stringParms += "&date=true";
    }
    if (chkNote.checked){
        stringParms += "&note=true";
    }
    window.location.href = "/films?recherche=" + recherche + stringParms;
    // await afficherEncheres(0, recherche)
    numero = offset;

}

/**
 * Fonction qui permet de fermer le menu de suggestions de recherche
 */
function fermerMenu(){
     // Remplacez 'menu' par l'ID de votre menu

    document.addEventListener('click', function(event) {
    let estClicDansMenu = divSuggestions.contains(event.target); // Vérifie si le clic est à l'intérieur du menu
    estClicDansMenu = searchbar.contains(event.target); // Vérifie si le clic est à l'intérieur du menu

    if (!estClicDansMenu) {
      // Fermer le menu ici
      divSuggestions.classList.add("cacher");
    }
  });
}

async function initialize() {
    fermerMenu();
    searchbar.addEventListener("input", typeSearchHandler);
    searchbar.addEventListener("focus", typeSearchHandler);
    btnSearch.addEventListener("click", clickSearchHandler);
    searchbar.addEventListener("keydown", function(e){
        if (e.key === "Enter"){
            ///Faire la recherche
        }
    })

}

window.addEventListener("load", initialize)
