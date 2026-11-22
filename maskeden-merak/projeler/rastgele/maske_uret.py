import sys, numpy as np
from scipy import ndimage
from PIL import Image
tohum=int(sys.argv[1]); out=sys.argv[2]
rng=np.random.default_rng(tohum)
H,W=1500,2400
def fbm():
    t=np.zeros((H,W))
    for o,a in [(256,1),(128,.5),(64,.28),(32,.15),(16,.08),(8,.04)]:
        g=rng.standard_normal((H//o+3,W//o+3))
        t+=a*ndimage.zoom(g,o,order=3)[:H,:W]
    return t/t.std()
yy,xx=np.mgrid[0:H,0:W]/np.array([H,W])[:,None,None] if False else np.mgrid[0:H,0:W]
# 2-3 kıta çekirdeği (uzunlamasına elips)
taban=np.zeros((H,W))
for k in range(rng.integers(2,4)):
    cx,cy=rng.uniform(.2,.8)*W,rng.uniform(.3,.7)*H
    a,b=rng.uniform(350,650),rng.uniform(200,380); t=rng.uniform(0,np.pi)
    dx,dy=xx-cx,yy-cy; u=(dx*np.cos(t)+dy*np.sin(t))/a; v=(-dx*np.sin(t)+dy*np.cos(t))/b
    taban=np.maximum(taban,np.exp(-(u*u+v*v)))
kenar=np.minimum.reduce([xx,W-1-xx,yy,H-1-yy])
f=taban*1.6+fbm()*0.45-np.exp(-kenar/60)*2
esik=np.quantile(f,0.66)
m=f>esik
L,n=ndimage.label(m); s=ndimage.sum(m,L,range(1,n+1)); m=np.isin(L,np.nonzero(s>=40)[0]+1)
L,n=ndimage.label(~m); s=ndimage.sum(~m,L,range(1,n+1)); m=~np.isin(L,np.nonzero(s>=200)[0]+1)
Image.fromarray((m*255).astype(np.uint8)).save(out)
L,n=ndimage.label(m); s=ndimage.sum(m,L,range(1,n+1))
print("kara payı",round(m.mean(),3),"bileşen",n,"en büyükler",sorted(s.astype(int))[::-1][:6])
