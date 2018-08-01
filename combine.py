# ******************** creating stage and mesh***************************
from pxr import Usd, UsdGeom, Gf, Sdf, Vt

stage = Usd.Stage.CreateNew('combine.usda')

xform = UsdGeom.Xform.Define(stage, '/xform')
mesh_geom = UsdGeom.Mesh.Define(stage, '/xform/mesh')


# ******************* connect path/ open exodus file********************** 
import sys

sys.path.append("/opt/moose/seacas/lib") #create connection for search path 
import exodus

exo = exodus.exodus('/Users/headjm/projects/moose/test/tests/kernels/'+
                    'simple_diffusion/simple_diffusion_out.e',"r")
# ******************* gather point info and store into variable************8
coordx = exo.get_coords()[0][:]
coordy = exo.get_coords()[1][:]
coordz = exo.get_coords()[2][:]

xyz=zip(coordx,coordy,coordz)
mesh_geom.CreatePointsAttr(xyz)
num_elems = exo.num_elems()

connectivity = []

elem_blk_ids = exo.get_elem_blk_ids()
for i in elem_blk_ids: 
    elem_conn= exo.get_elem_connectivity(i)
    connect = elem_conn[0]
    group = elem_conn[2]

    for i in range(0,len(connect)):
        connectivity.append(connect[i] - 1) 
#    Vertexmap = connect[i]
#    print 


mesh_geom.CreateFaceVertexIndicesAttr(connectivity)

vertex_counts = [4 for i in xrange(0, num_elems)]                                    

mesh_geom.CreateFaceVertexCountsAttr(vertex_counts)

mesh_geom.CreateDisplayColorAttr([(0,3,1)])

stage.GetRootLayer().Save()
exo.close() # close file 
