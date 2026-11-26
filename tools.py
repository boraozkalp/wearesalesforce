"""Araç sayfaları (TR/EN). HTML + data-* öznitelikleri; davranış assets/tools.js içinde."""

def F(id, label, val, hint='', typ='number', step='1', mn='0'):
    h = f'<small>{hint}</small>' if hint else ''
    return f'<div class="field"><label for="{id}">{label}</label><input id="{id}" type="{typ}" value="{val}" step="{step}" min="{mn}">{h}</div>'

def SEL(id, label, opts):
    o = ''.join(f'<option value="{v}">{t}</option>' for v, t in opts)
    return f'<div class="field"><label for="{id}">{label}</label><select id="{id}">{o}</select></div>'

# ---------- 1. Portfolio capacity
def portfolio(L):
    tr = L == 'tr'
    s = (lambda a, b: a if tr else b)
    return f'''<div class="tool-card" data-tool="portfolio" data-lang="{L}">
<h2>{s('1. Saha kapasitesi', '1. Field capacity')}</h2>
<div class="fields">
{F('p_days', s('Ayda sahada geçen gün', 'Field days per month'), 17, s('Ofis, toplantı, izin düşülmüş', 'After office, meetings, leave'))}
{F('p_visits', s('Günlük kaliteli ziyaret', 'Quality visits per day'), 6, s('Hazırlıklı, hedefli ziyaret', 'Prepared, objective-led visits'))}
{F('p_phone', s('Telefon/uzaktan temas oranı %', 'Remote contact share %'), 0, s('Ziyaretin yerini alan temaslar', 'Contacts replacing a visit'))}
</div>
<h2 style="margin-top:24px">{s('2. Segment bazlı ziyaret sıklığı (ayda)', '2. Visit frequency by segment (per month)')}</h2>
<div class="fields">
{F('p_fa', s('A segmenti – ayda ziyaret', 'Segment A – visits/month'), 4, s('Yüksek potansiyel, haftalık', 'High potential, weekly'), step='0.5')}
{F('p_fb', s('B segmenti – ayda ziyaret', 'Segment B – visits/month'), 2, s('İki haftada bir', 'Every two weeks'), step='0.5')}
{F('p_fc', s('C segmenti – ayda ziyaret', 'Segment C – visits/month'), 1, s('Ayda bir', 'Monthly'), step='0.5')}
</div>
<h2 style="margin-top:24px">{s('3. Portföy karması (%)', '3. Portfolio mix (%)')}</h2>
<div class="fields">
{F('p_ma', s('A segmenti payı %', 'Share of A %'), 20)}
{F('p_mb', s('B segmenti payı %', 'Share of B %'), 35)}
{F('p_mc', s('C segmenti payı %', 'Share of C %'), 45)}
</div>
<div class="result" id="p_out"></div>
<p class="note">{s('Formül: aylık ziyaret kapasitesi ÷ (uzaktan temas düşülmüş) müşteri başına ortalama aylık ziyaret. Sonucu yeni müşteri kazanımı ve tahsilat gibi ek görevler için %10–15 aşağı yuvarlamanızı öneririz.', 'Formula: monthly visit capacity ÷ average monthly visits per customer (net of remote contacts). We suggest rounding the result down by 10–15% to leave room for prospecting and collections.')}</p>
</div>'''

# ---------- 2. SMART
def smart(L):
    tr = L == 'tr'; s = (lambda a, b: a if tr else b)
    return f'''<div class="tool-card" data-tool="smart" data-lang="{L}">
<h2>{s('Hedefinizi parçalara ayırın', 'Break your target into parts')}</h2>
<div class="fields">
{F('s_when', s('Zaman (Ne zamana kadar?)', 'Time (By when?)'), s('Haziran sonuna kadar', 'By the end of June'), typ='text')}
{F('s_who', s('Kapsam (Hangi müşteri grubu?)', 'Scope (Which customers?)'), s('A segmenti restoran portföyünde', 'in the A-segment restaurant portfolio'), typ='text')}
{F('s_what', s('Ölçüt (Hangi KPI?)', 'Metric (Which KPI?)'), s('donuk ürün cirosunu', 'frozen category sales'), typ='text')}
{F('s_how', s('Hedef değer ve fiil', 'Target value'), s('%12 artıracağım', 'by 12%'), typ='text')}
{F('s_act', s('Aksiyon (Nasıl?)', 'Action (How?)'), s('15 müşteride yeni kategori denemesiyle', 'by trialling the category with 15 customers'), typ='text')}
{F('s_guard', s('Koruma kuralı (Neyi bozmadan?)', 'Guardrail (Without breaking what?)'), s('brüt kâr marjını %18’in altına düşürmeden', 'without letting gross margin fall below 18%'), typ='text')}
</div>
<div class="out" id="s_out"></div>
<h3>{s('SMART kontrolü', 'SMART check')}</h3>
<ul class="cl" id="s_chk">
<li><input type="checkbox" id="c1"><label for="c1"><b>S</b> – {s('Spesifik: Tek bir müşteri grubu ve tek bir KPI içeriyor mu?', 'Specific: does it name one customer group and one KPI?')}</label></li>
<li><input type="checkbox" id="c2"><label for="c2"><b>M</b> – {s('Ölçülebilir: Başlangıç değeri sistemde var mı?', 'Measurable: is the baseline available in the system?')}</label></li>
<li><input type="checkbox" id="c3"><label for="c3"><b>A</b> – {s('Ulaşılabilir: Portföy potansiyeli ve geçmiş trendle uyumlu mu?', 'Achievable: is it consistent with portfolio potential and past trend?')}</label></li>
<li><input type="checkbox" id="c4"><label for="c4"><b>R</b> – {s('İlgili: Şirket stratejisine ve kârlılığa hizmet ediyor mu?', 'Relevant: does it serve company strategy and profitability?')}</label></li>
<li><input type="checkbox" id="c5"><label for="c5"><b>T</b> – {s('Zamana bağlı: Ara kontrol tarihleri belli mi?', 'Time-bound: are interim checkpoints set?')}</label></li>
</ul>
<div class="btns"><button class="btn sec" data-copy="s_out">{s('Metni kopyala', 'Copy text')}</button></div>
</div>'''

# ---------- 3. Visit checklist
VC = {
 'tr': [('Ziyaret öncesi', ['Müşteri kartını ve son 3 ayın alım geçmişini inceledim', 'Son ziyarette verilen sözleri ve açık konuları kontrol ettim', 'Bu ziyaret için tek cümlelik ana hedefimi yazdım', 'Alternatif (yedek) hedefimi belirledim', 'Müşterinin henüz almadığı 2–3 kategoriyi işaretledim', 'Güncel kampanya ve fiyatları kontrol ettim', 'Teklif, numune ve katalog gibi araçlarımı hazırladım', 'Beklediğim 2 itiraz ve yanıtlarını not ettim']),
        ('Görüşme sırasında', ['Karar vericiyle konuştum', 'Ziyaretin amacını ilk dakikada netleştirdim', 'En az 3 açık soru sordum', 'Not aldım ve anahtar kelimeleri işaretledim', 'Önerimi müşterinin kazancıyla ilişkilendirdim', 'İtirazı dinleyip yeniden ifade ettikten sonra yanıtladım', 'Somut bir taahhüt veya sonraki adım aldım']),
        ('Ziyaret sonrası', ['Ziyaret notunu aynı gün sisteme girdim', 'Verilen sözleri tarihleriyle takvime ekledim', 'İlgili birimlere (operasyon, finans, kategori) bilgi verdim', 'Ziyareti kendi kendime 1 cümleyle değerlendirdim'])],
 'en': [('Before the visit', ['I reviewed the customer record and last 3 months of purchases', 'I checked promises made and open items from the last visit', 'I wrote my one-sentence main objective for this visit', 'I set a fallback objective', 'I flagged 2–3 categories the customer does not buy yet', 'I checked current promotions and prices', 'I prepared my tools: offer, samples, catalogue', 'I noted 2 expected objections and my responses']),
        ('During the visit', ['I spoke with the decision-maker', 'I made the purpose of the visit clear in the first minute', 'I asked at least 3 open questions', 'I took notes and marked key words', 'I linked my proposal to the customer’s gain', 'I listened to and rephrased the objection before answering', 'I secured a concrete commitment or next step']),
        ('After the visit', ['I logged the visit note in the system the same day', 'I put promises in the calendar with dates', 'I informed the relevant teams (operations, finance, category)', 'I evaluated the visit in one sentence'])],
}
def checklist(L):
    s = (lambda a, b: a if L == 'tr' else b)
    parts = []; k = 0
    for title, items in VC[L]:
        li = ''
        for it in items:
            k += 1; li += f'<li><input type="checkbox" id="v{k}"><label for="v{k}">{it}</label></li>'
        parts.append(f'<div class="tool-card"><h2>{title}</h2><ul class="cl">{li}</ul></div>')
    return f'''<div data-tool="checklist" data-lang="{L}"><div class="progress"><div style="display:flex;justify-content:space-between;font-weight:700;font-size:14px"><span>{s('Hazırlık durumu', 'Readiness')}</span><span id="v_pc">0%</span></div><div class="bar" style="background:#E4E0D8"><i id="v_bar" style="width:0"></i></div></div>
{''.join(parts)}<div class="btns"><button class="btn sec" onclick="window.print()">{s('Yazdır / PDF', 'Print / PDF')}</button><button class="btn ghost" style="color:var(--ink);border-color:var(--line)" data-reset>{s('Sıfırla', 'Reset')}</button></div></div>'''

# ---------- 4. Coaching observation form
CF = {
 'tr': [('Ziyarete hazırlık', ['Müşteri bilgilerini gözden geçirme', 'Ziyaret hedefini belirleme', 'Argümanları hazırlama (satış planı)', 'Araçları hazırlama (teklif, liste, tahsilat bilgisi)']),
        ('Açılış ve sunum', ['Karar verici kişiyle konuşma', 'Ziyaret hedefini açıkça ifade etme', 'Hazırlanan teklifin avantajlarını belirtme']),
        ('Bilgi toplama', ['Hedefe yönelik önemli bilgileri toplama', 'Açık soruları uygun kullanma', 'Kapalı soruları uygun kullanma', 'Etkin dinleme', 'Not alma', 'Kategori bazında alım potansiyelini çıkarma']),
        ('İkna', ['Müşterinin durumunu ve ihtiyaçlarını fark etme', 'İhtiyaca uygun fikir önerme', 'İkna edici mantık kurma', 'Avantajları somut gösterme', 'Sonuca bağlama']),
        ('İtiraz yönetimi', ['İtirazı dinleyip yeniden ifade etme', 'İtirazları önceliklendirme', 'Gerçek itirazı ayırt etme', 'Uygun şekilde yanıt verme']),
        ('Kapanış', ['Net noktalarda anlaşmaya varma', 'Sonraki adımları ve tarihleri belirleme', 'Açık soru veya ihtiyaç bırakmama']),
        ('Bilgi işleme', ['Uzlaşılan konuları hemen ele alma', 'Sonraki ziyaret için hedef belirleme', 'Bilgileri sisteme girme']),
        ('Performans analizi', ['Satış sonuçlarını analiz etme', 'Ziyareti genel olarak değerlendirme'])],
 'en': [('Visit preparation', ['Reviewing customer information', 'Setting the visit objective', 'Preparing arguments (sales plan)', 'Preparing tools (offer, list, collection info)']),
        ('Opening and presentation', ['Speaking with the decision-maker', 'Stating the visit objective clearly', 'Presenting the advantages of the prepared offer']),
        ('Gathering information', ['Collecting information relevant to the objective', 'Using open questions appropriately', 'Using closed questions appropriately', 'Active listening', 'Taking notes', 'Estimating purchase potential by category']),
        ('Persuasion', ['Recognising the customer’s situation and needs', 'Proposing ideas that fit the need', 'Building persuasive logic', 'Showing benefits concretely', 'Linking to a conclusion']),
        ('Handling objections', ['Listening to and rephrasing the objection', 'Prioritising objections', 'Identifying the real objection', 'Responding appropriately']),
        ('Closing', ['Agreeing on clear points', 'Setting next steps and dates', 'Leaving no open question or need']),
        ('Processing information', ['Addressing agreed issues immediately', 'Setting the objective for the next visit', 'Entering information into the system']),
        ('Performance analysis', ['Analysing sales results', 'Evaluating the visit overall'])],
}
def coaching(L):
    s = (lambda a, b: a if L == 'tr' else b)
    rows = ''; k = 0
    for gi, (g, items) in enumerate(CF[L]):
        rows += f'<tr class="grp" data-g="{gi}"><td>{gi+1}. {g}</td><td class="pc" id="g{gi}">–</td></tr>'
        for it in items:
            k += 1
            seg = ''.join(f'<button type="button" data-v="{v}">{v}</button>' for v in range(1, 6))
            rows += f'<tr data-g="{gi}"><td>{k}. {it}</td><td class="s"><div class="seg" data-k="{k}">{seg}</div></td></tr>'
    return f'''<div data-tool="coaching" data-lang="{L}">
<div class="tool-card"><div class="fields">
{F('k_coachee', s('Koçluk yapılan kişi (isteğe bağlı)', 'Coachee (optional)'), '', typ='text')}
{F('k_date', s('Tarih', 'Date'), '', typ='date')}
{F('k_n', s('Gözlenen ziyaret sayısı', 'Visits observed'), 6)}
</div><p class="note">{s('Ölçek: 5 Çok iyi · 4 İyi · 3 Orta · 2 Zayıf · 1 Çok zayıf. Bir günde en az 6 ziyaret gözlemlemenizi, puanı her ziyaretten sonra değil gün sonunda genel gözleme göre vermenizi öneririz.', 'Scale: 5 Very good · 4 Good · 3 Fair · 2 Weak · 1 Very weak. We suggest observing at least 6 visits in a day and scoring on the overall picture at day end, not after each visit.')}</p></div>
<div class="tool-card"><table class="score-t"><tr><th>{s('Kriter', 'Criterion')}</th><th>{s('Puan', 'Score')}</th></tr>{rows}</table></div>
<div class="result" id="k_out"></div>
<div class="tool-card"><h2>{s('Koçluk notu', 'Coaching note')}</h2><div class="fields" style="grid-template-columns:1fr">
<div class="field"><label>{s('Güçlü yönler', 'Strengths')}</label><textarea rows="3"></textarea></div>
<div class="field"><label>{s('Gelişim alanları (en fazla 2)', 'Development areas (max 2)')}</label><textarea rows="3"></textarea></div>
<div class="field"><label>{s('Anlaşılan aksiyon planı ve tarih', 'Agreed action plan and date')}</label><textarea rows="3"></textarea></div></div>
<div class="btns"><button class="btn sec" onclick="window.print()">{s('Yazdır / PDF', 'Print / PDF')}</button></div><p class="note">{s('Veriler tarayıcınızdan dışarı gönderilmez; sayfayı kapattığınızda silinir.', 'Data never leaves your browser and is cleared when you close the page.')}</p></div>
</div>'''

# ---------- 5. Incentive simulator
def incentive(L):
    s = (lambda a, b: a if L == 'tr' else b)
    return f'''<div class="tool-card" data-tool="incentive" data-lang="{L}">
<h2>{s('Prim kurgusu', 'Scheme design')}</h2>
<div class="fields">
{F('i_target', s('Hedef prim (yıllık, tam başarıda)', 'Target bonus (annual, at 100%)'), 60000, s('Para birimi fark etmez', 'Any currency'))}
{F('i_thr', s('Eşik: bu başarının altında prim yok (%)', 'Threshold: no bonus below (%)'), 80)}
{F('i_cap', s('Üst sınır: azami başarı (%)', 'Cap: maximum achievement (%)'), 130)}
{F('i_acc', s('Hedef üstü hızlandırıcı (x)', 'Above-target accelerator (x)'), 2, s('Hedefin üstündeki her 1 puan için prim puanı', 'Bonus points per point above target'), step='0.1')}
</div>
<h2 style="margin-top:24px">{s('KPI ağırlıkları ve gerçekleşme', 'KPI weights and achievement')}</h2>
<table class="score-t" id="i_kpis"><tr><th>KPI</th><th>{s('Ağırlık %', 'Weight %')}</th><th>{s('Gerçekleşme %', 'Achievement %')}</th><th>{s('Prim', 'Payout')}</th></tr>
<tr><td>{s('Ciro', 'Sales')}</td><td><input class="w" value="40" type="number"></td><td><input class="a" value="104" type="number"></td><td class="o"></td></tr>
<tr><td>{s('Brüt kâr', 'Gross profit')}</td><td><input class="w" value="25" type="number"></td><td><input class="a" value="97" type="number"></td><td class="o"></td></tr>
<tr><td>{s('Aktif müşteri / penetrasyon', 'Active customers / penetration')}</td><td><input class="w" value="20" type="number"></td><td><input class="a" value="112" type="number"></td><td class="o"></td></tr>
<tr><td>{s('Tahsilat / vadesi geçmiş', 'Collections / overdue')}</td><td><input class="w" value="15" type="number"></td><td><input class="a" value="78" type="number"></td><td class="o"></td></tr>
</table>
<div class="result" id="i_out"></div>
<div class="fig"><svg id="i_chart" viewBox="0 0 640 220"></svg><figcaption>{s('Başarı oranına göre prim eğrisi (KPI başına)', 'Payout curve by achievement (per KPI)')}</figcaption></div>
<p class="note">{s('Öneri: en fazla 4 KPI, her birinin ağırlığı en az %15. Eşik ve üst sınır, prim bütçesini öngörülebilir tutar; hızlandırıcı hedef üstü performansı ödüllendirir.', 'Tip: no more than 4 KPIs, each weighted at least 15%. The threshold and cap keep the bonus budget predictable; the accelerator rewards over-performance.')}</p>
</div>
<style>#i_kpis input{{width:90px;font:inherit;padding:6px 8px;border:1.5px solid var(--line);border-radius:8px}}</style>'''

# ---------- 6. Performance matrix
def matrix(L):
    s = (lambda a, b: a if L == 'tr' else b)
    return f'''<div class="tool-card" data-tool="matrix" data-lang="{L}">
<h2>{s('Satışçının iki göstergesi', 'Two indicators for the rep')}</h2>
<div class="fields">
{F('m_res', s('Sonuç: hedef gerçekleşmesi %', 'Results: target achievement %'), 92, s('Ciro, kâr ve müşteri KPI’larının ağırlıklı ortalaması', 'Weighted average of sales, profit and customer KPIs'))}
{F('m_beh', s('Davranış kalitesi: koçluk puanı %', 'Behaviour quality: coaching score %'), 74, s('Koçluk gözlem formundan', 'From the coaching observation form'))}
</div>
<div class="fig"><svg id="m_chart" viewBox="0 0 520 380"></svg></div>
<div class="result" id="m_out"></div>
</div>'''

# ---------- 7. Hunter funnel
def funnel(L):
    s = (lambda a, b: a if L == 'tr' else b)
    return f'''<div class="tool-card" data-tool="funnel" data-lang="{L}">
<h2>{s('Hedeften geriye hesap', 'Work back from the target')}</h2>
<div class="fields">
{F('f_goal', s('Hedef: ay sonunda düzenli alım yapan yeni müşteri', 'Goal: new customers buying regularly at month end'), 12)}
{F('f_r1', s('Saha taraması → nitelikli aday %', 'Canvass → qualified prospect %'), 40)}
{F('f_r2', s('Nitelikli aday → ilk ziyaret %', 'Qualified → first visit %'), 60)}
{F('f_r3', s('İlk ziyaret → deneme siparişi %', 'First visit → trial order %'), 35)}
{F('f_r4', s('Deneme siparişi → ikinci sipariş %', 'Trial order → second order %'), 55)}
{F('f_r5', s('İkinci sipariş → düzenli müşteri %', 'Second order → regular customer %'), 70)}
{F('f_days', s('Ayda saha günü', 'Field days per month'), 18)}
</div>
<div class="result" id="f_out"></div>
<div class="fig"><svg id="f_chart" viewBox="0 0 640 260"></svg></div>
<p class="note">{s('Oranları kendi geçmiş verinizle güncelleyin. İlk siparişi başarı saymayın: hedefi “ikinci siparişi veren ve düzenli alan müşteri” üzerinden kurun.', 'Update the rates with your own history. Do not count the first order as success: set the goal on customers who place a second order and buy regularly.')}</p>
</div>'''

TOOLS = {}
for L in ('tr', 'en'):
    tr = L == 'tr'
    TOOLS[L] = [
        dict(key='portfolio', slug='portfoy-kapasitesi' if tr else 'portfolio-capacity', icon='calc', modules=[2, 7],
             title='Portföy kapasitesi hesaplayıcı' if tr else 'Portfolio capacity calculator',
             summary='Saha günü, ziyaret kapasitesi ve segment sıklığından bir temsilcinin yönetebileceği gerçekçi müşteri sayısını hesaplayın.' if tr else 'Calculate how many customers one rep can realistically manage from field days, visit capacity and segment frequency.',
             kind='Hesaplayıcı' if tr else 'Calculator', html=portfolio(L)),
        dict(key='smart', slug='smart-hedef' if tr else 'smart-target', icon='goal', modules=[3],
             title='SMART hedef oluşturucu' if tr else 'SMART target builder',
             summary='“Daha çok sat” yerine zamanı, kapsamı, ölçütü ve koruma kuralı olan tek cümlelik bir hedef yazın.' if tr else 'Replace “sell more” with a one-sentence target that has a time, scope, metric and guardrail.',
             kind='Şablon' if tr else 'Template', html=smart(L)),
        dict(key='checklist', slug='ziyaret-kontrol-listesi' if tr else 'visit-checklist', icon='check', modules=[6],
             title='Ziyaret kontrol listesi' if tr else 'Customer visit checklist',
             summary='Ziyaret öncesi, sırası ve sonrası için 19 maddelik kontrol listesi; hazırlık yüzdenizi anında görün.' if tr else 'A 19-point checklist for before, during and after the visit, with an instant readiness score.',
             kind='Kontrol listesi' if tr else 'Checklist', html=checklist(L)),
        dict(key='coaching', slug='kocluk-gozlem-formu' if tr else 'coaching-observation-form', icon='form', modules=[6, 10],
             title='Koçluk gözlem formu' if tr else 'Coaching observation form',
             summary='Satış görüşmesinin 8 adımında 30 kriteri puanlayın; adım bazında yüzde ve öncelikli gelişim alanları otomatik çıksın.' if tr else 'Score 30 criteria across the 8 steps of a sales call; get step percentages and priority development areas automatically.',
             kind='Form' if tr else 'Form', html=coaching(L)),
        dict(key='incentive', slug='prim-simulatoru' if tr else 'incentive-simulator', icon='money', modules=[9],
             title='Prim simülatörü' if tr else 'Incentive simulator',
             summary='Eşik, üst sınır, hızlandırıcı ve KPI ağırlıklarıyla prim kurgusunu deneyin; ödemenin nasıl değiştiğini görün.' if tr else 'Test a bonus scheme with threshold, cap, accelerator and KPI weights; see how the payout changes.',
             kind='Simülatör' if tr else 'Simulator', html=incentive(L)),
        dict(key='matrix', slug='performans-matrisi' if tr else 'performance-matrix', icon='chart', modules=[4, 10],
             title='Performans okuma matrisi' if tr else 'Performance reading matrix',
             summary='Sonuç ve davranış kalitesini birlikte okuyun; temsilcinin hangi çeyrekte olduğunu ve yöneticinin ne yapması gerektiğini görün.' if tr else 'Read results and behaviour quality together; see which quadrant the rep is in and what the manager should do.',
             kind='Teşhis' if tr else 'Diagnostic', html=matrix(L)),
        dict(key='funnel', slug='yeni-musteri-hunisi' if tr else 'new-customer-funnel', icon='hunt', modules=[5],
             title='Yeni müşteri hunisi' if tr else 'New customer funnel',
             summary='Ay sonundaki yeni düzenli müşteri hedefinden geriye giderek kaç adayı taramanız ve kaç ziyaret yapmanız gerektiğini hesaplayın.' if tr else 'Work back from your month-end goal of new regular customers to see how many prospects to canvass and visits to make.',
             kind='Hesaplayıcı' if tr else 'Calculator', html=funnel(L)),
    ]
