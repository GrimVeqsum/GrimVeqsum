from pathlib import Path
import math, random, html
R=Path(__file__).resolve().parent.parent; A=R/'assets'; A.mkdir(exist_ok=True,parents=True)
random.seed(20261025)

def svgwrite(name,code):
 (A/name).write_text(code,encoding='utf-8')
def E(s):return html.escape(s,quote=True)

# Cinematic mountain banner composed from editable SVG layers.
w,h=1400,415
sky_stars=[]
for i in range(75):
 x=random.randrange(450,1380); y=random.randrange(10,190); r=random.choice([.5,.7,1,1.3]); op=random.uniform(.12,.65)
 sky_stars.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ecf7ff" opacity="{op:.2f}"/>')
# Mountain shapes are geometrically rich but subtle under the text.
mountains=[
 ('#1d2d49', '0,300 40,256 91,278 162,214 240,281 309,220 380,266 465,205 520,240 591,168 677,249 740,199 819,258 897,172 940,188 1018,138 1106,226 1175,165 1232,234 1311,179 1400,224 1400,415 0,415',.72),
 ('#14263f', '0,326 100,291 188,311 291,245 385,301 467,260 558,305 665,230 749,304 857,246 919,269 1032,193 1100,263 1157,236 1269,273 1355,240 1400,260 1400,415 0,415',.94),
 ('#0a1728', '0,351 138,321 236,347 332,308 413,354 548,315 664,358 786,300 880,334 1001,275 1070,331 1193,293 1312,333 1400,311 1400,415 0,415',1),
]
shape=''.join(f'<polygon points="{p}" fill="{c}" opacity="{o}"/>' for c,p,o in mountains)
# snow traces on very distant peaks
snow='''<path d="M971 166 L1018 138 1060 182 1035 172 1016 148 995 173 985 168Z" fill="#b3bfd8" opacity=".40"/>
<path d="M867 198 L897 172 927 200 911 190 899 180 889 198Z" fill="#c1b9d2" opacity=".35"/>
<path d="M576 186 L591 168 606 193 592 181Z" fill="#b7bdcb" opacity=".35"/>
<path d="M1151 190 L1175 165 1202 200 1179 179Z" fill="#f2c4b8" opacity=".30"/>'''
# River/lake reflections
lights=[]
for i in range(160):
 x=random.randrange(570,1400); y=random.randrange(331,414);
 ll=random.uniform(2,28)*(y-310)/105; op=random.uniform(.02,.26)
 lights.append(f'<line x1="{x}" y1="{y}" x2="{x+ll:.1f}" y2="{y}" stroke="{random.choice(["#f5a590","#67b3e5","#e6b4b4"])}" opacity="{op:.2f}" stroke-width="{random.choice([.5,1,1.2])}"/>')
# fine arcs/right telemetry
arcs='''<g fill="none" stroke="#8eabce" stroke-width="1" opacity=".18"><path d="M1110 92 H1240 L1271 61 H1354"/><path d="M1170 114 H1272 L1310 79 H1380"/><circle cx="1240" cy="92" r="3" fill="#76bfff"/></g>'''
hero=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Aidar Nazarov. Backend Software Engineer. Go, Java, Distributed Systems.">
<defs>
<linearGradient id="sky" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#090f1c"/><stop offset=".38" stop-color="#18223a"/><stop offset=".70" stop-color="#594155"/><stop offset="1" stop-color="#c46b62"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop stop-color="#07101d" stop-opacity=".98"/><stop offset=".43" stop-color="#08111e" stop-opacity=".84"/><stop offset=".69" stop-color="#08111e" stop-opacity=".1"/><stop offset="1" stop-color="#06101e" stop-opacity=".12"/></linearGradient>
<linearGradient id="lake" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#0a192b"/><stop offset="1" stop-color="#050e1b"/></linearGradient>
<radialGradient id="sunset" cx="85%" cy="49%" r="55%"><stop stop-color="#fa9589" stop-opacity=".42"/><stop offset=".5" stop-color="#ff8e7c" stop-opacity=".07"/><stop offset="1" stop-color="#ff8e7c" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{w}" height="{h}" rx="18" fill="url(#sky)"/>
<rect width="{w}" height="{h}" rx="18" fill="url(#sunset)"/>
{''.join(sky_stars)}
{shape}{snow}
<path d="M0 356 Q250 349 520 360 T1070 355 T1400 355 V415 H0Z" fill="url(#lake)"/>
{''.join(lights)}
<rect width="{w}" height="{h}" rx="18" fill="url(#fade)"/>
{arcs}
<rect x="1.2" y="1.2" width="1397.6" height="412.6" rx="17" fill="none" stroke="#324154" stroke-width="2"/>
<rect x="70" y="72" width="4" height="28" rx="2" fill="#fb7d78"/>
<text x="94" y="92" fill="#fd9c96" font-family="Arial,sans-serif" font-size="20" font-weight="700" letter-spacing="6">BACKEND ENGINEER</text>
<text x="70" y="174" fill="#ffffff" font-family="Arial,sans-serif" font-size="70" font-weight="700" letter-spacing="2">AIDAR NAZAROV</text>
<text x="73" y="218" fill="#c4d1e3" font-family="Arial,sans-serif" font-size="25">Go  ·  Java  ·  Distributed Systems</text>
<rect x="72" y="260" width="4" height="74" rx="2" fill="#5ba9fa"/>
<text x="92" y="280" fill="#d2ddeb" font-size="22" font-family="Arial,sans-serif">Building reliable APIs, scalable services</text>
<text x="92" y="312" fill="#d2ddeb" font-size="22" font-family="Arial,sans-serif">and pragmatic backend infrastructure.</text>
<text x="1360" y="376" text-anchor="end" fill="#e0ebfa" opacity=".74" font-size="14" letter-spacing="3" font-family="Arial,sans-serif">GRIMVEQSUM / ENGINEERING</text>
</svg>'''
svgwrite('hero.svg',hero)

# Technology matrix - all text is SVG-native and can be edited.
categories=[
 ('LANGUAGES',[('Go','#35c5dc'),('Java','#ef8a55'),('Python','#5e9bdd'),('C#','#c38dee')]),
 ('BACKEND & API',[('REST API','#54bafe'),('gRPC','#45cecf'),('Kafka','#e2e6ef'),('RabbitMQ','#f39a57')]),
 ('DATA & STORAGE',[('PostgreSQL','#6ba8ea'),('ClickHouse','#e6cd5f'),('Redis','#f06c6c'),('MinIO','#df657c')]),
 ('INFRASTRUCTURE',[('Docker','#45aaff'),('Kubernetes','#649bfa'),('Linux','#e6c55e'),('Terraform','#a895e3')]),
 ('TOOLS',[('Git','#fb8565'),('GitHub Actions','#91aaf3'),('Grafana','#fa9363'),('Prometheus','#e77752')]),
]
body=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="276" viewBox="0 0 1400 276">
<rect x="1" y="1" width="1398" height="274" rx="18" fill="#0c1524" stroke="#293849" stroke-width="2"/>''']
for col,(heading,items) in enumerate(categories):
 x=15+col*277
 body.append(f'<rect x="{x}" y="16" width="263" height="243" rx="13" fill="#101d30" stroke="#2d4056"/>')
 body.append(f'<text x="{x+20}" y="53" fill="#8fa6c4" font-family="Arial,sans-serif" font-size="17" letter-spacing="1.2" font-weight="700">{E(heading)}</text>')
 body.append(f'<line x1="{x+20}" y1="67" x2="{x+242}" y2="67" stroke="#28384d"/>')
 for j,(label,colr) in enumerate(items):
  xx=x+21+(j%2)*126; yy=97+(j//2)*91
  body.append(f'<rect x="{xx}" y="{yy}" width="104" height="70" rx="8" fill="#0b1626"/>')
  body.append(f'<rect x="{xx+12}" y="{yy+12}" width="26" height="26" rx="7" fill="{colr}" opacity=".18"/>')
  body.append(f'<circle cx="{xx+25}" cy="{yy+25}" r="7" fill="none" stroke="{colr}" stroke-width="2.8"/>')
  body.append(f'<path d="M{xx+20} {yy+25}h10 M{xx+25} {yy+20}v10" stroke="{colr}" stroke-width="1.5"/>')
  # compact text for long labels
  size=11.5 if len(label)>12 else 14
  body.append(f'<text x="{xx+12}" y="{yy+58}" fill="#deebfa" font-family="Arial,sans-serif" font-size="{size}" font-weight="600">{E(label)}</text>')
body.append('</svg>');svgwrite('tech-stack.svg',''.join(body))

projects=[
 dict(name='MovieTracker',kind='movie',desc1='Personal movie library with',desc2='event-driven metadata enrichment.',tags=['Go','Kafka','PostgreSQL']),
 dict(name='LinkPulse',kind='links',desc1='URL service with gRPC analytics',desc2='and ClickHouse event storage.',tags=['Go','gRPC','ClickHouse']),
 dict(name='FileStorage',kind='storage',desc1='File upload API backed by MinIO',desc2='object storage and PostgreSQL.',tags=['Go','MinIO','PostgreSQL']),
 dict(name='OrderReservationService',kind='orders',desc1='Inventory-aware reservations',desc2='with transactional stock control.',tags=['Java','Spring Boot','PostgreSQL'])
]
art={
'movie':'''<g transform="translate(27,39)"><rect x="18" y="25" width="190" height="118" rx="9" stroke="#83b7f7" fill="#0c2541" stroke-width="3"/><rect x="33" y="40" width="160" height="87" rx="5" fill="#112f4f" stroke="#5082b7"/><circle cx="111" cy="83" r="29" fill="#284f7c" stroke="#7cb1e8" stroke-width="2"/><path d="M104 68 L134 83 104 99Z" fill="#b6ddff"/><path d="M18 15v12m28-12v12m29-12v12m29-12v12m29-12v12m29-12v12m28-12v12M18 141v13m28-13v13m29-13v13m29-13v13m29-13v13m29-13v13m28-13v13" stroke="#79acd8" stroke-width="7"/></g>''',
'links':'''<g transform="translate(36,25)" fill="none" stroke-linecap="round"><path d="M10 167H224M21 20V166" stroke="#324b69" stroke-width="2"/><g stroke="#203852"><path d="M50 18V170 M85 18V170 M120 18V170 M155 18V170 M190 18V170 M20 48H220 M20 86H220 M20 124H220"/></g><path d="M26 134 L58 116 87 128 115 67 149 83 179 42 215 17" stroke="#68b8ff" stroke-width="5"/><path d="M26 152 L60 139 86 145 114 122 150 130 183 89 215 81" stroke="#fa9a82" stroke-width="3" opacity=".7"/>{dots}</g>'''.replace('{dots}', ''.join(f'<circle cx="{x}" cy="{y}" r="5" fill="#72befe" stroke="#152a44" stroke-width="2"/>' for x,y in [(26,134),(58,116),(87,128),(115,67),(149,83),(179,42),(215,17)])),
'storage':'''<g transform="translate(40,38)" stroke-linejoin="round"><path d="M23 64h75l18 24h99v93H23Z" fill="#143755" stroke="#7dbaf2" stroke-width="3"/><path d="M23 87h192l-20 74H7Z" fill="#285b82" stroke="#79b7f0" stroke-width="3"/><path d="M65 24c4-23 44-28 56-7 20-10 40 0 43 18 32-3 45 37 25 53H56C16 74 27 32 65 24Z" fill="#295474" stroke="#7ec8ff" stroke-width="3"/><path d="M109 83V44M92 60L109 42l17 18" stroke="#c9e8ff" stroke-width="5" fill="none" stroke-linecap="round"/></g>''',
'orders':'''<g transform="translate(37,33)" stroke="#84b9ee" stroke-width="2"><path d="M5 33L69 8l65 25-65 27Z" fill="#1a4267"/><path d="M5 33v74l64 33V60Z" fill="#103352"/><path d="M134 33v74l-65 33V60Z" fill="#245980"/><path d="M69 60V140M33 21l69 26" stroke="#5280a5"/><path d="M123 92L185 68l57 25-62 25Z" fill="#235879"/><path d="M123 92v56l57 31v-61Z" fill="#173d5d"/><path d="M242 93v55l-62 31v-61Z" fill="#2a6285"/><path d="M153 81l60 25" stroke="#5c87ac"/></g>''',
}
for p in projects:
 name=p['name'];desc1=p['desc1'];desc2=p['desc2'];tags=p['tags'];kind=p['kind'];tagx=292
 rect=[]
 for tag in tags:
  width=26+len(tag)*8.5
  rect.append(f'<rect x="{tagx}" y="156" width="{width}" height="30" rx="9" fill="#1c3550" stroke="#335475"/><text x="{tagx+13}" y="176" font-size="14" fill="#a6d4ff" font-family="Arial,sans-serif">{E(tag)}</text>')
  tagx+=width+8
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="690" height="226" viewBox="0 0 690 226" role="img" aria-label="{E(name)} project">
 <defs><linearGradient id="shade" x1="0" x2="1" y1="0" y2="1"><stop stop-color="#122941"/><stop offset="1" stop-color="#081625"/></linearGradient></defs>
 <rect x="1" y="1" width="688" height="224" rx="16" fill="#0d1828" stroke="#32455b" stroke-width="2"/>
 <rect x="12" y="12" width="262" height="200" rx="11" fill="url(#shade)"/>
 <path d="M12 160 Q140 98 274 172V211H12Z" fill="#081524" opacity=".5"/>
 {art[kind]}
 <text x="292" y="68" font-size="27" font-weight="700" font-family="Arial,sans-serif" fill="#67b9ff">{E(name)}</text>
 <text x="292" y="103" font-size="17" fill="#d6e1ef" font-family="Arial,sans-serif">{E(desc1)}</text>
 <text x="292" y="131" font-size="17" fill="#d6e1ef" font-family="Arial,sans-serif">{E(desc2)}</text>
 {''.join(rect)}
 <path d="M648 196h18 m-7-7 7 7-7 7" stroke="#69b8ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
 </svg>'''
 svgwrite('project-'+kind+'.svg',s)

# Intro snake illustration. Workflow will replace it with real contribution data.
# Initial visualization is explicitly marked as preview (no fake contribution counts).
snake=[]
for r in range(7):
 for c in range(74):
  x=22+c*18; y=46+r*18
  snake.append(f'<rect x="{x}" y="{y}" width="13" height="13" rx="3" fill="#21334b" opacity=".58"/>')
points=[]
for c in range(4,69):
 y=107+46*math.sin((c-4)/8)
 points.append(f'{22+c*18},{y:.1f}')
snake_svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="220" viewBox="0 0 1400 220">
<rect x="1" y="1" width="1398" height="218" rx="15" fill="#0a1523" stroke="#293b50" stroke-width="2"/>
{''.join(snake)}
<polyline points="{' '.join(points)}" fill="none" stroke="#57b3f6" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" opacity=".88" stroke-dasharray="25 7"><animate attributeName="stroke-dashoffset" values="0;-128" dur="5s" repeatCount="indefinite"/></polyline>
<rect x="20" y="189" width="1360" height="22" fill="#0a1523" opacity=".8"/>
<text x="30" y="205" font-size="14" fill="#8ea3bd" font-family="Arial,sans-serif">PREVIEW · Run the GitHub Action to render your real contribution history</text>
</svg>'''
if not (A/'snake.svg').exists():
    svgwrite('snake.svg',snake_svg)
print('Generated:',*[p.name for p in A.iterdir()])
