import numpy as np, sys, json, warnings
import fastscapelib as fs
warnings.filterwarnings("ignore")
D=sys.argv[1]
regions={"Alpler":(45,7),"Himalaya_Nepal":(27,84),"Appalachian":(35,-84),"Skandinav_Dagları":(60,6),"Zagros":(30,50),"Orta_And":(-19,-70)}
def name(lat,lon): return f"{'N' if lat>=0 else 'S'}{abs(lat):02d}{'E' if lon>=0 else 'W'}{abs(lon):03d}"
b=6  # 6x6 block mean -> ~185 m
res={}
for r,(la,lo) in regions.items():
    rows=[np.concatenate([np.load(f"{D}/{name(la+i,lo+j)}.npy")[:-1,:-1] for j in range(3)],axis=1) for i in range(2,-1,-1)]
    Z=np.concatenate(rows,axis=0)
    n=Z.shape[0]//b
    z=np.nanmean(Z[:n*b,:n*b].reshape(n,b,n,b),axis=(1,3)).astype('float64')
    z=np.where(np.isfinite(z),z,0.0)
    latc=la+1.5
    dy=b/3600*110.57e3; dx=b/3600*111.32e3*np.cos(np.radians(latc))
    # hypsometric integral over whole block (land+whatever >0)
    zz=z[z>0]
    hi=(zz.mean()-zz.min())/(zz.max()-zz.min())
    # flow routing on grid with spacing (dy,dx); boundaries fixed value
    grid=fs.RasterGrid([n,n],[dy,dx],fs.NodeStatus.FIXED_VALUE)
    fg=fs.FlowGraph(grid,[fs.SingleFlowRouter(),fs.MSTSinkResolver()])
    fg.update_routes(z)
    A=np.asarray(fg.accumulate(1.0))
    zc=np.asarray(fg.impl().receivers) if hasattr(fg,'impl') else None
    # use steepest-descent slope via gradient magnitude on the (sink-resolved) surface as proxy: local D8 slope
    zp=np.pad(z,1,mode='edge')
    sl=np.zeros_like(z)
    for di in (-1,0,1):
        for dj in (-1,0,1):
            if di==0 and dj==0: continue
            dist=np.hypot(di*dy,dj*dx)
            s=(z-zp[1+di:1+di+n,1+dj:1+dj+n])/dist
            sl=np.maximum(sl,s)
    ok=(A>1e6)&(sl>0)&(z>50)
    # exclude 2-pixel border
    ok[:3,:]=ok[-3:,:]=False; ok[:,:3]=ok[:,-3:]=False
    lA=np.log10(A[ok]/1e6); lS=np.log10(sl[ok])
    bins=np.linspace(0,min(lA.max(),4),13)
    xs=[];ys=[]
    for k in range(len(bins)-1):
        m=(lA>=bins[k])&(lA<bins[k+1])
        if m.sum()>200: xs.append(np.median(lA[m])); ys.append(np.median(lS[m]))
    xs=np.array(xs);ys=np.array(ys)
    sel=xs>np.log10(10)  # A>10 km2 channel part
    th=-np.polyfit(xs[sel],ys[sel],1)[0] if sel.sum()>=3 else np.nan
    # drainage density proxy: share of cells with A>1 km2 times cell... skip
    res[r]={"hi":float(hi),"theta_concavity_A_gt_10km2":float(th),"n_binned":int(sel.sum()),"max_A_km2":float(A.max()/1e6),
            "median_slope_A_1_to_3km2":float(10**np.median(lS[(lA>=0)&(lA<0.5)])) if ((lA>=0)&(lA<0.5)).any() else None,
            "median_slope_A_100_to_1000km2":float(10**np.median(lS[(lA>=2)&(lA<3)])) if ((lA>=2)&(lA<3)).any() else None}
    print(r,res[r],flush=True)
json.dump(res,open(sys.argv[2],"w"),indent=1,ensure_ascii=False)
