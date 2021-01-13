import math
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def local_qft():
    reg_size = 6
    q = QuantumRegister(reg_size)

    # TODO: Is ClassicalRegister overhead negligable?
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    b4 = ClassicalRegister(1)
    b5 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3, b4, b5)

    # qc = QuantumCircuit(q)

    # TODO: Cleaner input through bitstring?
    # zero_state = [1, 0]
    # qc.initialize(zero_state, 2)
    # qc.initialize(zero_state, 3)

    one_state = [0, 1]
    qc.initialize(one_state, 0)
    qc.initialize(one_state, 1)
    qc.initialize(one_state, 4)
    qc.initialize(one_state, 5)
    qc.initialize(one_state, 2)
    qc.initialize(one_state, 3)

    # Can loop this such that
    # foreach psi 1->n:
    #   H , R2(q[psi+1])->R(n-psi)(n)
    # where R(n)(i) = crz(2 * math.pi / pow(2, 2), q[i] ...)

    for i in range(0, reg_size):
        qc.h(q[i])
        for j in range(reg_size - i-1):
            qc.crz(2 * math.pi / pow(2, 2+j), q[i+j+1], q[i])

    # TODO: full reversal
    # TODO: measure

    # print(qc)
    return qc
