#!/usr/bin/env python3
"""Independent source/native/frozen/ERC/BOM/privacy gates for the isolated draft.

This never accepts integrated audio, publishes, changes source contracts, or
suppresses ERC. --freeze-plan must run BEFORE attaching the draft to the root.
--native regenerates XML/ERC/BOM/PDF, preserving ERC's failing release exit code.
"""
import argparse, ast, collections, copy, csv, gzip, hashlib, html, io, itertools, json, math, os, re
import subprocess, sys, tarfile, urllib.parse, xml.etree.ElementTree as ET, zipfile
from pathlib import Path
import fitz

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'sim/kicad'))
from sexp import parse,find
sys.path.insert(0,str(ROOT/'scripts'))
from build_audio_aux_draft import PIN_HASH,PASSIVE_HASH,CONTRACT_HASH,CALC_HASH,STATE_HASH,PARENT_ID,ROOT_ID,PARENT_UUID,bom_command

INPUT=ROOT/'design/audio_aux_draft_inputs.json'
EXPECT=ROOT/'design/audio_aux_draft_expected_erc.json'
PARENT_NAME='AUX DRAFT / DO NOT ENABLE'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
hashdata=lambda b:hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
def git(*argv):
    r=subprocess.run(['git',*argv],cwd=ROOT,capture_output=True)
    if r.returncode:raise ValueError('Git read/check failed; command='+argv[0])
    return r.stdout
def run(argv,expected=0):
    r=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True)
    if r.returncode!=expected:raise ValueError('Command exit differs: '+str(r.returncode))
    return r.returncode
def xml(p):
    r=ET.parse(p).getroot();comps={}
    for c in r.findall('./components/comp'):
        d={x.attrib['name']:x.text or '' for x in c.findall('./fields/field')}
        d.update(Value=c.findtext('value',''),Footprint=c.findtext('footprint',''),Datasheet=c.findtext('datasheet',''))
        d['properties']={p.attrib['name']:p.attrib.get('value','') for p in c.findall('property')}
        d['sheet']=c.find('sheetpath').attrib['names'];comps[c.attrib['ref']]=d
    nets={n.attrib['name']:{(p.attrib['ref'],p.attrib['pin']) for p in n.findall('node')} for n in r.findall('./nets/net')}
    return {'components':comps,'nets':nets,'sheets':len(r.findall('./design/sheet'))}
def tuples(r):
    return sorted((s['path'],v['type'],v['severity'],tuple((i['uuid'],i['description']) for i in v['items']))
                  for s in r['sheets'] for v in s['violations'])
def source_expected(i):
    """Derive every endpoint independently from source ledgers, including overlap."""
    pinrows=i['pins'];passives=i['passives'];m=i['ref_map'];points={};parts={}
    for p in pinrows:
        key=(m[p['ref']],p['pin']);assert key not in points
        points[key]=p['net'];parts[p['ref']]=p['mpn']
    for p in passives:
        parts[p['ref']]=p['mpn'];e=p['endpoints'];kind=p['kind']
        if kind=='rectifier':e={'1':e['cathode'],'2':e['anode']}
        elif kind=='normally_closed_photomos':e={'1':e['LED_A'],'2':e['LED_K'],'3':e['contact3'],'4':e['contact4']}
        else:e={str(n+1):v for n,v in enumerate(e)}
        for no,n in e.items():
            key=(m[p['ref']],no);assert key not in points or points[key]==n,'Source overlap disagrees'
            points[key]=n
    groups=collections.defaultdict(set)
    for key,n in points.items():groups[('OPEN',key) if n=='OPEN' else n].add(key)
    return parts,points,dict(groups)
def number(v):
    m=re.fullmatch(r'([0-9.eE+\-]+)(M|k|R|uF|nF|pF|uH)',v)
    if not m:return None
    return float(m[1])*{'M':1e6,'k':1e3,'R':1,'uF':1e-6,'nF':1e-9,'pF':1e-12,'uH':1e-6}[m[2]]
def evaluate(i,a,base):
    errors=[]
    def req(name,ok):
        if not ok:errors.append(name)
    parts,points,groups=source_expected(i);new=set(i['ref_map'].values());old=set(base['components'])
    req('259_unique_source_union',len(parts)==259 and len(new)==259 and set(parts)==set(i['ref_map']))
    req('289_pin_rows',len(i['pins'])==289)
    req('exact_native_component_union',set(a['components'])==old|new and not old&new)
    req('17_structural_unfulfilled_providers',len(i['provider_obligations'])==17 and len(i['provider_states'])==17 and
        {p['id'] for p in i['provider_obligations']}=={p['id'] for p in i['provider_states']} and
        all(p['status']=='UNFULFILLED' and p['fulfilled'] is False and p['READY_prerequisite'] is False for p in i['provider_states']))
    req('truthful_status_scope',i['status']=='NATIVE_DRAFT_PROGRESS' and i['scope']=='native_draft_progress' and all(v is False for v in i['flags'].values()))
    req('original_targets_retained',len(i['original_A_records'])==20 and i['targets']['PCM_Hz']==768000 and i['targets']['native_DSD_ratio']==512 and i['targets']['DoP_ratio']==256 and i['targets']['desktop_stereo_W_per_ch']=={'16':7.6,'32':6.4,'64':4.3,'300':1,'600':.5})
    req('every_old_component_field_unchanged',all(a['components'].get(r)==d for r,d in base['components'].items()))
    req('every_old_pin_partition_unchanged',{frozenset(ep) for ep in a['nets'].values() if ep and any(r in old for r,n in ep)}=={frozenset(ep) for ep in base['nets'].values()})
    req('zero_conductive_old_new_connections',all(not(any(r in new for r,n in ep) and any(r in old for r,n in ep)) for ep in a['nets'].values()))
    req('exact_all_source_pin_and_passive_partitions',{frozenset(ep) for ep in a['nets'].values() if ep and all(r in new for r,n in ep)}=={frozenset(ep) for ep in groups.values()})
    for ref,mpn in parts.items():
        r=i['ref_map'][ref];d=a['components'].get(r,{});pr=next((p for p in i['passives'] if p['ref']==ref),None)
        req('MPN_'+r,d.get('Manufacturer_Part_Number')==mpn)
        req('source_identity_'+r,d.get('Source_Reference')==ref and d.get('Source_ID')==(pr['source'] if pr else next(p['source'] for p in i['pins'] if p['ref']==ref)))
        req('blank_new_Footprint_'+r,d.get('Footprint')=='')
        req('not_excluded_dnp_'+r,not any(k in d.get('properties',{}) for k in ['exclude_from_bom','exclude_from_board','dnp']))
        pages={p['pin']:{'source':p['source'],'page':p['page'],'function':p['function']} for p in i['pins'] if p['ref']==ref}
        try:pageprop=json.loads(d.get('Source_Pin_Pages','{}'))
        except Exception:pageprop=None
        req('source_pin_pages_'+r,pageprop==pages)
        if pr:
            v=pr['value'];key={'resistor':'ohm','capacitor':'F_nom','inductor':'H_nom'}.get(pr['kind'])
            if key:req('exact_passive_value_'+r,number(d.get('Value','')) is not None and math.isclose(number(d['Value']),v[key],rel_tol=1e-12))
            else:req('exact_device_value_'+r,d.get('Value')==mpn)
            req('source_condition_'+r,d.get('Source_Condition')==pr['condition'])
        else:req('exact_active_value_'+r,d.get('Value')==mpn)
    return errors

def plan_check(i,r):
    """Only anticipated physical provider boundaries and legitimate OPEN pins.

    Missing LED drivers cause 3 single-pin labels per each of 54 LED nets.
    No new library/grid/type-conflict/dangling-wire report is admissible.
    KiCad reports one representative per undriven power partition and emits open
    parent pins for the first branch in its native report; all 72 boundary ports
    are independently counted and checked in the actual native source.
    """
    counts=collections.Counter();allowedports={'AD_RETURN' if n=='GND' else 'AD_'+n for v in i['ports'].values() for n in v if n!='GND'}
    parts,points,groups=source_expected(i)
    for s in r['sheets']:
        for v in s['violations']:
            typ=v['type'];counts[(typ,v['severity'])]+=1
            if typ=='isolated_pin_label':
                for item in v['items']:
                    m=re.search(r"(?:Hierarchical )?Label '(AD_K_[^']+_LED_[AK])'",item['description'])
                    assert m and m[1] in allowedports,'Non-provider isolated label'
            elif typ=='pin_not_connected':
                for item in v['items']:
                    d=item['description'];m=re.fullmatch(r"Hierarchical Sheet Pin '([^']+)'",d)
                    if m:assert m[1] in allowedports,'Unexpected open hierarchy pin'
                    else:assert re.match(r'Symbol '+re.escape(i['ref_map']['U_AUX5'])+r' Pin (10|11) \[',d),'Unexpected open component pin'
            elif typ=='power_pin_not_driven':
                d=v['items'][0]['description'];m=re.match(r'Symbol (\S+) Pin (\S+) \[',d)
                assert m and (m[1],m[2]) in points,'Missing-power pin outside selected source'
                n=points[m[1],m[2]]
                permitted={'GND','AUX_SOURCE','AUX5V'}|{b+s for b in ['IV','QUIET','LINE'] for s in ['_5V_INPUT','_VIN_FILTER','_P_PRE','_N_PRE']}
                assert n in permitted,'Undriven power outside admitted converter/return boundaries'
            else:raise AssertionError('Unexpected draft ERC category: '+typ)
    assert counts=={('isolated_pin_label','warning'):162,('pin_not_connected','error'):28,('power_pin_not_driven','error'):15},'Native expected ERC count changed'
    return {f'{k[0]}:{k[1]}':v for k,v in counts.items()}

def privacy(e):
    host=urllib.parse.urlparse(os.environ.get('YOUTRACK_BASE_URL','')).hostname;token=os.environ.get('YOUTRACK_TOKEN','')
    assert host and token,'Configured private scan needles unavailable'
    tally=collections.Counter();fail=[]
    def match(data):
        for enc in ['utf-8','utf-16-le','utf-16-be']:
            if host.encode(enc).lower() in data.lower():return True
            try:s=data.decode(enc)
            except UnicodeError:continue
            s=html.unescape(urllib.parse.unquote(s));s=re.sub(r'\\u([0-9a-fA-F]{4})',lambda m:chr(int(m[1],16)),s).replace('\\/','/')
            if host.lower() in s.lower():return True
        return token.encode() in data or bool(re.search(rb'(?i)\bBearer\s+(?:perm:|eyJ)[A-Za-z0-9_:.\-]{12,}|\bperm:[A-Za-z0-9_.\-]{20,}',data))
    def inspect(data,depth=0):
        assert depth<20
        if match(data):raise ValueError('Privacy match')
        if data.startswith(b'%PDF-'):
            tally['pdfs']+=1
            with fitz.open(stream=data,filetype='pdf') as d:
                inspect(json.dumps(d.metadata).encode(),depth+1)
                for p in d:inspect((p.get_text()+json.dumps(p.get_links(),default=str)).encode(),depth+1)
                for n in range(1,d.xref_length()):
                    inspect(d.xref_object(n).encode(),depth+1);inspect(d.xref_stream(n) or b'',depth+1)
                for name in d.embfile_names():inspect(d.embfile_get(name),depth+1)
        if zipfile.is_zipfile(io.BytesIO(data)):
            tally['archives']+=1
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                inspect(z.comment,depth+1)
                for p in z.infolist():
                    inspect((p.filename.encode()+p.comment),depth+1)
                    if not p.is_dir():tally['archive_entries']+=1;inspect(z.read(p),depth+1)
        elif data.startswith(b'\x1f\x8b'):tally['archives']+=1;inspect(gzip.decompress(data),depth+1)
        elif len(data)>262 and data[257:262]==b'ustar':
            tally['archives']+=1
            with tarfile.open(fileobj=io.BytesIO(data),mode='r:') as t:
                for p in t:
                    inspect(p.name.encode(),depth+1)
                    if p.isfile():tally['archive_entries']+=1;inspect(t.extractfile(p).read(),depth+1)
    def safe(data,label):
        try:inspect(data)
        except Exception as ex:fail.append({'surface_sha256':hashdata(label.encode()),'error_type':type(ex).__name__})
    # Local all-ref history, current working tree, staged contents and all ref/tag names/messages.
    lines=git('rev-list','--objects','--all').decode().splitlines();tally['reachable_objects']=len(lines)
    for line in lines:
        oid,_,name=line.partition(' ');kind=git('cat-file','-t',oid).decode().strip();tally[kind+'s']+=1
        safe(git('cat-file',kind,oid),oid)
    paths=set(git('ls-files').decode().splitlines())|set(git('ls-files','--others','--exclude-standard').decode().splitlines())
    for p in sorted(paths):
        if (ROOT/p).is_file():tally['working_files']+=1;safe((ROOT/p).read_bytes(),p)
    for line in git('ls-files','--stage').decode().splitlines():
        meta,_,p=line.partition('\t');mode,oid,stage=meta.split()
        if mode!='160000':tally['staged_blobs']+=1;safe(git('cat-file','blob',oid),oid)
    safe(git('for-each-ref','--format=%(refname) %(contents)'), 'ref-tag-names-messages')
    report={'counts':dict(tally),'hits_or_extraction_errors':fail,'coverage_complete':not fail,'private_needles_configured':True}
    save(e/'privacy.json',report);assert not fail,'Privacy extraction/match gate failed; opaque report only'
    return report

def visual(e):
    from PIL import Image,ImageDraw
    before=fitz.open(e/'baseline.pdf');after=fitz.open(ROOT/'exports/ereader_rev1.pdf')
    assert len(before)==16 and len(after)==21
    parity=[]
    for n in range(21):
        pix=after[n].get_pixmap(matrix=fitz.Matrix(1,1));img=Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
        img.save(e/('final-page-%02d.png'%(n+1)))
        if n<16:
            old=before[n].get_pixmap(matrix=fitz.Matrix(1,1));a=Image.frombytes('RGB',[old.width,old.height],old.samples);b=img.copy();assert a.size==b.size
            # Generated titleblock dates/page counts only; the pinless root review island has an explicit own mask.
            w,h=a.size;mm=72/25.4
            boxes=[(w-120*mm,h-55*mm,w,h)]
            if n==0:boxes.append(tuple(x*mm for x in [428,27,575,69]))
            for im in [a,b]:
                draw=ImageDraw.Draw(im)
                for box in boxes:draw.rectangle(box,fill='white')
            assert a.tobytes()==b.tobytes(),'Old schematic raster changed: '+str(n+1)
            parity.append({'page':n+1,'body_pixels_identical':True,'mask_boxes_pixels':boxes})
    save(e/'visual-parity.json',{'pages':21,'old_pages':parity,'new_pages':[17,18,19,20,21],'final_pdf_sha256':sha(ROOT/'exports/ereader_rev1.pdf'),'new_page_review':'Requires human/agent visual inspection of all five rendered pages; raster parity alone is not new-layout approval'})

def main(args):
    i=load(INPUT);e=args.evidence_dir;e.mkdir(parents=True,exist_ok=True)
    if args.freeze_plan:
        # Must be frozen while root has no draft child: an already-attached root is rejected.
        assert PARENT_ID not in (ROOT/'ereader/ereader_rev1.kicad_sch').read_text()
        r=load(e/'draft-plan-erc.json');counts=plan_check(i,r)
        expected={'prepared_before_root_attachment':True,'input_sha256':sha(INPUT),'standalone_report_sha256':sha(e/'draft-plan-erc.json'),
                  'standalone_xml_sha256':sha(e/'draft-plan.xml'),'counts':counts,'tuples':tuples(r),
                  'reason':'54 externally undriven LED nets x3 labels;26 native representative open parent ports;RT10/SS11 source OPEN;15 representative undriven supply/return partitions',
                  'native_files_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in (ROOT/'ereader').glob('audio_aux_draft*.kicad_sch')}}
        save(EXPECT,expected);print('Expected source-role-qualified native ERC frozen before root attachment');return
    expect=load(EXPECT);assert sha(INPUT)==expect['input_sha256'],'Input seal changed'
    checks=[]
    def check(name,expected,actual,ok):
        checks.append({'CHECK':name,'COMMAND':'check_audio_aux_draft.py '+args.mode,'EXPECTED':expected,'ACTUAL':actual,'RESULT':'PASS' if ok else 'FAIL'})
        assert ok,'Gate failed: '+name
    if args.mode=='--privacy':privacy(e);print('Privacy gate PASS; no private values printed');return
    if args.mode=='--visual':visual(e);print('Every PDF page rendered; all16 old circuit bodies pixel-identical');return
    if args.source_dir:
        b=args.source_dir
        for name,h in [('all-pin-ledger.json',PIN_HASH),('passive-ledger.json',PASSIVE_HASH),('contract.json',CONTRACT_HASH),('calculations.json',CALC_HASH),('state-matrix.json',STATE_HASH)]:
            check('source_hash_'+name,h,sha(b/name),sha(b/name)==h)
        c=load(b/'contract.json');check('source_pins_exact','sealed source',i['pins']==load(b/'all-pin-ledger.json'),i['pins']==load(b/'all-pin-ledger.json'))
        check('source_passives_exact','sealed source',i['passives']==load(b/'passive-ledger.json'),i['passives']==load(b/'passive-ledger.json'))
        check('full_source_predicates_states_targets','unchanged',True,all(i[k]==c[k] for k in ['provider_obligations','intrinsic_unknowns','targets','original_A_records','interfaces']) and i['state_matrix']==load(b/'state-matrix.json') and i['calculations']==load(b/'calculations.json'))
        gate=load(b.parent/'audio_aux_converter_cell-latest-gate.json')
        check('current_root_local_source_gate','PASS-local-only',gate.get('verdict'),gate['verdict']=='PASS' and gate['contract_sha256']==CONTRACT_HASH and gate['provider_obligations_unfulfilled']==17 and gate['joint_accepted'] is False)
        for s in load(b/'sources.json'):check('manufacturer_source_hash_'+s['id'],s['sha256'],sha(Path(s['file'])),sha(Path(s['file']))==s['sha256'])
        review=b.parent/'schematic_scope_application_review-v2';st=load(review/'exact-staging-inputs.json')
        check('review2_exact_staging','same exact pins/passives/providers',True,all(i[k]==st[k] for k in ['pins','passives','provider_obligations','state_matrix','intrinsic_unknowns','targets','original_A_records']))
        # Replay only the sealed source's pure arithmetic predicates. Do not import
        # its CLI module: that would overwrite a source owner's result artifacts.
        verifier=b/'verify.py';tree=ast.parse(verifier.read_text())
        functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['evaluate','full_evaluate']]
        assert len(functions)==2
        scope={'math':math,'itertools':itertools}
        exec(compile(ast.Module(body=functions,type_ignores=[]),str(verifier),'exec'),scope)
        replay=scope['full_evaluate'](c,i['passives'],i['pins'],i['calculations'])
        check('read_only_source_full_arithmetic_replay','zero failed conditional predicates',replay,not replay)
        check('conditional_power_actor_budget','desktop<=11W / quiet<=8.2W',i['calculations']['power']['desktop_W'],
            i['calculations']['power']['desktop_W']<=11 and i['calculations']['power']['portable_W']<=8.2)
    if args.mode=='--native':
        assert args.kicad
        for cmd in [['sch','export','netlist','--format','kicadxml','--output',str(e/'post.xml'),'ereader/ereader_rev1.kicad_sch'],
                    ['sch','erc','--format','json','--output',str(e/'post-erc.json'),'ereader/ereader_rev1.kicad_sch'],
                    ['sch','export','pdf','--output',str(e/'post.pdf'),'ereader/ereader_rev1.kicad_sch'],bom_command(e/'post-bom.csv','ereader/ereader_rev1.kicad_sch')]:
            run([args.kicad]+cmd)
        exitcode=run([args.kicad,'sch','erc','--format','json','--exit-code-violations','--output',str(e/'release-erc.json'),'ereader/ereader_rev1.kicad_sch'],5)
        check('release_ERC_honestly_fails',5,exitcode,exitcode==5)
    base=xml(e/'baseline.xml');a=xml(e/'post.xml');errors=evaluate(i,a,base)
    check('complete_native_semantic_gate','zero mismatches',errors,not errors)
    check('native_counts','615components/577nets/21sheets',[len(a['components']),len(a['nets']),a['sheets']],len(a['components'])==615 and len(a['nets'])==577 and a['sheets']==21)
    # Exact unchanged existing ASTs and raw hashes. Root adds only the isolated sheet.
    baseline='588fc58'
    frozen=load(e/'baseline-file-hashes.json');changed=[]
    allowed={'ereader/ereader_rev1.kicad_sch','ereader/sym-lib-table','exports/ereader_rev1.pdf','exports/ereader_rev1_bom.csv'}
    for p,h in frozen.items():
        if p not in allowed and (not (ROOT/p).is_file() or h!=sha(ROOT/p)):changed.append(p)
    check('frozen_existing_file_bytes','empty delta',changed,not changed)
    oldroot=parse(git('show',baseline+':ereader/ereader_rev1.kicad_sch').decode());newroot=parse((ROOT/'ereader/ereader_rev1.kicad_sch').read_text())
    added=[s for s in find(newroot,'sheet') if str(find(s,'uuid')[0][1])==PARENT_ID]
    check('root_review_only_addition','1 pinless sheet; all original AST unchanged',len(added),len(added)==1 and not find(added[0],'pin') and [n for n in newroot if n not in added]==oldroot)
    ot=parse(git('show',baseline+':ereader/sym-lib-table').decode());nt=parse((ROOT/'ereader/sym-lib-table').read_text())
    nl=[s for s in find(nt,'lib') if find(s,'name')[0][1]=='Aux_Draft']
    check('symbol_registry_append_only','1 new entry; all old entries unchanged',len(nl),len(nl)==1 and [n for n in nt if n not in nl]==ot)
    for p,h in expect['native_files_sha256'].items():check('frozen_native_plan_'+p,h,sha(ROOT/p),sha(ROOT/p)==h)
    # All source roles and symbol pin number/name/type are verified independently.
    library=parse((ROOT/'libs/symbols/Aux_Draft.kicad_sym').read_text());syms={s[1]:s for s in find(library,'symbol')}
    nodes={}
    for p in (ROOT/'ereader').glob('audio_aux_draft*.kicad_sch'):
        d=parse(p.read_text());check('draft_forbidden_constructs_'+p.name,'no globals/NC/exclusions/PWR_FLAG',True,
            not find(d,'global_label') and not find(d,'no_connect') and 'PWR_FLAG' not in p.read_text() and 'power:GND' not in p.read_text())
        for s in find(d,'symbol'):
            if find(s,'lib_id'):
                props={q[1]:q[2] for q in find(s,'property')};nodes[props['Reference']]=s
    check('all_259_real_native_symbols',259,len(nodes),len(nodes)==259)
    for row in i['parts'].values():
        sym=syms[row['lib'].split(':')[1]];actual={}
        for unit in find(sym,'symbol'):
            for p in find(unit,'pin'):actual[str(find(p,'number')[0][1])]=(str(find(p,'name')[0][1]),p[1])
        for no,fn,typ,n in row['pins']:
            role_ok=actual.get(no)==(fn,typ) if no in row['source_pin_pages'] else no in actual and actual[no][1]==typ
            check('symbol_pin_'+row['ref']+'_'+no,(fn,typ),actual.get(no),role_ok)
        s=nodes[row['ref']];props={p[1]:p[2] for p in find(s,'property')}
        check('all_new_fields_frozen_'+row['ref'],'blank Footprint, source MPN/value',True,props['Footprint']=='' and props['Manufacturer_Part_Number']==row['mpn'] and props['Value']==row['value'])
    # Native diagnostics: retain every old tuple; draft tuples bound by pre-attachment exact plan.
    pre=load(e/'baseline-erc.json');post=load(e/'post-erc.json')
    # KiCad's representative among three equal local RUN_U13 labels can vary between runs.
    # Only this frozen old alias partition has an explicitly witnessed equivalence.
    oldfile=ROOT/'ereader/main_3v3_supply.kicad_sch'
    assert sha(oldfile)==load(e/'baseline-file-hashes.json')['ereader/main_3v3_supply.kicad_sch']
    od=parse(oldfile.read_text());alts={}
    for label in find(od,'label'):
        if label[1]=='RUN_U13':
            loc=find(label,'at')[0];alts[str(find(label,'uuid')[0][1])]=[float(loc[1]),float(loc[2])]
    assert len(alts)==3
    anchor=next(h for h in find(od,'hierarchical_label') if h[1]=='MAIN_RUN_PERMIT')
    anchorid=str(find(anchor,'uuid')[0][1]);anchorloc=[float(x) for x in find(anchor,'at')[0][1:3]]
    oldnet=next(ep for name,ep in base['nets'].items() if name.endswith(('RUN_U13','MAIN_RUN_PERMIT')))
    assert next(ep for name,ep in a['nets'].items() if name.endswith(('RUN_U13','MAIN_RUN_PERMIT')))==oldnet
    def witness(report):
        vs=[(sh,v) for sh in report['sheets'] for v in sh['violations'] if v['type']=='multiple_net_names']
        assert len(vs)==1
        sh,v=vs[0];assert sh['path']=='/Main 3V3 digital supply/' and v['severity']=='warning'
        assert len(v['items'])==2
        l,h=v['items'];assert l['description']=="Label 'RUN_U13'" and h['description']=="Hierarchical Label 'MAIN_RUN_PERMIT'"
        assert l['uuid'] in alts and h['uuid']==anchorid
        assert [round(l['pos'][k]*100,4) for k in ['x','y']]==alts[l['uuid']]
        assert [round(h['pos'][k]*100,4) for k in ['x','y']]==anchorloc
        return {'raw':v,'sheet':sh['path']}
    bw,pw=witness(pre),witness(post)
    def normalized(report):
        result=copy.deepcopy(report)
        for sh in result['sheets']:
            for v in sh['violations']:
                if v['type']=='multiple_net_names':v['items'][0]['uuid']=sorted(alts)[0]
        return tuples(result)
    save(e/'old-alias-diagnostic-witness.json',{'before':bw,'after':pw,'frozen_file_sha256':sha(oldfile),'allowed_label_positions_mm':alts,'anchor_uuid':anchorid,'old_partition':sorted(oldnet),'scope':'one existing representative label identity; no suppression'})
    pt=normalized(pre);at=normalized(post)
    olditems={x[0] for t in pt for x in t[3]};oldactual=[t for t in at if any(x[0] in olditems for x in t[3])]
    check('every_baseline_ERC_tuple_unchanged',len(pt),len(oldactual),pt==oldactual)
    # Native report sheet attribution varies for isolated label items. UUIDs identify exact source locations;
    # normalize only the known parent prefix, then require exact type/severity/UUID/description and sheet.
    actualnew=[t for t in at if t not in oldactual]
    expected=[(('/' if t[1]=='isolated_pin_label' else '/'+PARENT_NAME+t[0]),t[1],t[2],tuple(tuple(x) for x in t[3])) for t in expect['tuples']]
    check('exact_new_ERC_tuples_pre_enumerated',len(expected),len(actualnew),sorted(expected)==sorted(actualnew))
    counts=collections.Counter(v['severity'] for s in post['sheets'] for v in s['violations'])
    check('post_ERC_counts','138errors/178warnings',dict(counts),counts=={'error':138,'warning':178})
    cp=fitz.open(ROOT/'exports/ereader_rev1.pdf');np=fitz.open(e/'post.pdf')
    check('canonical_PDF_native_all_pages',21,len(cp),len(cp)==len(np)==21 and all(cp[j].get_pixmap().samples==np[j].get_pixmap().samples for j in range(21)))
    # Native CSV fidelity plus old row invariance and exact selected union.
    bom=ROOT/'exports/ereader_rev1_bom.csv'
    with bom.open(encoding='utf-8-sig',newline='') as f_:br=list(csv.DictReader(f_))
    with (e/'baseline-bom.csv').open(encoding='utf-8-sig',newline='') as f_:oldrows=list(csv.DictReader(f_))
    check('BOM_delta_exact_259',611,len(br),len(br)==611 and {r['Reference'] for r in br}-{r['Reference'] for r in oldrows}==set(i['ref_map'].values()) and all(r in br for r in oldrows))
    run([sys.executable,str(ROOT/'scripts/check_bom_export.py'),str(e/'post.xml'),'--bom',str(bom)])
    check('BOM_native_fidelity',0,0,True)
    run(['git','diff','--check'])
    save(e/'native-audit.json',{'status':'NATIVE_DRAFT_PROGRESS','scope':'native_draft_progress','checks':checks,'source_input_sha256':sha(INPUT),'expected_erc_sha256':sha(EXPECT),'flags':i['flags'],'native_counts':[615,577,21]})
    if args.mode=='--self-test':
        tests=[]
        def reject(name,change):
            ii=copy.deepcopy(i);aa=copy.deepcopy(a);bb=copy.deepcopy(base);change(ii,aa,bb)
            try:errs=evaluate(ii,aa,bb)
            except Exception:errs=['semantic rejection']
            tests.append({'case':name,'rejected':bool(errs)});assert errs,'Negative test escaped: '+name
        r=i['ref_map']['Q_IV'];u=i['ref_map']['U_IV_N_LDO'];k=i['ref_map']['K_IV_P_OUT']
        reject('wrong_MPN',lambda ii,aa,bb:aa['components'][r].update(Manufacturer_Part_Number='incorrect'))
        reject('wrong_value',lambda ii,aa,bb:aa['components'][i['ref_map']['R_IV_GEN_EN']].update(Value='100k'))
        reject('wrong_source',lambda ii,aa,bb:aa['components'][r].update(Source_ID='wrong'))
        reject('wrong_source_page',lambda ii,aa,bb:aa['components'][r].update(Source_Pin_Pages='{}'))
        reject('missing_component',lambda ii,aa,bb:aa['components'].pop(k))
        reject('extra_component',lambda ii,aa,bb:aa['components'].update(U_EXTRA=copy.deepcopy(aa['components'][u])))
        reject('nonblank_footprint',lambda ii,aa,bb:aa['components'][r].update(Footprint='physical'))
        reject('old_field_change',lambda ii,aa,bb:aa['components'][next(iter(bb['components']))].update(Value='changed'))
        reject('erased_provider',lambda ii,aa,bb:ii['provider_obligations'].pop())
        reject('fulfilled_provider',lambda ii,aa,bb:ii['provider_states'][0].update(fulfilled=True))
        reject('provider_optional',lambda ii,aa,bb:ii['provider_states'][0].update(status='OPTIONAL'))
        reject('draft_as_full_PASS',lambda ii,aa,bb:ii.update(status='PASS'))
        reject('full_ready_flag',lambda ii,aa,bb:ii['flags'].update(integrated_audio_ready=True))
        reject('production_flag',lambda ii,aa,bb:ii['flags'].update(production_qualified=True))
        reject('physical_flag',lambda ii,aa,bb:ii['flags'].update(physical_acceptance_complete=True))
        reject('reduced_PCM',lambda ii,aa,bb:ii['targets'].update(PCM_Hz=192000))
        def move(aa,p,other):
            src=next(n for n,ep in aa['nets'].items() if p in ep);aa['nets'][src].remove(p);aa['nets'][other].add(p)
        reject('Si2323_source_drain_polarity',lambda ii,aa,bb:move(aa,(r,'2'),next(n for n,ep in aa['nets'].items() if (r,'3') in ep)))
        reject('negative_LDO_enable_wrong_rail',lambda ii,aa,bb:move(aa,(u,'5'),next(n for n,ep in aa['nets'].items() if (u,'8') in ep)))
        reject('FormB_contact_wrong_net',lambda ii,aa,bb:move(aa,(k,'3'),next(n for n,ep in aa['nets'].items() if (k,'4') in ep)))
        reject('old_root_GND_connection',lambda ii,aa,bb:move(aa,(r,'2'),next(iter(bb['nets']))))
        reject('faked_power_actor',lambda ii,aa,bb:aa['components'].update(PWR_FLAG={'Value':'PWR_FLAG'}))
        reject('source_pin_erasure',lambda ii,aa,bb:ii['pins'].pop())
        stale=copy.deepcopy(i);stale['source_hashes']['all-pin-ledger.json']='0'*64
        tests.append({'case':'stale_hash_seal','rejected':hashdata((json.dumps(stale,indent=2)+'\n').encode())!=expect['input_sha256']})
        forbidden='(global_label "GND" (at 0 0 0))'
        tests.append({'case':'global_GND_construct','rejected':bool(find(parse('(kicad_sch '+forbidden+')'),'global_label'))})
        tests.append({'case':'no_connect_erasure_of_provider','rejected':bool(find(parse('(kicad_sch (no_connect (at 0 0)))'),'no_connect'))})
        for key in ['uuid','description','pos']:
            broken=copy.deepcopy(post);vv=next(v for sh in broken['sheets'] for v in sh['violations'] if v['type']=='multiple_net_names')
            vv['items'][0][key]={'x':0,'y':0} if key=='pos' else 'outside frozen witness'
            try:witness(broken);rejected=False
            except AssertionError:rejected=True
            tests.append({'case':'alias_witness_wrong_'+key,'rejected':rejected})
        broken=copy.deepcopy(post);ss=next(sh for sh in broken['sheets'] if any(v['type']=='multiple_net_names' for v in sh['violations']));ss['violations'].append(copy.deepcopy(next(v for v in ss['violations'] if v['type']=='multiple_net_names')))
        try:witness(broken);rejected=False
        except AssertionError:rejected=True
        tests.append({'case':'additional_alias_warning','rejected':rejected})
        assert len(tests)==29 and all(x['rejected'] for x in tests);save(e/'self-test.json',{'tests':tests,'negative_tests':len(tests),'all_rejected':True})
    print('Native draft audit PASS; all integrated/source/full/production/physical flags remain false')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence-dir',type=Path,required=True);p.add_argument('--source-dir',type=Path);p.add_argument('--kicad');p.add_argument('--freeze-plan',action='store_true');g=p.add_mutually_exclusive_group();g.add_argument('--native',dest='mode',action='store_const',const='--native');g.add_argument('--audit',dest='mode',action='store_const',const='--audit');g.add_argument('--self-test',dest='mode',action='store_const',const='--self-test');g.add_argument('--privacy',dest='mode',action='store_const',const='--privacy');g.add_argument('--visual',dest='mode',action='store_const',const='--visual');p.set_defaults(mode='--audit');main(p.parse_args())
