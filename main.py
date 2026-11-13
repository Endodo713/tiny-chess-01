import json,os,urllib.request as w
U=os.environ.get("MAKEFUN_ENV_URL") or exit()
N,E,S,W=-10,1,10,-1
A=(N,E,S,W);B=(-9,11,9,-11);Q=A+B
D={'P':(N,-20,-11,-9),'N':(-19,-8,12,21,19,8,-12,-21),'B':B,'R':A,'Q':Q,'K':Q}
V={'.':0,'P':100,'N':320,'B':330,'R':500,'Q':900,'K':20000}
T={'P':'kkkkkkkkuuuuuuuummoqqommllmppmllkkkookkkljikkijllmmggmmlkkkkkkkk','N':'aceeeecacgkkkkgcekmnnmkeelnoonleeknoonkeelmnnmlecgkllkgcaceeeeca','B':'giiiiiigikkkkkkiiklmmlkiillmmlliikmmmmkiimmmmmmiilkkkkligiiiiiig','R':'k'*64,'Q':'k'*64,'K':'eccaacceeccaacceeccaacceeccaaccegeecceegiggggggiookkkkoooqmkkmqo'}
PT={p:[(V[p]+(ord(t[(s//10-2)*8+s%10-1])-107)*5)if 0<=9-s//10<8 and 0<=s%10-1<8 else 0 for s in range(120)]for p,t in T.items()}
M=10**6;I=10**9
def gen(bd,ep):
 ms=[]
 for i,p in enumerate(bd):
  if p not in 'PNBRQK':continue
  for d in D[p]:
   j=i+d
   while True:
    q=bd[j]
    if q in ' \nPNBRQK':break
    if p=='P':
     if d in(N,-20)and q!='.':break
     if d==-20 and(i<81 or bd[i+N]!='.'):break
     if d in(-11,-9)and q=='.'and j!=ep:break
     if 21<=j<=28:
      for r in 'QRBN':ms.append((i,j,r))
      break
    ms.append((i,j,''))
    if p in 'PNK' or q in 'pnbrqk':break
    if i==91 and bd[j+E]=='K':ms.append((j+E,j+W,''))
    if i==98 and bd[j+W]=='K':ms.append((j+W,j+E,''))
    j+=d
 return ms
def val(bd,i,j,pr,ep):
 p,q=bd[i],bd[j]
 s=PT[p][j]-PT[p][i]
 if q in 'pnbrqk':s+=PT[q.upper()][119-j]
 if p=='P':
  if 21<=j<=28:s+=PT[pr][j]-PT['P'][j]
  if j==ep:s+=PT['P'][119-(j+S)]
 return s
def move(pos,m):
 bd,sc,ep=pos
 i,j,pr=m
 p=bd[i]
 sc+=val(bd,i,j,pr,ep)
 L=list(bd);L[j]=L[i];L[i]='.'
 ep2=0
 if p=='K' and abs(j-i)==2:
  L[91 if j<i else 98]='.';L[(i+j)//2]='R'
 if p=='P':
  if 21<=j<=28:L[j]=pr
  if j-i==2*N:ep2=i+N
  if j==ep:L[j+S]='.'
 return(''.join(L)[::-1].swapcase(),-sc,119-ep2 if ep2 else 0)
def kcap(pos):
 bd,sc,ep=pos
 for m in gen(bd,ep):
  if bd[m[1]]=='k':return m
 return None
ND=0;LIM=200000;TT={}
class Ab(Exception):pass
def qs(pos,a,bt,pl):
 global ND;ND+=1
 if ND>LIM:raise Ab
 bd,sc,ep=pos
 if sc>=bt:return bt
 if sc>a:a=sc
 ms=[m for m in gen(bd,ep) if bd[m[1]]in 'pnbrqk' or m[2]]
 ms.sort(key=lambda m:V[bd[m[1]].upper()],reverse=True)
 for m in ms:
  np=move(pos,m)
  if kcap(np):continue
  s=-qs(np,-bt,-a,pl+1)
  if s>=bt:return bt
  if s>a:a=s
 return a
def sr(pos,d,a,bt,pl):
 global ND;ND+=1
 if ND>LIM:raise Ab
 if d<=0:return qs(pos,a,bt,pl)
 bd,sc,ep=pos
 ms=gen(bd,ep)
 ms.sort(key=lambda m:10**6+V[bd[m[1]].upper()]if bd[m[1]]in 'pnbrqk' else 0,reverse=True)
 b0=TT.get(bd)
 if b0 and b0 in ms:ms.remove(b0);ms.insert(0,b0)
 best=-I;bm=None
 for m in ms:
  np=move(pos,m)
  if kcap(np):continue
  s=-sr(np,d-1,-bt,-a,pl+1)
  if s>best:best=s;bm=m
  if s>a:
   a=s
   if a>=bt:break
 if bm:TT[bd]=bm
 return best if bm else -M+pl
def pf(f):
 a=f.split();L=list((' '*9+'\n')*2+(' '+'........\n')*8+(' '*9+'\n')*2)
 for ri,row in enumerate(a[0].split('/')):
  r=7-ri;f0=0
  for c in row:
   if c.isdigit():f0+=int(c)
   else:L[(9-r)*10+f0+1]=c;f0+=1
 sc=sum(PT[p][i]if p in'PNBRQK'else-PT[p.upper()][119-i]for i,p in enumerate(L)if p in'PNBRQKpnbrqk')
 ep=0
 if a[3]!='-':ep=(10-int(a[3][1]))*10+ord(a[3][0])-96
 if a[1]=='b':
  L=list(''.join(L)[::-1].swapcase());sc=-sc;ep=119-ep if ep else 0
 return(''.join(L),sc,ep)
def nm(s):
 return chr(96+s%10)+str(10-s//10)
def mu(m):
 i,j,pr=m
 return nm(i)+nm(j)+(pr.lower()if pr else'')
def ch(f,g):
 global ND
 bd,sc,ep=pf(f)
 ls=set(g);ms=[]
 for m in gen(bd,ep):
  u=mu(m)
  if u in ls:ms.append((m,u))
 if not ms:return g[0]
 bm,bu=ms[0];ND=0
 try:
  for d in range(1,64):
   cb,cbu=bm,bu;al=-I
   for m,u in ms:
    np=move((bd,sc,ep),m)
    if kcap(np):continue
    s=-sr(np,d-1,-I,I,1)
    if s>al:al=s;cb,cbu=m,u
   bm,bu=cb,cbu
   if ND>LIM:break
 except Ab:pass
 return bu
def post(p,bd):
 q=w.Request(U+p,data=json.dumps(bd).encode(),headers={'content-type':'application/json'})
 return json.load(w.urlopen(q))
while True:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  g=post('/move',{'game':g['game'],'move':ch(g['fen'],g['legal_moves'])})
