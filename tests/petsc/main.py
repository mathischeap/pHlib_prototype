# -*- coding: utf-8 -*-

# python tests/petsc/main.py


from petsc4py import PETSc

from src.config import COMM, SIZE, RANK, MASTER_RANK

PETSc_COMM = PETSc.COMM_WORLD

print(PETSc_COMM.size)

v = PETSc.Vec().create(comm=PETSc_COMM)
# v.setSizes(100, 50)
# v.setType('mpi')

# print(v)


if __name__ == '__main__':
    pass
