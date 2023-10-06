"use strict";

var leftArrowRecent = document.getElementById("left-arrow-recents");
var rightArrowRecent = document.getElementById("right-arrow-recents");
var leftArrowBests = document.getElementById("left-arrow-bests");
var rightArrowBests = document.getElementById("right-arrow-bests");

var scrollerBests = document.getElementById("scroller-bests");
var scrollerRecent = document.getElementById("scroller-recents");

leftArrowRecent.addEventListener("click", function() {
    scrollerRecent.scrollBy(-1277, 0);
});

rightArrowRecent.addEventListener("click", function() {
    scrollerRecent.scrollBy(1277, 0);
});

leftArrowBests.addEventListener("click", function() {
    scrollerBests.scrollBy(-1277, 0);
});

rightArrowBests.addEventListener("click", function() {
    scrollerBests.scrollBy(1277, 0);
});