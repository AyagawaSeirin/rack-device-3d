from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];f=ROOT/'sources/download-index.json';rr=json.loads(f.read_text())
views={'nwr-1.jpg':'rear / top oblique, assembly','nwr-2.jpg':'front / top, three removed fans and two removed PSUs','nwr-3.jpg':'front left brand-controls, cage and ear macro','abacus-1.webp':'front low oblique','abacus-2.webp':'front/top high oblique','abacus-3.webp':'rear/top oblique','serverlama-angledside.jpg':'front/right/top stock photograph','serverlama-front.jpg':'front stock photograph','serverlama-angledtop.jpg':'front/top stock photograph','overview-501590.jpg':'official front/right oblique schematic','overview-501591.jpg':'official rear/left oblique schematic','install-501768.jpg':'traditional N3K-C3064-ACC-KIT mounting scheme','install-501933.jpg':'alternative NXK-ACC-KIT-1RU mounting scheme; NOT selected ears','psu-pe2-1.webp':'PE2 PSU top/internal end','psu-pe2-2.webp':'PE2 PSU rear/underside','psu-pe2-3.webp':'PE2 manufacturer label closeup'}
for r in rr:
 name=Path(r.get('local_path',r['requested_path'])).name
 if r['status']!='downloaded':r.update(confidence='access failure; no source content adopted',actual_model='not verified from failed response');continue
 official='/official/' in r['local_path'];psu=name.startswith('psu-')
 r.update(actual_model='NXA-PAC-1100W-PE2 module' if psu else 'multiple models; ONLY FX2 column used' if 'datasheet' in name else 'N9K-C9336C-FX2' if name in views or official or name.startswith(('nwr','abacus','serverlama')) else 'not adopted / unreviewed',view=views.get(name,'document / page'),options='blue port-side exhaust, NWR traditional three-slot ears' if name.startswith('nwr-') else 'blue exhaust; alternative five-feature ears excluded' if name.startswith('abacus-') else 'different dark-casing PE2 subrevision, local detail evidence only' if psu else 'see EVIDENCE.md',confidence='A official specification/schematic' if official else 'B original physical photo' if name in views and not name.startswith('serverlama') else 'C stock/merchant secondary',pdf_physical_page=55 if name=='hardware-guide.pdf' else 10 if name=='datasheet.pdf' else None,pdf_printed_page=49 if name=='hardware-guide.pdf' else 10 if name=='datasheet.pdf' else None)
 r['adopted_components']=views.get(name,'see EVIDENCE.md; not whole-device authority')
f.write_text(json.dumps(rr,indent=2))
# Derived content provenance, no rewriting of originals.
d=[]
for x in sorted((ROOT/'sources/derived').iterdir()):
 n=x.name
 if n.startswith('hardware-guide'):src='sources/official/hardware-guide.pdf';method='PDF text extraction' if x.suffix=='.txt' else 'PDF page rendered at 144 dpi'
 elif n.startswith('datasheet'):src='sources/official/datasheet.pdf';method='PDF page rendered at 144 dpi'
 else:src='sources/third_party/nwr-2.jpg';method='Pillow direct pixel crop, no resize/contrast/retouch'
 d.append({'local_path':str(x.relative_to(ROOT)),'parent':src,'method':method,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()})
(ROOT/'sources/derived-index.json').write_text(json.dumps(d,indent=2))
