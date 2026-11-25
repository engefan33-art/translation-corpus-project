"""Python standard library only. Run from this directory. No invented bilingual names."""
import csv, json, re, random, hashlib, urllib.request, pathlib, collections
P=pathlib.Path(__file__).resolve().parent
COMMIT='9d009101be468758a8f73a2b425a85dea119731f'
URL=f'https://raw.githubusercontent.com/Hong-Kong-Districts-Info/hkdatasets/{COMMIT}/data-raw/hkstreetnames20.csv'
DATE='2026-11-14'
raw=P/'source.csv'
if not raw.exists(): raw.write_bytes(urllib.request.urlopen(URL).read())
rules=json.loads((P/'codebook-rules.json').read_text(encoding='utf-8'))
mapping=rules['canonical']
zhterms=sorted(set(sum(mapping.values(),[])+['坊','堤','海旁','走廊','徑','街','路','道','里','巷','圍']),key=len,reverse=True)
def classify(en,zh,version=2):
    # Last standalone generic token allows ROAD EAST and LANE KEI LUN WAI.
    ens=re.findall(r'\b('+'|'.join(mapping)+r')\b',en)
    eg=ens[-1] if ens else ''
    z=zh
    if version==2: z=re.sub(r'(?:[東西南北中]|[一二三四五六七八九十0-9]+段|[（(][^）)]*[）)])+$','',z)
    zg=next((s for s in zhterms if z.endswith(s)),'')
    cat='unresolved' if not eg and not zg else 'one_sided' if not eg or not zg else 'conventional' if zg in mapping[eg] else 'alternative'
    return eg or '∅',zg or '∅',cat
rows=list(csv.DictReader(raw.open(encoding='utf-8-sig',newline='')))
eligible=[]; seen=set(); reject=collections.Counter()
for line,r in enumerate(rows,2):
    en=' '.join(r['StreetNames_EN'].split()); zh=' '.join(r['StreetNames_ZH'].split())
    if not en or not zh or not re.search('[A-Za-z]',en) or not re.search('[\u3400-\u9fff]',zh): reject['empty_or_missing_script']+=1; continue
    if len(en)>150 or len(zh)>80: reject['length']+=1; continue
    if (en,zh) in seen: reject['duplicate_pair']+=1; continue
    seen.add((en,zh)); eligible.append(dict(id=f'HK{line:05}',source_row=line,source_text=en,target_text=zh,district=r['DC'],source=f'hkstreetnames20 / 2020-06-30 snapshot; commit {COMMIT}; CSV line {line}; retrieved {DATE}; seed 2026; {URL}',source_url=f'https://github.com/Hong-Kong-Districts-Info/hkdatasets/blob/{COMMIT}/data-raw/hkstreetnames20.csv#L{line}',human_checked='no',unit='street-name pair',year=2020))
pilot=random.Random(2025).sample(eligible,25)
plog=[]
for r in pilot:
    a=classify(r['source_text'],r['target_text'],1); b=classify(r['source_text'],r['target_text'],2)
    plog.append(dict(id=r['id'],source_text=r['source_text'],target_text=r['target_text'],v1=a,v2=b,changed=a!=b))
(P/'pilot.json').write_text(json.dumps(plog,ensure_ascii=False,indent=2),encoding='utf-8')
sample=random.Random(2026).sample(eligible,500)
for r in sample:
    r['en_generic'],r['zh_generic'],r['category']=classify(r['source_text'],r['target_text'])
    r['key_term']=r['en_generic']; r['notes']='Automatic v2 lexical annotation; human verification pending. Source/target are display labels, not a historical direction claim.'
sample.sort(key=lambda r:r['id'])
audit=random.Random(2050).sample(sample,50)
review_path=P/'human-review-50.csv'
fields=['id','source_text','target_text','category','source_url','verified_by_student','error_found','corrected_source_text','corrected_target_text','corrected_category','review_notes']
if review_path.exists():
    with review_path.open(encoding='utf-8-sig',newline='') as f:
        reviews=list(csv.DictReader(f))
    assert {r['id'] for r in reviews}=={r['id'] for r in audit}, 'Review sample changed; existing review retained.'
    by_id={r['id']:r for r in sample}
    for review in reviews:
        row=by_id[review['id']]
        assert all(review[k]==row[k] for k in ('source_text','target_text','category','source_url')), 'Reviewed source changed.'
        if review['verified_by_student'].strip().lower()=='yes':
            assert review['error_found'].strip().lower() in ('yes','no'), 'Missing review outcome.'
            for field in ('source_text','target_text','category'):
                correction=review.get('corrected_'+field,'').strip()
                if correction:
                    row[field]=correction
            row['en_generic'],row['zh_generic'],_=classify(row['source_text'],row['target_text'])
            row['key_term']=row['en_generic']
            row['human_checked']='yes'
        row['notes']='Student review recorded.' if row['human_checked']=='yes' else 'Automatic v2 annotation; not manually checked.'
else:
    with review_path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(audit)
    reviews=[]
meta=dict(source_url=URL,commit=COMMIT,retrieved=DATE,raw_rows=len(rows),eligible=len(eligible),rejected=dict(reject),sample_seed=2026,pilot_seed=2025,review_seed=2050,pilot_changes=sum(x['changed'] for x in plog),sample_size=500,human_checked=0,sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),counts=dict(collections.Counter(r['category'] for r in sample)))
meta.update(human_checked=sum(r['human_checked']=='yes' for r in sample),human_review_errors=sum(r.get('error_found','').lower()=='yes' for r in reviews),human_review_corrections=sum(any(r.get('corrected_'+f,'').strip() for f in ('source_text','target_text','category')) for r in reviews))
for name,obj in [('data.json',sample),('metadata.json',meta)]: (P/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
(P/'data.js').write_text('window.CORPUS='+json.dumps(sample,ensure_ascii=False)+';\nwindow.META='+json.dumps(meta,ensure_ascii=False)+';',encoding='utf-8')
with (P/'corpus.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(sample[0]));w.writeheader();w.writerows(sample)
assert len(sample)==500 and len({r['id'] for r in sample})==500 and len(audit)==50
assert sum(meta['counts'].values())==500
print(json.dumps(meta,ensure_ascii=True,indent=2))
