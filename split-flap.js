(function(){
"use strict";
var reduced=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
var alphabet=" ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-";
document.querySelectorAll("[data-splitflap]").forEach(function(line){
 var phrase=line.getAttribute("data-splitflap")||line.textContent, chars=Array.from(phrase);
 line.setAttribute("aria-label",phrase); line.textContent="";
 chars.forEach(function(char,index){
  var tile=document.createElement("span"); tile.className="flap-char"+(char===" "?" is-space":"")+(/[.,]/.test(char)?" is-punct":""); tile.setAttribute("aria-hidden","true");
  tile.textContent=reduced||char===" "?char:alphabet[Math.floor(Math.random()*alphabet.length)]; line.appendChild(tile);
  if(!reduced&&char!==" ") window.setTimeout(function(){var count=0,timer=window.setInterval(function(){count++;tile.classList.remove("is-flipping");void tile.offsetWidth;tile.classList.add("is-flipping");tile.textContent=count>=8?char:alphabet[Math.floor(Math.random()*alphabet.length)];if(count>=8){window.clearInterval(timer);tile.classList.remove("is-flipping");}},120);},index*55);
 });
});
})();
