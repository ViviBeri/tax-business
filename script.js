(function(){
var d=document,cur='en';
var ev=function(n,p){try{if(window.gtag)gtag('event',n,p||{})}catch(e){}};
var q=function(s){return d.querySelectorAll(s)};
var mb=d.getElementById('menuBtn'),nv=d.getElementById('mainNav');
if(mb&&nv){mb.addEventListener('click',function(){var o=nv.classList.toggle('open');mb.setAttribute('aria-expanded',o)});
nv.addEventListener('click',function(e){if(e.target.closest('a'))nv.classList.remove('open')})}
q('.yr').forEach(function(e){e.textContent=new Date().getFullYear()});
d.addEventListener('click',function(e){var a=e.target.closest('a');if(!a)return;
if(a.classList.contains('lang')){ev('language_switch',{language:a.getAttribute('hreflang')});return}
var h=a.href||'',l=a.dataset.loc||'page',p={link_location:l,page_path:location.pathname};
if(h.indexOf('wa.me')>-1)ev('whatsapp_click',p);
else if(h.indexOf('tel:')===0)ev('call_click',p);
else if(a.classList.contains('service-card'))ev('select_service',{service:a.dataset.service,link_location:'home-card'})});
var sv=d.getElementById('service');
if(sv)sv.addEventListener('change',function(){if(sv.value)ev('select_service',{service:sv.value,link_location:'form'})});
var f=d.getElementById('enquiryForm');
if(f)f.addEventListener('submit',function(e){e.preventDefault();var g=new FormData(f),s=g.get('service')||'Not selected';
var m='New Website Enquiry\nService: '+s+'\nName: '+g.get('name')+'\nPhone: '+g.get('phone')+'\nRequirement: '+(g.get('message')||'-');
ev('generate_lead',{service:s,link_location:'form'});
var u='https://wa.me/919003633696?text='+encodeURIComponent(m);
if(!window.open(u,'_blank'))location.href=u});
})();
