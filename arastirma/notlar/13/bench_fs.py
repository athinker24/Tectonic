import numpy as np, time, sys
import fastscapelib as fs
n=int(sys.argv[1]); steps=int(sys.argv[2])
shape=[n,n]
grid=fs.RasterGrid(shape,[10e3,10e3],fs.NodeStatus.FIXED_VALUE)
fg=fs.FlowGraph(grid,[fs.SingleFlowRouter(),fs.MSTSinkResolver()])
spl=fs.SPLEroder(fg,1e-5,0.4,1,1e-5)
dif=fs.DiffusionADIEroder(grid,0.01)
rng=np.random.default_rng(0)
z=rng.random(shape)*10.0
U=np.full(shape,1e-3); U[0,:]=U[-1,:]=U[:,0]=U[:,-1]=0
dt=1e5
t0=time.time()
for i in range(steps):
    z+=U*dt
    fg.update_routes(z)
    area=fg.accumulate(1.0*grid.nodes_areas())
    z-=spl.erode(z,area,dt)
    z-=dif.erode(z,dt)
el=time.time()-t0
print(f"n={n} nodes={n*n} steps={steps} total={el:.2f}s per_step={el/steps:.3f}s zmax={z.max():.0f}")
