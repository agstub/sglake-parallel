import numpy as np
from dolfin import *
from params import *
from mpi4py import MPI
from plotting import plot_fields
from mesh_fcns import get_fields
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

for i in range(nt):
    hdf5 = HDF5File(MPI.COMM_WORLD, "./results/h5files/sol"+str(i)+".h5", "r")
    mesh = Mesh()
    hdf5.read(mesh, "mesh",False)

    P1 = FiniteElement('P',mesh.ufl_cell(),1)     # pressure
    P2 = FiniteElement('P',mesh.ufl_cell(),2)     # velocity
    R  = FiniteElement("R", mesh.ufl_cell(),0)    # mean water pressure
    element = MixedElement([[P2,P2,P2],P1,R])
    W = FunctionSpace(mesh,element)
    w = Function(W)
    hdf5.read(w, "solution")

    h,s,wb,xh,yh,xs,ys = get_fields(w,mesh)

    h = comm.gather(h,root=0)
    s = comm.gather(s,root=0)
    wb = comm.gather(wb,root=0)

    xh = comm.gather(xh,root=0)
    yh = comm.gather(yh,root=0)
    xs = comm.gather(xs,root=0)
    ys = comm.gather(ys,root=0)

    if rank ==0:
        h = np.concatenate(h).ravel()
        s = np.concatenate(s).ravel()
        wb = np.concatenate(wb).ravel()

        xh = np.concatenate(xh).ravel()
        yh = np.concatenate(yh).ravel()
        xs = np.concatenate(xs).ravel()
        ys = np.concatenate(ys).ravel()


        plot_fields(h,s,wb,xh,yh,xs,ys,i)
        sys.stdout.flush()
