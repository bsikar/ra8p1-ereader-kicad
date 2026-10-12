#!/usr/bin/env python3
"""Transcribe the root-adopted, unpowered AUX draft; never integrates providers.

The source directory is external and immutable. No source PDF or private graph
record is copied. Run --prepare before generation to pin fresh native baseline.
Run --generate to create the draft island, then freeze its standalone ERC before
--attach. Existing root/library-table entries are preserved verbatim.
"""
import argparse, collections, copy, csv, hashlib, json, math, re, subprocess, sys, uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'sim/kicad'))
from sexp import Q, parse, dump, find

NS = uuid.UUID('f0c43b3e-8b8a-4b6e-b861-48eb3ce5d965')
uid = lambda name: Q(str(uuid.uuid5(NS, name)))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
FONT = ['effects', ['font', ['size', '1.27', '1.27']]]
ROOT_ID = '0586cc51-9c57-495b-a0c9-c29ba0d48166'
PARENT_ID = str(uid('parent-instance'))
PARENT_UUID = str(uid('parent-file'))
BRANCHES = ['AUX5', 'IV', 'QUIET', 'LINE']
FILES = {b: f'audio_aux_draft_{b.lower()}.kicad_sch' for b in BRANCHES}
TITLES = {b: f'AUX DRAFT {b}' for b in BRANCHES}
PIN_HASH = 'e5dc151b01229407d80adb826eb78131ce64825e446d9e0d7adf000862f9db64'
PASSIVE_HASH = '12d96641bcf731e4ccae781b9e8aebd8c6c89060b21d553aa44ae0c19395ecc7'
CONTRACT_HASH = 'cfcb027fb3228c46034e894482be663833b5dfebabaffa9df85f57caa9e6aa94'
CALC_HASH = 'f7c014c1bcc206f4287c71d02aba052edcba540a3012c0f5ed62e75589339bed'
STATE_HASH = '44dfc2929f1a5a3962d894750c6473248da010a34a9ff18f1046d8819cc4ced2'

def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def writejson(p, v): p.write_text(json.dumps(v, indent=2)+'\n', encoding='utf-8')
def f(v): return f'{v:.4f}'.rstrip('0').rstrip('.') or '0'
def prop(k, v, x=0, y=0, hide=True):
    return ['property', Q(k), Q(str(v)), ['at', f(x), f(y), '0'], copy.deepcopy(FONT)+([['hide','yes']] if hide else [])]
def branch(ref):
    return next(b for b in ['QUIET', 'LINE', 'AUX5', 'IV'] if b in ref.split('_'))
def value(p):
    d=p['value']
    if p['kind']=='resistor':
        n=d['ohm'];return f'{n/1e6:g}M' if n>=1e6 else f'{n/1000:g}k' if n>=1000 else f'{n:g}R'
    if p['kind']=='capacitor':
        n=d['F_nom'];return f'{n/1e-6:g}uF' if n>=1e-6 else f'{n/1e-9:g}nF' if n>=1e-9 else f'{n/1e-12:g}pF'
    if p['kind']=='inductor':return f"{d['H_nom']/1e-6:g}uH"
    return p['mpn']
def net(n): return 'AD_RETURN' if n=='GND' else 'AD_'+n

def pin_type(mpn, fn, n):
    if mpn=='Si2323DS-T1-GE3' and fn=='G':return 'input'
    if fn in ['NC','DNC']:
        return 'no_connect' if n=='OPEN' else 'passive' # LM76005 grounded NC pads per source p4
    if mpn=='TPS65131RGER':
        if fn in ['VIN','INN','PGND','AGND','EP','VPOS','VNEG']:return 'power_in'
        if fn=='VREF':return 'power_out'
        if fn in ['FBP','FBN','ENP','ENN','PSP','PSN']:return 'input'
        if fn=='BSW':return 'output'
    if mpn.startswith('TPS7A'):
        if fn=='OUT':return 'power_out'
        if fn in ['IN','GND','EP']:return 'power_in'
        if fn in ['FB','EN']:return 'input'
    if mpn=='LM76005RNPR':
        if fn in ['PVIN','PGND','AGND','EP','BIAS']:return 'power_in'
        if fn=='VCC':return 'power_out'
        if fn in ['FB','SYNC/MODE','EN']:return 'input'
        if fn=='PGOOD':return 'open_collector'
    return 'passive'

class Sheet:
    def __init__(self, name, title, paper, path, page):
        self.name,self.path,self.page=name,path,page
        self.doc=['kicad_sch',['version','20260306'],['generator','eeschema'],['generator_version',Q('10.0')],
                  ['uuid',uid(name+'-file')],['paper',Q(paper)],['title_block',['title',Q(title)],
                  ['comment','1',Q('DRAFT / 17 UNFULFILLED PROVIDERS / DO NOT ENABLE')]],['lib_symbols']]
        self.libs=self.doc[-1];self.bounds=[]
    def text(self,t,x,y,size=1.27):
        self.doc.append(['text',Q(t),['exclude_from_sim','no'],['at',f(x),f(y),'0'],
                         ['effects',['font',['size',str(size),str(size)]],['justify','left','top']],['uuid',uid(self.name+t)]])
    def wire(self,a,b,key):
        self.doc.append(['wire',['pts',['xy',f(a[0]),f(a[1])],['xy',f(b[0]),f(b[1])]],
                        ['stroke',['width','0'],['type','default']],['uuid',uid(self.name+key)]])
    def label(self,n,p,rot=0):
        self.doc.append(['label',Q(n),['at',f(p[0]),f(p[1]),str(rot)],copy.deepcopy(FONT)+
                        [['justify','left' if rot==0 else 'right','bottom']],['uuid',uid(self.name+n+str(p))]])
    def endpoint(self,n,p,side,key):
        if n=='OPEN':return
        q=(p[0]+(5.08 if side=='right' else -5.08),p[1]);self.wire(p,q,key);self.label(net(n),q,0 if side=='right' else 180)
    def hport(self,n,x,y,kind='passive'):
        self.doc.append(['hierarchical_label',Q(net(n)),['shape',kind],['at',f(x),f(y),'0'],
                         copy.deepcopy(FONT)+[['justify','left']],['uuid',uid(self.name+'hport'+n)]])
        # Boundary text lies to the right; the short conductor and local label
        # approach from the left, keeping the wire out of the label body.
        self.wire((x,y),(x-5.08,y),'hwire'+n);self.label(net(n),(x-5.08,y),180)
    def add_part(self,row,lib,px,py,pins,mpn,source,page,condition,rotation=0,auto_labels=True):
        # pins=(number,function,type,net). Each endpoint is source-accounted.
        name=lib.split(':')[1]
        if not any(s[1]==lib for s in self.libs[1:]):self.libs.append(copy.deepcopy(symbols[name]))
        inst=['symbol',['lib_id',Q(lib)],['at',f(px),f(py),str(rotation)],['unit','1'],['exclude_from_sim','no'],
              ['in_bom','yes'],['on_board','yes'],['dnp','no'],['uuid',uid(row['ref'])]]
        top=max(y for x,y,side in pincoords[name].values())+2.54
        for sub in find(symbols[name],'symbol'):
            for r in find(sub,'rectangle'):top=max(top,float(find(r,'start')[0][2])+2.54)
        if rotation in [90,270] and name in ['resistor','capacitor','inductor']:
            refs=(px+5.08,py-1.27);vals=(px+5.08,py+1.27)
        else:refs=(px,py-top-5.08);vals=(px,py-top-2.54)
        rp=prop('Reference',row['ref'],*refs,False);vp=prop('Value',row['value'],*vals,False)
        if rotation in [90,270]:
            find(rp,'at')[0][3]='90';find(vp,'at')[0][3]='90'
        if name=='Si2323DS_T1_GE3' and rotation in [90,270]:
            find(rp,'at')[0][1:3]=[f(px+12.7),f(py-12.7)];find(vp,'at')[0][1:3]=[f(px+12.7),f(py-10.16)]
            rp[-1].append(['justify','left']);vp[-1].append(['justify','left'])
        if rotation in [90,270] and name in ['resistor','capacitor','inductor']:
            rp[-1].append(['justify','left']);vp[-1].append(['justify','left'])
        inst += [rp,vp,
                 prop('Footprint','',px,py),prop('Datasheet',urls[source],px,py),
                 prop('Manufacturer_Part_Number',mpn,px,py),prop('Manufacturer_Name',manufacturers[source],px,py),
                 prop('Source_Reference',row['source_ref'],px,py),prop('Source_ID',source,px,py),
                 prop('Source_Page',page,px,py),prop('Source_Condition',condition,px,py),
                 prop('Source_Pin_Pages',json.dumps(row['source_pin_pages'],sort_keys=True),px,py),
                 prop('Selection_Basis','Exact sealed AUX local source ledger; conditional draft',px,py),
                 prop('Sourcing_Snapshot','Source snapshot 2026-10-11; no live availability claim',px,py),
                 prop('Procurement_Status','DRAFT / DO NOT ENABLE / 17 UNFULFILLED providers',px,py)]
        inst += [['pin',Q(p[0]),['uuid',uid(row['ref']+'pin'+p[0])]] for p in pins]
        inst.append(['instances',['project',Q('ereader_rev1'),['path',Q(self.path),['reference',Q(row['ref'])],['unit','1']]],
                                 ['project',Q('audio_aux_draft'),['path',Q(self.path.replace('/'+ROOT_ID+'/'+PARENT_ID,'/'+PARENT_UUID)),['reference',Q(row['ref'])],['unit','1']]]])
        self.doc.append(inst)
        coords=pincoords[name];out={};angle=math.radians(rotation)
        for no,fn,typ,n in pins:
            x,y,side=coords[no];xx=x*math.cos(angle)-y*math.sin(angle);yy=x*math.sin(angle)+y*math.cos(angle)
            point=(round(px+xx,4),round(py-yy,4));out[no]=point
            if auto_labels:self.endpoint(n,point,'right' if xx>=0 else 'left',row['ref']+no)
        return out
    def junction(self,p,key):
        self.doc.append(['junction',['at',f(p[0]),f(p[1])],['diameter','0'],['color','0','0','0','0'],['uuid',uid(self.name+'junction'+key)]])
    def save(self):
        self.doc += [['embedded_fonts','no']];(ROOT/'ereader'/self.name).write_text(dump(self.doc)+'\n',encoding='utf-8')

symbols={};pincoords={}
def box(name,pins,graphic='box'):
    # 100mil pin grid, 50mil text; custom electrical symbols have no physical fields.
    count=len(pins);by={p[0]:p for p in pins};bottom=[]
    if name=='TPS65131RGER':
        left=[by[n] for n in ['4','5','6','7','8','10','9','11','12','20']]
        right=[by[n] for n in ['1','24','23','22','13','14','15','16','17','21','18']];bottom=[by[n] for n in ['2','3','19','EP']]
    elif name=='LM76005RNPR':
        left=[by[n] for n in ['20','21','22','18','17','9','7','23','10','11']]
        right=[by[n] for n in ['1','2','3','4','5','6','12','16','8']];bottom=[by[n] for n in ['13','14','15','19','24','25','26','27','28','29','30','EP']]
    elif name.startswith('TPS7A'):
        left=[by[n] for n in ['8','5','6']];right=[by[n] for n in ['1','2','3','7']];bottom=[by[n] for n in ['4','EP']]
    else:left=pins[:math.ceil(count/2)];right=pins[math.ceil(count/2):]
    width=20.32 if name=='LM76005RNPR' else 15.24 if count>9 else 12.7
    h=max(12.7 if count>4 else 5.08,max(len(left),len(right))*2.54/2+2.54)
    body=['symbol',Q(name+'_0_1'),['rectangle',['start',f(-width),f(h)],['end',f(width),f(-h)],
          ['stroke',['width','0.254'],['type','default']],['fill',['type','background']]]]
    # Form B contact is explicitly closed at LED=0; tiny conventional diode/PMOS details are annotated.
    unit=['symbol',Q(name+'_1_1')];coords={}
    for group,sign in [(left,-1),(right,1)]:
        for i,(n,fn,typ,_) in enumerate(group):
            x=sign*(width+3.81);y=h-2.54*(i+1);side='left' if sign<0 else 'right';coords[n]=(x,y,side)
            unit.append(['pin',typ,'line',['at',f(x),f(y),'0' if sign<0 else '180'],['length','3.81'],
                         ['name',Q(fn),copy.deepcopy(FONT)],['number',Q(n),copy.deepcopy(FONT)]])
    for i,(n,fn,typ,_) in enumerate(bottom):
        x=(i-(len(bottom)-1)/2)*2.54;y=-h-3.81;coords[n]=(x,y,'bottom')
        unit.append(['pin',typ,'line',['at',f(x),f(y),'90'],['length','3.81'],['name',Q(fn),copy.deepcopy(FONT)],['number',Q(n),copy.deepcopy(FONT)]])
    s=['symbol',Q('Aux_Draft:'+name),['pin_names',['offset','0.508']],['exclude_from_sim','no'],['in_bom','yes'],['on_board','yes'],
       prop('Reference','U',0,h+5.08,False),prop('Value',name,0,h+2.54,False),prop('Footprint',''),prop('Datasheet',''),body,unit]
    if graphic=='form_b':
        body.append(['text',Q('Form B / NC at LED=0'),['at','0',f(-h+1.27),'0'],['effects',['font',['size','1.27','1.27']]]])
    symbols[name]=s;pincoords[name]=coords

def primitive(name,pins,kind):
    # All ordinary R/C/L/D use stock KiCad Device geometry, not rectangular IC stand-ins.
    if name in symbols:return
    stock=Path(args.kicad).parents[1]/'share/kicad/symbols/Device.kicad_sym'
    doc=parse(stock.read_text(encoding='utf-8'))
    src=next(s for s in find(doc,'symbol') if s[1]==kind)
    s=copy.deepcopy(src);s[1]=Q('Aux_Draft:'+name)
    for sub in find(s,'symbol'):
        sub[1]=Q(str(sub[1]).replace(kind,name,1))
    for p in find(s,'property'):
        if p[1]=='Footprint':p[2]=Q('')
    coords={}
    for sub in find(s,'symbol'):
        for p in find(sub,'pin'):
            if kind=='Q_PMOS':find(p,'number')[0][1]=Q({'G':'1','S':'2','D':'3'}[str(find(p,'name')[0][1])])
            if kind=='D_Schottky':find(p,'name')[0][1]=Q({'1':'CATHODE','2':'ANODE'}[str(find(p,'number')[0][1])])
            a=find(p,'at')[0];n=str(find(p,'number')[0][1]);coords[n]=(float(a[1]),float(a[2]),'right' if float(a[1])>=0 else 'left')
    # Rotate stock vertical passive to horizontal, endpoints +/-3.81 on one row.
    if kind in ['R','C','L']:
        for sub in find(s,'symbol'):
            for item in sub[2:]:
                if not isinstance(item,list):continue
                for kw in ['at','start','end','center']:
                    for a in find(item,kw):
                        x,y=float(a[1]),float(a[2]);a[1],a[2]=f(-y),f(x)
                        if kw=='at' and item[0]=='pin':a[3]=str((int(a[3])+90)%360)
                for pts in find(item,'pts'):
                    for a in find(pts,'xy'):
                        x,y=float(a[1]),float(a[2]);a[1],a[2]=f(-y),f(x)
        coords={n:(-y,x,'left' if -y<0 else 'right') for n,(x,y,side) in coords.items()}
    symbols[name]=s;pincoords[name]=coords

def sheetnode(name,file,sid,x,y,w,h,page,ports):
    node=['sheet',['at',f(x),f(y)],['size',f(w),f(h)],['exclude_from_sim','no'],['in_bom','yes'],['on_board','yes'],['dnp','no'],
          ['stroke',['width','0.254'],['type','solid']],['fill',['color','0','0','0','0']],['uuid',Q(sid)],
          prop('Sheetname',name,x+w/2,y-3.81,False),prop('Sheetfile',file,x+w/2,y+h+3.81,False)]
    coords={}
    for i,n in enumerate(ports):
        p=(x,y+5.08+i*5.08);coords[n]=p
        node.append(['pin',Q(net(n)),'passive',['at',f(p[0]),f(p[1]),'180'],['uuid',uid(sid+n)],copy.deepcopy(FONT)+[['justify','left']]])
    node.append(['instances',['project',Q('ereader_rev1'),['path',Q('/'+ROOT_ID+'/'+PARENT_ID if sid!=PARENT_ID else '/'+ROOT_ID),['page',Q(str(page))]]],
                            ['project',Q('audio_aux_draft'),['path',Q('/'+PARENT_UUID),['page',Q(str(page-16))]]]])
    return node,coords

def cli(argv):
    r=subprocess.run([args.kicad]+argv,cwd=ROOT,capture_output=True,text=True)
    if r.returncode:raise RuntimeError('KiCad export failed: '+str(r.returncode))
    return r

def bom_command(output,schematic):
    with (ROOT/'exports/ereader_rev1_bom.csv').open(encoding='utf-8-sig',newline='') as f_:header=next(csv.reader(f_))
    gen={'Qty':'QUANTITY','DNP':'DNP','Exclude from BOM':'EXCLUDE_FROM_BOM','Exclude from Board':'EXCLUDE_FROM_BOARD'}
    return ['sch','export','bom','--output',str(output),'--fields',','.join(gen.get(h,h) for h in header),'--labels',','.join(header),str(schematic)]

def main():
    B=args.source_dir;E=args.evidence_dir;E.mkdir(parents=True,exist_ok=True)
    P=load(B/'passive-ledger.json');N=load(B/'all-pin-ledger.json');C=load(B/'contract.json')
    for name,h in [('all-pin-ledger.json',PIN_HASH),('passive-ledger.json',PASSIVE_HASH),('contract.json',CONTRACT_HASH),('calculations.json',CALC_HASH),('state-matrix.json',STATE_HASH)]:
        assert sha(B/name)==h,'Stale source hash: '+name
    if args.prepare:
        for av in [['sch','export','netlist','--format','kicadxml','--output',str(E/'baseline.xml'),'ereader/ereader_rev1.kicad_sch'],
                   ['sch','erc','--format','json','--output',str(E/'baseline-erc.json'),'ereader/ereader_rev1.kicad_sch'],
                   ['sch','export','pdf','--output',str(E/'baseline.pdf'),'ereader/ereader_rev1.kicad_sch'],bom_command(E/'baseline-bom.csv','ereader/ereader_rev1.kicad_sch')]:cli(av)
        tracked=subprocess.check_output(['git','ls-files'],cwd=ROOT,text=True).splitlines()
        writejson(E/'baseline-file-hashes.json',{p:sha(ROOT/p) for p in tracked if (ROOT/p).is_file()})
        print('Fresh native baseline prepared');return
    if args.attach:
        p=ROOT/'ereader/ereader_rev1.kicad_sch';text=p.read_text(encoding='utf-8')
        assert PARENT_ID not in text,'Already attached'
        # Root A2: compact review-only sheet in the empty upper-right corner.
        nd,_=sheetnode('AUX DRAFT / DO NOT ENABLE','audio_aux_draft.kicad_sch',PARENT_ID,436.88,35.56,127,25.4,17,[])
        end=text.rfind(')');p.write_text(text[:end]+dump(nd)+'\n'+text[end:],encoding='utf-8')
        print('Review-only hierarchy attached, zero root pins');return
    assert args.generate
    source_info=load(B/'sources.json')
    global urls,manufacturers
    urls={s['id']:s['url'] for s in source_info}
    manufacturers={'tps65131':'Texas Instruments','tps7a49-real':'Texas Instruments','tps7a30-real':'Texas Instruments','lm76005':'Texas Instruments',
                   'si2323':'Vishay','mbrm120':'onsemi','xal1010':'Coilcraft','tnpw':'Vishay','kemet-x7r':'KEMET','kemet-c0g':'KEMET','photomos':'Panasonic'}
    refs=sorted(set(p['ref'] for p in P)|set(n['ref'] for n in N))
    counts=collections.Counter();mapping={}
    for r in refs:
        counts[r[0]]+=1;mapping[r]=r[0]+'AD'+str(counts[r[0]])
    pp={p['ref']:p for p in P};pn={r:[n for n in N if n['ref']==r] for r in refs}
    rows={};pins={}
    for r in refs:
        pr=pp.get(r);nr=pn[r]
        mpn=pr['mpn'] if pr else nr[0]['mpn'];v=value(pr) if pr else mpn
        if nr:
            pins[r]=[(n['pin'],n['function'],pin_type(mpn,n['function'],n['net']),n['net']) for n in nr]
        elif pr['kind']=='rectifier':
            pins[r]=[('1','K','passive',pr['endpoints']['cathode']),('2','A','passive',pr['endpoints']['anode'])]
        else:pins[r]=[(str(i+1),str(i+1),'passive',n) for i,n in enumerate(pr['endpoints'])]
        rows[r]={'source_ref':r,'ref':mapping[r],'mpn':mpn,'value':v,'sheet':branch(r),'pins':pins[r],
                 'source_pin_pages':{n['pin']:{'source':n['source'],'page':n['page'],'function':n['function']} for n in nr}}
        name=mpn.replace('-','_').replace('/','_')
        if pr and pr['kind'] in ['resistor','capacitor','inductor','rectifier']:
            name=pr['kind'];primitive(name,pins[r],{'resistor':'R','capacitor':'C','inductor':'L','rectifier':'D_Schottky'}[name])
        elif mpn=='Si2323DS-T1-GE3':primitive(name,pins[r],'Q_PMOS')
        else:box(name,pins[r],'form_b' if mpn=='AQY412EHAX' else 'box')
        rows[r]['lib']='Aux_Draft:'+name
    # Shared-return-only hierarchy. The separate branch 5V input partitions are deliberately NOT joined.
    ports={b:['GND']+(['AUX_SOURCE','AUX5_ENABLE','AUX5V'] if b=='AUX5' else
            [b+'_5V_INPUT',b+'_GEN_ENABLE',b+'_LDO_ENABLE',b+'_P',b+'_N']+
            [n['net'] for n in N if branch(n['ref'])==b and n['function'] in ['LED_A','LED_K']]) for b in BRANCHES}
    parent=Sheet('audio_aux_draft.kicad_sch','Isolated AUX draft / source-local envelope','A2','/'+ROOT_ID+'/'+PARENT_ID,17)
    parent.doc[4]=['uuid',Q(PARENT_UUID)]
    parent.text('DRAFT / AUXILIARY LOCAL ENVELOPE ONLY / 17 UNFULFILLED PROVIDERS / DO NOT ENABLE',15.24,12.7,1.8)
    parent.text('Review island only. No root pins, global nets, ground alias, provider drivers or manufacture release.\nAUX5V and branch 5V inputs are distinct source partitions; supply-routing/hold provider is absent.',15.24,20.32)
    placements={'AUX5':(71.12,55.88,101.6,40.64),'IV':(71.12,160.02,101.6,129.54),'QUIET':(256.54,160.02,101.6,129.54),'LINE':(441.96,160.02,101.6,129.54)}
    for b in BRANCHES:
        sid=str(uid(b+'-instance'));path='/'+ROOT_ID+'/'+PARENT_ID+'/'+sid
        sh=Sheet(FILES[b],f'{b} local AUX draft / DO NOT ENABLE','A3' if b=='AUX5' else 'A2',path,18+BRANCHES.index(b))
        sh.text('DRAFT / 17 UNFULFILLED PROVIDERS / DO NOT ENABLE',15.24,12.7,1.8)
        sh.text('Source-local return only. All boundary providers absent; supply partitions remain separate.',15.24,20.32)
        pts={};done=set();serial=[0]
        def put(r,x,y,rot=0):
            pr=pp.get(r);info=pr or pn[r][0]
            pts[r]=sh.add_part(rows[r],rows[r]['lib'],x,y,pins[r],rows[r]['mpn'],info['source'],
                'see Source_Condition' if pr else info['page'],pr['condition'] if pr else 'Conditional source pin table',rot,False)
            return pts[r]
        def at(r,n):return pts[r][str(n)]
        def line(a,c):
            if a==c:return
            serial[0]+=1;sh.wire(a,c,'local'+str(serial[0]));sh.junction(a,'a'+str(serial[0]));sh.junction(c,'c'+str(serial[0]))
        def route(a,*cs):
            for c in cs:line(a,c);a=c
        def alias(r,n):
            n=str(n);v=next(p[3] for p in pins[r] if p[0]==n)
            if v=='OPEN' or (r,n) in done:return
            p=at(r,n);lc=pincoords[rows[r]['lib'].split(':')[1]][n]
            # Use the actual rotated pin direction for ordinary vertical parts.
            inst=next(i for i in reversed(sh.doc) if isinstance(i,list) and i and i[0]=='symbol' and find(i,'property')[0][2]==rows[r]['ref'])
            rot=float(find(inst,'at')[0][3]);a=math.radians(rot);dx=lc[0]*math.cos(a)-lc[1]*math.sin(a);dy=-(lc[0]*math.sin(a)+lc[1]*math.cos(a))
            if abs(dy)>abs(dx):q=(p[0],p[1]+(5.08 if dy>0 else -5.08));lr=0
            else:q=(p[0]+(5.08 if dx>=0 else -5.08),p[1]);lr=0 if dx>=0 else 180
            line(p,q);sh.label(net(v),q,lr);done.add((r,n))
        def join(addresses,y):
            ns={next(p[3] for p in pins[r] if p[0]==str(n)) for r,n in addresses};assert len(ns)==1 and 'OPEN' not in ns
            ps=[at(r,n) for r,n in addresses];xs=sorted(set(p[0] for p in ps))
            for x1,x2 in zip(xs,xs[1:]):line((x1,y),(x2,y))
            for (r,n),p in zip(addresses,ps):line(p,(p[0],y));done.add((r,str(n)));sh.junction((p[0],y),str(serial[0])+r+str(n))
            sh.label(net(next(iter(ns))),(xs[0],y),180)
        def bank(rr,x,y,pitch=20.32):
            for j,r in enumerate(rr):put(r,x+j*pitch,y,270)
            join([(r,'1') for r in rr],y-12.7);join([(r,'2') for r in rr],y+12.7)
        def pair(a,na,c,nc):
            assert next(p[3] for p in pins[a] if p[0]==str(na))==next(p[3] for p in pins[c] if p[0]==str(nc))
            pa,pb=at(a,na),at(c,nc);route(pa,(pb[0],pa[1]),pb);done.update([(a,str(na)),(c,str(nc))])
        def divider(top,bot,ff,x,y):
            put(top,x,y,270);put(bot,x,y+22.86,270);put(ff,x+20.32,y,270)
            join([(top,'1'),(ff,'1')],y-12.7)
            join([(top,'2'),(bot,'1'),(ff,'2')],y+11.43)
        selected=[r for r in refs if branch(r)==b]
        if b=='AUX5':
            put('U_AUX5',96.52,91.44)
            bank(['C_AUX5_IN_'+str(j) for j in range(4)]+['C_AUX5_IN_HF'],30.48,43.18,17.78)
            # Shared PVIN rail and local IC return pins are wired in short groups.
            pv=[('U_AUX5',str(j)) for j in [20,21,22]]
            x=at(*pv[0])[0]-10.16
            for r,n in pv:route(at(r,n),(x,at(r,n)[1]));done.add((r,n))
            line((x,at(*pv[0])[1]),(x,at(*pv[-1])[1]));sh.label(net('AUX_SOURCE'),(x,at(*pv[0])[1]),180)
            swx=144.78;sw=[('U_AUX5',str(j)) for j in range(1,6)]
            for r,n in sw:line(at(r,n),(swx,at(r,n)[1]));done.add((r,n))
            line((swx,at(*sw[0])[1]),(swx,at(*sw[-1])[1]));put('L_AUX5',165.1,at(*sw[0])[1]);line((swx,at(*sw[0])[1]),at('L_AUX5','1'));done.add(('L_AUX5','1'))
            put('C_AUX5_BOOT',162.56,96.52);pair('U_AUX5','6','C_AUX5_BOOT','1');pair('C_AUX5_BOOT','2','L_AUX5','1')
            for k in range(2):bank(['C_AUX5_OUT_'+str(j) for j in range(k*14,(k+1)*14)],208.28,86.36+k*43.18,12.7)
            route(at('L_AUX5','2'),(195.58,at('L_AUX5','2')[1]),(195.58,73.66),(208.28,73.66));done.add(('L_AUX5','2'))
            divider('R_AUX5_TOP','R_AUX5_BOT','C_AUX5_FF',167.64,149.86)
            # Feedback wire reaches its local divider; its upper rail aliases the output bank.
            p=at('U_AUX5','12');route(p,(147.32,p[1]),(147.32,161.29),(167.64,161.29));done.add(('U_AUX5','12'))
            bank(['C_AUX5_VCC','C_AUX5_BIAS'],50.8,154.94,35.56) if False else None
            put('C_AUX5_VCC',50.8,152.4,270);put('C_AUX5_BIAS',86.36,152.4,270);put('R_AUX5_EN',30.48,109.22,270);put('R_AUX5_PG',127,175.26)
            # Local input, bootstrap, feedback, VCC, BIAS and enable parts belong to the converter block.
            route((30.48,30.48),(22.86,30.48),(22.86,at('U_AUX5','20')[1]),(x,at('U_AUX5','20')[1]))
            route((208.28,73.66),(195.58,73.66),(195.58,116.84),(208.28,116.84))
            route((195.58,116.84),(195.58,137.16),(167.64,137.16))
            pv=at('U_AUX5','8');route(pv,(132.08,pv[1]),(132.08,139.7),(50.8,139.7),at('C_AUX5_VCC','1'));done.update([('U_AUX5','8'),('C_AUX5_VCC','1')])
            pv=at('U_AUX5','17');route(pv,(58.42,pv[1]),(58.42,139.7));done.add(('U_AUX5','17'))
            pv=at('U_AUX5','9');route(pv,(63.5,pv[1]),(63.5,134.62),(86.36,134.62),at('C_AUX5_BIAS','1'));done.update([('U_AUX5','9'),('C_AUX5_BIAS','1')]);sh.label(net('AUX5V'),(86.36,134.62),0)
            pair('U_AUX5','18','R_AUX5_EN','1');sh.label(net('AUX5_ENABLE'),at('R_AUX5_EN','1'),180);pair('U_AUX5','16','R_AUX5_PG','1')
            join([('U_AUX5',str(j)) for j in [13,14,15,19,24,25,26,27,28,29,30,'EP']],123.19)
            sh.text('Forced PWM: SYNC=VCC. RT/SS and NC7/23 physically open.\n28 x 10uF output bank; 140..354.2uF conditional effective total.\nAUX5V does not supply the three branch inputs in this draft.',15.24,207.01)
            for i,n in enumerate(ports[b]):sh.hport(n,63.5+i*96.52,240.03)
        else:
            u='U_'+b;put(u,104.14,93.98)
            q='Q_'+b;put(q,139.7,38.1,270);put('R_'+b+'_GATE',111.76,30.48)
            lp='L_'+b+'_P';dp='D_'+b+'_P';put(lp,172.72,40.64);put(dp,205.74,40.64,180)
            pair(q,'3',lp,'1');sh.label(net(b+'_P_L_IN'),at(lp,'1'),180);pair(lp,'2',dp,'2')
            put('C_'+b+'_GEN_P_IN',157.48,63.5,270)
            bank(['C_'+b+'_P_PRE_'+str(j) for j in range(4)],223.52,66.04)
            p=at(dp,'1');route(p,(p[0],53.34),(223.52,53.34));done.add((dp,'1'))
            # Both switch pins share the inductor/rectifier switching node.
            for n in ['1','24']:
                p=at(u,n);route(p,(185.42,p[1]),(185.42,40.64));done.add((u,n))
            put('R_'+b+'_VIN',48.26,63.5);put('C_'+b+'_GEN_N_IN',25.4,86.36,270);put('C_'+b+'_VIN',58.42,86.36,270);put('R_'+b+'_GEN_EN',50.8,124.46,270)
            divider('R_'+b+'_GEN_P_TOP','R_'+b+'_GEN_P_BOT','C_'+b+'_GEN_P_FF',284.48,99.06)
            ln='L_'+b+'_N';dn='D_'+b+'_N';put(ln,172.72,147.32,270);put(dn,205.74,134.62)
            pair(ln,'1',dn,'1')
            for n in ['13','14']:
                p=at(u,n);route(p,(152.4,p[1]),(152.4,134.62),at(dn,'1'));done.add((u,n))
            bank(['C_'+b+'_N_PRE_'+str(j) for j in range(4)],223.52,157.48)
            p=at(dn,'2');route(p,(p[0],144.78),(223.52,144.78));done.add((dn,'2'))
            divider('R_'+b+'_GEN_N_TOP','R_'+b+'_GEN_N_BOT','C_'+b+'_GEN_N_FF',284.48,190.5)
            for j,suf in enumerate(['CP','CN','VREF']):put('C_'+b+'_'+suf,172.72+j*33.02,203.2,270)
            join([(u,n) for n in ['2','3','19','EP']],119.38)
            for sign,cy in [('P',63.5),('N',165.1)]:
                lu='U_'+b+'_'+sign+'_LDO';put(lu,431.8,cy)
                pre='C_'+b+'_'+sign+'_';rt='R_'+b+'_'+sign+'_'
                put(pre+'IN',375.92,cy+25.4,270);put(pre+'NR',398.78,cy+48.26,270)
                divider(rt+'TOP',rt+'BOT',pre+'FF',457.2,cy+25.4)
                put(pre+'OUT',505.46,cy+25.4,270);put(rt+'PRELOAD',535.94,cy+25.4,270)
                join([(pre+'OUT','1'),(rt+'PRELOAD','1'),(rt+'TOP','1'),(pre+'FF','1')],cy+12.7)
                p=at(lu,'1');route(p,(551.18,p[1]),(551.18,cy+12.7),(535.94,cy+12.7));done.add((lu,'1'))
                p=at(lu,'2');route(p,(447.04,p[1]),(447.04,cy+36.83),(457.2,cy+36.83));done.add((lu,'2'))
                p=at(lu,'8');route(p,(365.76,p[1]),(365.76,cy+12.7),(375.92,cy+12.7),at(pre+'IN','1'));done.add((lu,'8'));done.add((pre+'IN','1'));sh.label(net(b+'_'+sign+'_PRE'),(365.76,p[1]),180)
                p=at(lu,'6');route(p,(398.78,p[1]),at(pre+'NR','1'));done.add((lu,'6'));done.add((pre+'NR','1'));sh.label(net(b+'_'+sign+'_NR'),(398.78,p[1]),180)
                join([(pre+'IN','2'),(pre+'NR','2'),(pre+'OUT','2'),(rt+'PRELOAD','2'),(rt+'BOT','2'),(lu,'4'),(lu,'EP')],cy+63.5)
            put('R_'+b+'_LDO_EN',350.52,177.8,270)
            # Each Form B drain has its actual series resistor path drawn locally.
            relays=sorted(r for r in selected if r.startswith('K_'))
            for j,r in enumerate(relays):
                x=76.2+(j%3)*172.72;y=292.1+(j//3)*34.29;put(r,x,y)
                rr=sorted(k for k in selected if k.startswith('R_'+r) and k not in pts)
                for k,rrr in enumerate(rr):put(rrr,x+43.18+k*25.4,y+2.54)
                pair(r,'4',rr[0],'1')
                for a,c in zip(rr,rr[1:]):pair(a,'2',c,'1')
            sh.text('Si2323 G1/S2/D3. TPS7A30 EN uses positive 2..5.25V, default-low 10k.\nForm B contacts closed at LED=0; all LED drivers remain external and absent.',15.24,394.97)
            for i,n in enumerate(ports[b]):sh.hport(n,76.2+(i%4)*139.7,241.3+(i//4)*6.35)
        assert set(pts)==set(selected),'Layout omitted source components: '+str(set(selected)-set(pts))
        for r in selected:
            for n,fn,typ,v in pins[r]:alias(r,n)
        sh.save()
        x,y,w,h=placements[b];nd,pc=sheetnode(TITLES[b],FILES[b],sid,x,y,w,h,18+BRANCHES.index(b),ports[b]);parent.doc.append(nd)
        parent.wire(pc['GND'],(pc['GND'][0]-15.24,pc['GND'][1]),b+'return');parent.label('AD_RETURN',(pc['GND'][0]-15.24,pc['GND'][1]),180)
    # All 17 source numeric predicates/owners remain in the checked-in input snapshot.
    obligations=C['provider_obligations']
    for i,o in enumerate(obligations):
        parent.text(f"{i+1:02}: {o['id']} / UNFULFILLED",15.24+(i//9)*282,305+(i%9)*6.35)
    parent.text('259 components / 289 source pin rows plus every passive endpoint. Full audio/digital/display/reset AND remains false.\nDesktop budget 10.598354W <=11W; quiet 7.958557W <=8.2W are conditional source calculations, not powered-circuit acceptance.\nAll modes, PCM768k / DSD512 / DoP256, stereo speakers, A01..A20 and physical requirements remain open under their owners.',15.24,369.57)
    parent.save()
    library=['kicad_symbol_lib',['version','20241209'],['generator','kicad_symbol_editor'],['generator_version',Q('10.0')]]
    for name,s in symbols.items():
        ls=copy.deepcopy(s);ls[1]=Q(name);library.append(ls)
    (ROOT/'libs/symbols/Aux_Draft.kicad_sym').write_text(dump(library)+'\n',encoding='utf-8')
    table=ROOT/'ereader/sym-lib-table';t=table.read_text()
    if '"Aux_Draft"' not in t:
        at=t.rfind(')');table.write_text(t[:at]+'\t(lib (name "Aux_Draft") (type "KiCad") (uri "${KIPRJMOD}/../libs/symbols/Aux_Draft.kicad_sym") (options "") (descr "Isolated unpowered AUX draft electrical symbols"))\n'+t[at:],encoding='utf-8')
    inputdoc={'pins':N,'passives':P,'provider_obligations':obligations,'state_matrix':load(B/'state-matrix.json'),
              'intrinsic_unknowns':C['intrinsic_unknowns'],'targets':C['targets'],'original_A_records':C['original_A_records'],
              'calculations':load(B/'calculations.json'),'interfaces':C['interfaces'],
              'source_hashes':{n:sha(B/n) for n in ['contract.json','all-pin-ledger.json','passive-ledger.json','calculations.json','state-matrix.json','sources.json']},
              'sources':[{'id':s['id'],'url':s['url'],'sha256':s['sha256']} for s in source_info],
              'ref_map':mapping,'net_map':{n:net(n) for n in sorted({n['net'] for n in N if n['net']!='OPEN'}|{e for p in P for e in (p['endpoints'].values() if isinstance(p['endpoints'],dict) else p['endpoints'])})},
              'parts':rows,'ports':ports,'provider_states':[{'id':o['id'],'status':'UNFULFILLED','fulfilled':False,'READY_prerequisite':False} for o in obligations],
              'status':'NATIVE_DRAFT_PROGRESS','scope':'native_draft_progress',
              'flags':{k:False for k in ['whole_source_accepted','integrated_audio_ready','whole_display_ready','qualified_circuit_ready','all_original_requirements_met','production_qualified','physical_acceptance_complete','joint_accepted','goal_complete','disposition_coverage_complete']}}
    # Reject any accidental private source or graph path before repository serialization.
    assert not re.search(r'youtrack|\.harness|bearer\s|authorization|api[_-]?token',json.dumps(inputdoc),re.I)
    writejson(ROOT/'design/audio_aux_draft_inputs.json',inputdoc)
    writejson(E/'generated-plan.json',{'part_count':len(rows),'pin_rows':len(N),'ports':ports,'source_hashes':inputdoc['source_hashes']})
    print('Generated isolated AUX circuit: 259 parts, 289 source pin rows, 17 unfulfilled providers')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--source-dir',type=Path,required=True);ap.add_argument('--evidence-dir',type=Path,required=True);ap.add_argument('--kicad',required=True)
    g=ap.add_mutually_exclusive_group(required=True);g.add_argument('--prepare',action='store_true');g.add_argument('--generate',action='store_true');g.add_argument('--attach',action='store_true')
    args=ap.parse_args();main()
