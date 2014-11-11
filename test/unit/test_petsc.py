# This file is part of PyOP2
#
# PyOP2 is Copyright (c) 2012, Imperial College London and
# others. Please see the AUTHORS file in the main source directory for
# a full list of copyright holders.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The name of Imperial College London or that of other
#       contributors may not be used to endorse or promote products
#       derived from this software without specific prior written
#       permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTERS
# ''AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

"""
PETSc specific unit tests
"""

import pytest
import numpy as np

from pyop2 import op2

# If mpi4py or petsc4py are not available this test module is skipped
mpi4py = pytest.importorskip("mpi4py")
petsc4py = pytest.importorskip("petsc4py")


class TestPETSc:

    def test_set_petsc_mpi_comm(self, backend):
        "PETSc MPI communicator should be converted to mpi4py communicator."
        op2.MPI.comm = petsc4py.PETSc.Sys.getDefaultComm()
        assert isinstance(op2.MPI.comm, mpi4py.MPI.Comm)

    @pytest.mark.xfail
    def test_vec_norm_changes(self, backend, skip_cuda, skip_opencl):
        s = op2.Set(1)
        d = op2.Dat(s)

        d.data[:] = 1

        with d.vec_ro as v:
            assert np.allclose(v.norm(), 1.0)

        d.data[:] = 2

        with d.vec_ro as v:
            assert np.allclose(v.norm(), 2.0)
