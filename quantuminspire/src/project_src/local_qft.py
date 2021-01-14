import math
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def local_qft(qubit_count=6, init_states=[1, 1, 1, 1, 1, 1]):
    q = QuantumRegister(qubit_count)

    # TODO: Is ClassicalRegister overhead negligible?
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    b4 = ClassicalRegister(1)
    b5 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3, b4, b5)

    zero_state = [1, 0]
    one_state = [0, 1]

    for i, state in enumerate(init_states):
        if state == 0:
            qc.initialize(zero_state, i)
        # for now only basis states are supported
        # TODO: add |+>, |->, |+i> & |-i>
        else:
            qc.initialize(one_state, i)

    # foreach psi 1->n:
    #   H , R2(q[psi+1])->R(n-psi)(n)
    # where R(n)(i) = crz(2 * math.pi / pow(2, 2), q[i] ...)

    for i in range(0, qubit_count):
        qc.h(q[i])
        for j in range(qubit_count - i - 1):
            qc.crz(2 * math.pi / pow(2, 2+j), q[i+j+1], q[i])

    # Bit-order reversal through swap gates
    for i in range(0, int(qubit_count / 2)):
        qc.swap(q[i], q[qubit_count - i - 1])

    # print(qc)
    return qc
