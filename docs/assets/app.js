(function(){
  var root=document.body.dataset.root||'', lang=document.body.dataset.lang||'tr';
  var b=document.getElementById('burger'), n=document.getElementById('nav');
  if(b) b.onclick=function(){n.classList.toggle('open')};
  // search
  var S=document.getElementById('search'), q=document.getElementById('q'), R=document.getElementById('sres'), sel=-1;
  function fold(s){return (s||'').toLocaleLowerCase(lang==='tr'?'tr':'en').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/ı/g,'i')}
  var IDX=(window.SEARCH||[]).filter(function(x){return x.l===lang}).map(function(x){x._t=fold(x.t);x._s=fold(x.s);x._x=fold(x.x);return x});
  function esc(s){return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function hl(s,w){s=esc(s);w.forEach(function(t){if(t.length<2)return;var re=new RegExp('('+t.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+')','ig');s=s.replace(re,'<mark>$1</mark>')});return s}
  function run(){
    var v=q.value.trim(); sel=-1; if(!v){R.innerHTML='';return}
    var w=fold(v).split(/\s+/).filter(Boolean);
    var res=IDX.map(function(x){var sc=0;for(var i=0;i<w.length;i++){var t=w[i];var a=x._t.indexOf(t)>-1?10:0,b=x._s.indexOf(t)>-1?4:0,c=x._x.indexOf(t)>-1?1:0;if(!a&&!b&&!c)return null;sc+=a+b+c}return [sc,x]}).filter(Boolean).sort(function(a,b){return b[0]-a[0]}).slice(0,14);
    R.innerHTML=res.length?res.map(function(r){var x=r[1];return '<a href="'+root+(document.body.dataset.preview?x.u.replace(/\/(#|$)/,'/index.html$1'):x.u)+'"><small>'+esc(x.k)+'</small><b>'+hl(x.t,v.split(/\s+/))+'</b><span>'+hl(x.s,v.split(/\s+/))+'</span></a>'}).join(''):'<div class="none">'+R.dataset.empty+'</div>';
  }
  function open(){S.hidden=false;q.focus();q.select()} function close(){S.hidden=true}
  var sb=document.getElementById('sbtn'); if(sb) sb.onclick=open;
  document.getElementById('sclose').onclick=close;
  S.addEventListener('click',function(e){if(e.target===S)close()});
  q.addEventListener('input',run);
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&S.hidden&&!/input|textarea|select/i.test(document.activeElement.tagName)){e.preventDefault();open()}
    else if(e.key==='Escape')close();
    else if(!S.hidden&&(e.key==='ArrowDown'||e.key==='ArrowUp')){var a=R.querySelectorAll('a');if(!a.length)return;e.preventDefault();sel=(sel+(e.key==='ArrowDown'?1:-1)+a.length)%a.length;a.forEach(function(x,i){x.classList.toggle('sel',i===sel)});a[sel].scrollIntoView({block:'nearest'})}
    else if(!S.hidden&&e.key==='Enter'){var a2=R.querySelectorAll('a');if(a2.length)location.href=a2[Math.max(sel,0)].href}
  });
  // toc highlight
  var links=[].slice.call(document.querySelectorAll('.toc a'));
  if(links.length&&'IntersectionObserver' in window){
    var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(a){a.classList.remove('on')});var a=map[e.target.id];if(a)a.classList.add('on')}})},{rootMargin:'-80px 0px -70% 0px'});
    Object.keys(map).forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el)});
  }
  // glossary filter
  var gf=document.getElementById('glf');
  if(gf) gf.addEventListener('input',function(){var v=fold(gf.value);document.querySelectorAll('.gl').forEach(function(g){g.style.display=!v||fold(g.textContent).indexOf(v)>-1?'':'none'});document.querySelectorAll('.gl-letter').forEach(function(h){h.style.display=v?'none':''})});
})();
