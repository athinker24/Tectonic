import numpy as np, sys, json, warnings
warnings.filterwarnings("ignore")
D=sys.argv[1]
regions={"Alpler":(45,7),"Himalaya_Nepal":(27,84),"Appalachian":(35,-84),"Skandinav_Dagları":(60,6),"Zagros":(30,50),"Orta_And":(-19,-70)}
def name(lat,lon):
    return f"{'N' if lat>=0 else 'S'}{abs(lat):02d}{'E' if lon>=0 else 'W'}{abs(lon):03d}"
scales={"5 km":162,"10 km":324,"20 km":648}  # 1 arcsec px; 162 px = 0.045 deg
out={}
for r,(la,lo) in regions.items():
    rows=[]
    for i in range(2,-1,-1):  # north first
        rows.append(np.concatenate([np.load(f"{D}/{name(la+i,lo+j)}.npy")[:-1,:-1] for j in range(3)],axis=1))
    Z=np.concatenate(rows,axis=0)  # 10800x10800
    latc=la+1.5
    res={"valid_frac":float(np.isfinite(Z).mean()),"mean_elev_m":float(np.nanmean(Z)),"max_elev_m":float(np.nanmax(Z)),"min_elev_m":float(np.nanmin(Z))}
    # fine-scale slope (30 m) median, 10th/90th
    dzdy,dzdx=np.gradient(Z[::4,::4],120*1.0,120*np.cos(np.radians(latc)))  # 120 m nominal px
    sl=np.degrees(np.arctan(np.hypot(dzdx,dzdy))); res["slope30m_median_deg"]=float(np.nanmedian(sl)); res["slope30m_p90_deg"]=float(np.nanpercentile(sl,90))
    for sname,b in scales.items():
        n=Z.shape[0]//b
        Zb=Z[:n*b,:n*b].reshape(n,b,n,b)
        valid=np.isfinite(Zb).mean(axis=(1,3))
        mx=np.nanmax(Zb,axis=(1,3)); mn=np.nanmin(Zb,axis=(1,3)); mean=np.nanmean(Zb,axis=(1,3))
        ok=valid>0.9
        relief=(mx-mn)[ok]
        # coarse slope
        dy=b/3600*110.57e3; dx=b/3600*111.32e3*np.cos(np.radians(latc))
        m2=np.where(ok,mean,np.nan)
        gy,gx=np.gradient(m2,dy,dx); cs=np.degrees(np.arctan(np.hypot(gx,gy)))
        res[sname]={"cells":int(ok.sum()),"mean_relief_m":float(np.nanmean(relief)),"median_relief_m":float(np.nanmedian(relief)),"p90_relief_m":float(np.nanpercentile(relief,90)),
                    "mean_elev_m":float(np.nanmean(mean[ok])),"cell_slope_median_deg":float(np.nanmedian(cs)),"cell_slope_p90_deg":float(np.nanpercentile(cs,90)),
                    "cell_dx_km":float(dx/1e3)}
    out[r]=res
    print(r,"done",flush=True)
json.dump(out,open(sys.argv[2],"w"),indent=1,ensure_ascii=False)
