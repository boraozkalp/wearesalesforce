(function(){
  function $(id){return document.getElementById(id)}
  function v(id){var e=$(id);return e?parseFloat(String(e.value).replace(',','.'))||0:0}
  var L=document.body.dataset.lang||'tr', TR=L==='tr';
  function fmt(n,d){return (Math.round(n*Math.pow(10,d||0))/Math.pow(10,d||0)).toLocaleString(TR?'tr-TR':'en-GB')}
  function on(sel,fn){document.querySelectorAll(sel).forEach(function(el){el.addEventListener('input',fn);el.addEventListener('change',fn)});fn()}
  document.querySelectorAll('[data-copy]').forEach(function(b){b.onclick=function(){var t=$(b.dataset.copy).innerText;navigator.clipboard&&navigator.clipboard.writeText(t);b.textContent=TR?'Kopyalandı ✓':'Copied ✓'}});

  // portfolio
  if(document.querySelector('[data-tool=portfolio]')) on('[data-tool=portfolio] input',function(){
    var cap=v('p_days')*v('p_visits'), remote=v('p_phone')/100;
    var ma=v('p_ma'),mb=v('p_mb'),mc=v('p_mc'),sum=ma+mb+mc||1;
    var avg=(ma*v('p_fa')+mb*v('p_fb')+mc*v('p_fc'))/sum, eff=avg*(1-remote);
    var n=eff>0?cap/eff:0, safe=n*0.87;
    $('p_out').innerHTML='<div class="big">'+fmt(Math.floor(safe))+' – '+fmt(Math.floor(n))+'</div><p>'+(TR?'müşteri: önerilen portföy aralığı (alt değer %13 yeni müşteri ve tahsilat payı bırakır)':'customers: recommended portfolio range (lower value keeps 13% for prospecting and collections)')+'</p>'+
      '<div class="kpis"><div><b>'+fmt(cap)+'</b><span>'+(TR?'aylık ziyaret kapasitesi':'monthly visit capacity')+'</span></div><div><b>'+fmt(avg,1)+'</b><span>'+(TR?'müşteri başı ort. ziyaret/ay':'avg visits/customer/month')+'</span></div>'+
      '<div><b>'+fmt(Math.round(safe*ma/sum))+'</b><span>A</span></div><div><b>'+fmt(Math.round(safe*mb/sum))+'</b><span>B</span></div><div><b>'+fmt(Math.round(safe*mc/sum))+'</b><span>C</span></div></div>'+
      (Math.abs(sum-100)>0.5?'<p style="color:#F3BF5C">'+(TR?'Uyarı: segment payları toplamı %':'Warning: segment shares add up to ')+fmt(sum)+(TR?' — %100 olmalı.':'% — should be 100%.')+'</p>':'');
  });

  // smart
  if(document.querySelector('[data-tool=smart]')) on('[data-tool=smart] input[type=text]',function(){
    var p=['s_when','s_who','s_what','s_how','s_act','s_guard'].map(function(i){return $(i).value.trim()});
    $('s_out').textContent=TR? (p[0]+' '+p[1]+' '+p[2]+' '+p[3]+'; bunu '+p[4]+' ve '+p[5]+' yapacağım.').replace(/\s+/g,' ')
      : ('I will grow '+p[2]+' '+p[1]+' '+p[3]+' '+p[0].charAt(0).toLowerCase()+p[0].slice(1)+', '+p[4]+', '+p[5]+'.').replace(/\s+/g,' ');
  });

  // checklist
  var ck=document.querySelector('[data-tool=checklist]');
  if(ck){var f=function(){var a=ck.querySelectorAll('input[type=checkbox]'),c=ck.querySelectorAll('input:checked').length,p=Math.round(100*c/a.length);$('v_pc').textContent=p+'%';$('v_bar').style.width=p+'%'};on('[data-tool=checklist] input',f);
    ck.querySelector('[data-reset]').onclick=function(){ck.querySelectorAll('input').forEach(function(i){i.checked=false});f()}}

  // coaching
  var co=document.querySelector('[data-tool=coaching]');
  if(co){var sc={};
    var calc=function(){var gs={},tot=0,max=0,n=0;
      co.querySelectorAll('.seg').forEach(function(s){var k=s.dataset.k,g=s.closest('tr').dataset.g;gs[g]=gs[g]||[0,0,0];gs[g][1]+=5;if(sc[k]){gs[g][0]+=sc[k];gs[g][2]++;tot+=sc[k];n++}max+=5});
      var low=[];Object.keys(gs).forEach(function(g){var x=gs[g];var pc=x[2]?Math.round(100*x[0]/(x[2]*5)):null;$('g'+g).textContent=pc===null?'–':pc+'%';if(pc!==null)low.push([pc,co.querySelector('tr.grp[data-g="'+g+'"] td').textContent])});
      low.sort(function(a,b){return a[0]-b[0]});
      var pct=n?Math.round(100*tot/(n*5)):0;
      $('k_out').innerHTML='<div class="big">'+(n?pct+'%':'–')+'</div><p>'+(TR?'Genel puan · '+n+'/30 kriter puanlandı · '+tot+' / '+(n*5)+' puan':'Overall score · '+n+'/30 criteria scored · '+tot+' / '+(n*5)+' points')+'</p><div class="bar"><i style="width:'+pct+'%"></i></div>'+
        (low.length>1?'<p style="margin-top:14px"><b style="color:#F3BF5C">'+(TR?'Öncelikli gelişim alanları:':'Priority development areas:')+'</b> '+low.slice(0,2).map(function(x){return x[1]+' ('+x[0]+'%)'}).join(' · ')+'</p>':'');
    };
    co.querySelectorAll('.seg button').forEach(function(b){b.onclick=function(){var s=b.parentNode;s.querySelectorAll('button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');sc[s.dataset.k]=+b.dataset.v;calc()}});calc();}

  // incentive
  if(document.querySelector('[data-tool=incentive]')){
    var pay=function(a){var thr=v('i_thr'),cap=v('i_cap'),acc=v('i_acc');if(a<thr)return 0;a=Math.min(a,cap);if(a<=100)return 50+50*(a-thr)/Math.max(100-thr,1);return 100+acc*(a-100)};
    on('[data-tool=incentive] input',function(){
      var T=v('i_target'),tot=0,ws=0;
      document.querySelectorAll('#i_kpis tr').forEach(function(r,i){if(!i)return;var w=parseFloat(r.querySelector('.w').value)||0,a=parseFloat(r.querySelector('.a').value)||0;ws+=w;var p=pay(a);var amt=T*w/100*p/100;tot+=amt;r.querySelector('.o').textContent=fmt(amt)+' ('+fmt(p)+'%)'});
      $('i_out').innerHTML='<div class="big">'+fmt(tot)+'</div><p>'+(TR?'toplam prim · hedef primin %':'total payout · ')+fmt(100*tot/(T||1))+(TR?'’i':'% of target bonus')+'</p>'+(Math.abs(ws-100)>0.5?'<p style="color:#F3BF5C">'+(TR?'Ağırlık toplamı %'+fmt(ws)+' — %100 olmalı.':'Weights add up to '+fmt(ws)+'% — should be 100%.')+'</p>':'');
      var W=640,H=220,x0=46,y0=190,xs=function(a){return x0+(a-50)/(150-50)*(W-x0-16)},mx=Math.max(100+v('i_acc')*(v('i_cap')-100),110),ys=function(p){return y0-p/mx*(y0-16)};
      var d='';for(var a=50;a<=150;a+=1){d+=(a===50?'M':'L')+xs(a).toFixed(1)+' '+ys(pay(a)).toFixed(1)}
      var g='<line x1="'+x0+'" y1="'+y0+'" x2="'+(W-10)+'" y2="'+y0+'" stroke="#C9C3B6"/><line x1="'+x0+'" y1="10" x2="'+x0+'" y2="'+y0+'" stroke="#C9C3B6"/>';
      [60,80,100,120,140].forEach(function(a){g+='<text x="'+xs(a)+'" y="'+(y0+18)+'" font-size="12" text-anchor="middle" fill="#5B6578">'+a+'%</text><line x1="'+xs(a)+'" y1="'+y0+'" x2="'+xs(a)+'" y2="'+(y0+4)+'" stroke="#C9C3B6"/>'});
      [0,50,100,150,200].filter(function(p){return p<=mx}).forEach(function(p){g+='<text x="'+(x0-8)+'" y="'+(ys(p)+4)+'" font-size="12" text-anchor="end" fill="#5B6578">'+p+'</text>'});
      g+='<path d="'+d+'" fill="none" stroke="#E5484D" stroke-width="3"/><line x1="'+xs(100)+'" y1="10" x2="'+xs(100)+'" y2="'+y0+'" stroke="#2F7DC0" stroke-dasharray="4 4"/>';
      $('i_chart').innerHTML=g;
    });
  }

  // matrix
  if(document.querySelector('[data-tool=matrix]')) on('[data-tool=matrix] input',function(){
    var r=Math.max(40,Math.min(140,v('m_res'))),b=Math.max(0,Math.min(100,v('m_beh')));
    var hiR=r>=100,hiB=b>=70;
    var Q=TR?{hh:['Yıldız','Sürdürün ve geliştirin: yetki verin, zor hedefler ve mentorluk rolü önerin.'],hl:['Kırılgan başarı','Sonuç iyi ama yöntem zayıf: sonuç kalıcı olmayabilir. Ziyaret kalitesine odaklı koçluk yapın.'],lh:['Doğru yolda','Davranış doğru, sonuç henüz gelmiyor: portföy potansiyelini ve hedefin gerçekçiliğini kontrol edin, sabırla destekleyin.'],ll:['Yoğun müdahale','Hem sonuç hem davranış düşük: net bir 60–90 günlük gelişim planı ve sık koçluk gerekir.']}
      :{hh:['Star','Sustain and stretch: delegate, set challenging goals and offer a mentoring role.'],hl:['Fragile success','Good results, weak method: results may not last. Coach on visit quality.'],lh:['On the right track','Right behaviour, results not yet there: check portfolio potential and target realism, support patiently.'],ll:['Intensive support','Both results and behaviour are low: a clear 60–90 day development plan and frequent coaching are needed.']};
    var k=(hiR?'h':'l')+(hiB?'h':'l'),q=Q[k];
    var W=520,H=380,x0=60,y0=330,xs=function(x){return x0+x/100*(W-x0-20)},ys=function(y){return y0-(y-40)/100*(y0-20)};
    var c=function(x,y,w,h,f,t){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" fill="'+f+'" rx="6"/><text x="'+(x+12)+'" y="'+(y+24)+'" font-size="14" font-weight="700" fill="#041E41">'+t+'</text>'};
    var mx=xs(70),my=ys(100);
    var g=c(x0,20,mx-x0-3,my-23,k==='hl'?'#FBE3A6':'#F5F2EC',Q.hl[0])+c(mx,20,W-20-mx,my-23,k==='hh'?'#CFE3F6':'#F5F2EC',Q.hh[0])+c(x0,my,mx-x0-3,y0-my,k==='ll'?'#F8C9BC':'#F5F2EC',Q.ll[0])+c(mx,my,W-20-mx,y0-my,k==='lh'?'#D6E9C9':'#F5F2EC',Q.lh[0]);
    g+='<text x="'+((x0+W-20)/2)+'" y="'+(y0+36)+'" text-anchor="middle" font-size="13" fill="#5B6578">'+(TR?'Davranış kalitesi →':'Behaviour quality →')+'</text><text transform="translate(20 '+((20+y0)/2)+') rotate(-90)" text-anchor="middle" font-size="13" fill="#5B6578">'+(TR?'Sonuç →':'Results →')+'</text>';
    g+='<circle cx="'+xs(b)+'" cy="'+ys(r)+'" r="11" fill="#E5484D" stroke="#fff" stroke-width="3"/>';
    $('m_chart').innerHTML=g;
    $('m_out').innerHTML='<div class="big">'+q[0]+'</div><p>'+q[1]+'</p><p class="note" style="color:#9FB0CC">'+(TR?'Eşikler: sonuç %100, davranış %70. Kendi standartlarınıza göre uyarlayın.':'Thresholds: results 100%, behaviour 70%. Adapt to your own standards.')+'</p>';
  });

  // funnel
  if(document.querySelector('[data-tool=funnel]')) on('[data-tool=funnel] input',function(){
    var r=[v('f_r1'),v('f_r2'),v('f_r3'),v('f_r4'),v('f_r5')].map(function(x){return Math.max(x,1)/100});
    var st=[v('f_goal')];for(var i=4;i>=0;i--)st.unshift(st[0]/r[i]);
    st=st.map(function(x){return Math.ceil(x)});
    var lab=TR?['Taranacak işletme','Nitelikli aday','İlk ziyaret','Deneme siparişi','İkinci sipariş','Düzenli müşteri']:['Businesses to canvass','Qualified prospects','First visits','Trial orders','Second orders','Regular customers'];
    var perDay=st[0]/Math.max(v('f_days'),1), visits=st[2]+st[3];
    $('f_out').innerHTML='<div class="big">'+fmt(st[0])+'</div><p>'+(TR?'işletme taranmalı · günde yaklaşık '+fmt(perDay,1)+' tarama':'businesses to canvass · about '+fmt(perDay,1)+' per field day')+'</p><div class="kpis">'+st.slice(1).map(function(x,i){return '<div><b>'+fmt(x)+'</b><span>'+lab[i+1]+'</span></div>'}).join('')+'<div><b>'+fmt(visits)+'</b><span>'+(TR?'satış ziyareti (ilk + takip)':'sales visits (first + follow-up)')+'</span></div></div>';
    var W=640,mx=st[0],g='',cols=['#041E41','#173A6B','#2F7DC0','#4697D8','#F3BF5C','#E5484D'];
    st.forEach(function(x,i){var w=Math.max(40,(W-200)*x/mx),y=8+i*41;g+='<rect x="'+((W-200-w)/2)+'" y="'+y+'" width="'+w+'" height="34" rx="6" fill="'+cols[i]+'"/><text x="'+((W-200)/2)+'" y="'+(y+22)+'" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">'+fmt(x)+'</text><text x="'+(W-188)+'" y="'+(y+22)+'" font-size="13" fill="#041E41">'+lab[i]+'</text>'});
    $('f_chart').innerHTML=g;
  });
})();
