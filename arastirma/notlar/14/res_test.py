import numpy as np, sys
import fastscapelib as fs
def run(L, dx, m, n, K, U0, T, dt, D=0.0, seed=0):
    N=int(round(L/dx))
    grid=fs.RasterGrid([N,N],[dx,dx],fs.NodeStatus.FIXED_VALUE)
    fg=fs.FlowGraph(grid,[fs.SingleFlowRouter(),fs.MSTSinkResolver()])
    spl=fs.SPLEroder(fg,K,m,n,1e-6)
    dif=fs.DiffusionADIEroder(grid,D) if D>0 else None
    rng=np.random.default_rng(seed)
    z=rng.random((N,N))
    U=np.full((N,N),U0); U[0,:]=U[-1,:]=U[:,0]=U[:,-1]=0
    for i in range(int(T/dt)):
        z+=U*dt
        fg.update_routes(z)
        area=fg.accumulate(grid.nodes_areas())
        z-=spl.erode(z,area,dt)
        if dif is not None: z-=dif.erode(z,dt)
    return z
L=400e3; U0=1e-3; T=4e7; dt=1e5
for (m,n,K) in [(0.5,1,1e-7),(0.4,1,1e-7),(0.5,1.5,1e-7),(0.45,1,1e-7)]:
    print("m,n,K=",m,n,K)
    for dx in [20e3,10e3,5e3,2.5e3]:
        z=run(L,dx,m,n,K,U0,T,dt)
        print(f"  dx={dx/1e3:5.1f} km N={z.shape[0]:3d} mean z={z.mean():8.1f} m  max z={z.max():8.1f} m")
