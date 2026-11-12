import gzip, io, os, sys, urllib.request, numpy as np
D=sys.argv[1]
regions={ # name: (lat0, lon0) lower-left of a 3x3-degree block
 "Alpler":(45,7),"Himalaya_Nepal":(27,84),"Appalachian":(35,-84),"Skandinav_Dagları":(60,6),"Zagros":(30,50),"Orta_And":(-19,-70)}
def name(lat,lon):
    return f"{'N' if lat>=0 else 'S'}{abs(lat):02d}{'E' if lon>=0 else 'W'}{abs(lon):03d}"
for r,(la,lo) in regions.items():
    for i in range(3):
        for j in range(3):
            n=name(la+i,lo+j); out=f"{D}/{n}.npy"
            if os.path.exists(out): continue
            url=f"https://s3.amazonaws.com/elevation-tiles-prod/skadi/{n[:3]}/{n}.hgt.gz"
            try:
                raw=gzip.decompress(urllib.request.urlopen(url,timeout=60).read())
                a=np.frombuffer(raw,dtype='>i2').reshape(3601,3601).astype('float32')
                a[a==-32768]=np.nan
                np.save(out,a)
            except Exception as e:
                print("FAIL",n,e)
print("done")
