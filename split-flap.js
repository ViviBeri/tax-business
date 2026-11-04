(function(){
"use strict";
var reduced=window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll("[data-splitflap]").forEach(function(line){
 var phrase=line.getAttribute("data-splitflap")||line.textContent;
 var chars=Array.from(phrase);
 line.setAttribute("aria-label",phrase);
 line.textContent="";
 chars.forEach(function(char,index){
  var tile=document.createElement("span");
  tile.className="flap-char"+(char===" "?" is-space":"")+(/[.,]/.test(char)?" is-punct":"");
  tile.setAttribute("aria-hidden","true");
  tile.textContent=char;
  line.appendChild(tile);
  if(!reduced&&char!==" ") {
   window.setTimeout(function(){
    tile.classList.add("is-flipping");
    window.setTimeout(function(){tile.classList.remove("is-flipping");},240);
   },index*45);
  }
 });
});
})();