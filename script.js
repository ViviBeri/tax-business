document.getElementById('year').textContent=new Date().getFullYear();
const btn=document.getElementById('langBtn');
let tamil=false;
btn?.addEventListener('click',()=>{tamil=!tamil;document.documentElement.lang=tamil?'ta':'en';btn.textContent=tamil?'English':'தமிழ்';document.querySelectorAll('[data-en]').forEach(el=>{el.innerHTML=tamil?el.dataset.ta:el.dataset.en});});
document.getElementById('enquiryForm')?.addEventListener('submit',e=>{e.preventDefault();const f=new FormData(e.target);const msg=`Hello Vivian, I would like assistance.\nName: ${f.get('name')}\nBusiness / Requirement: ${f.get('requirement')}\nPhone: ${f.get('phone')||'Not provided'}`;window.open('https://wa.me/919003633696?text='+encodeURIComponent(msg),'_blank');});
