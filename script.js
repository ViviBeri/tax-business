const btn=document.getElementById('langBtn');let tamil=false;
function setLang(){
  document.querySelectorAll('[data-en]').forEach(el=>{el.innerHTML=tamil?el.dataset.ta:el.dataset.en});
  document.documentElement.lang=tamil?'ta':'en'; btn.textContent=tamil?'English':'தமிழ்';
}
btn.addEventListener('click',()=>{tamil=!tamil;setLang()});
document.getElementById('year').textContent=new Date().getFullYear();