import math
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from quantuminspire.src.project_src.gates import *


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


def qft_3n():
    q = QuantumRegister(9)
    b = [ClassicalRegister(1) for i in range(9)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    # gates on the first qubit
    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [4, 3, 2, 0], [4, 3, 2, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [5, 3, 2, 0], [5, 3, 2, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [7, 6, 2, 0], [7, 6, 2, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 6)), [8, 6, 2, 0], [8, 6, 2, 0])

    # gates on the second qubit
    qc.h(q[1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [4, 3, 2, 1], [4, 3, 2, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [5, 3, 2, 1], [5, 3, 2, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [7, 6, 2, 1], [7, 6, 2, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [8, 6, 2, 1], [8, 6, 2, 1])

    # gates on the third qubit
    qc.h(q[4])
    qc.crz(2 * math.pi / pow(2, 2), q[5], q[4])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [7, 6, 3, 4], [7, 6, 3, 4])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [8, 6, 3, 4], [8, 6, 3, 4])

    # gates on the fourth qubit
    qc.h(q[5])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [7, 6, 3, 5], [7, 6, 3, 5])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [8, 6, 3, 5], [8, 6, 3, 5])

    # gates on the fifth qubit
    qc.h(q[7])
    qc.crz(2 * math.pi / pow(2, 2), q[8], q[7])

    # gates on the eigth qubit
    qc.h(q[8])

    return qc


def qft_2n():
    # define (qu)bits
    q = QuantumRegister(8)
    b = [ClassicalRegister(1) for i in range(8)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    # construct circuit using local and nonlocal gates
    # gates on first qubit
    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])
    qc.crz(2 * math.pi / pow(2, 3), q[2], q[0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [5, 4, 3, 0], [5, 4, 3, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [6, 4, 3, 0], [6, 4, 3, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 6)), [7, 4, 3, 0], [7, 4, 3, 0])

    # gates on second qubit
    qc.h(q[1])
    qc.crz(2 * math.pi / pow(2, 2), q[2], q[1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [5, 4, 3, 1], [5, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [6, 4, 3, 1], [6, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [7, 4, 3, 1], [7, 4, 3, 1])
    # gates on third qubit
    qc.h(q[2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [5, 4, 3, 2], [5, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [6, 4, 3, 2], [6, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [7, 4, 3, 2], [7, 4, 3, 2])
    # gates on fourth qubit
    qc.h(q[5])
    qc.crz(2 * math.pi / pow(2, 2), q[6], q[5])
    qc.crz(2 * math.pi / pow(2, 3), q[7], q[5])
    # gates on fifth qubit
    qc.h(q[6])
    qc.crz(2 * math.pi / pow(2, 2), q[7], q[6])
    # gates on sixth qubit
    qc.h(q[7])
    return qc


def qft_2n_L():
    # define (qu)bits
    q = QuantumRegister(8)
    b = [ClassicalRegister(1) for i in range(8)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    # construct circuit using local and nonlocal gates
    # gates on first qubit
    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])
    qc.swap(q[0], q[1])
    qc.crz(2 * math.pi / pow(2, 3), q[2], q[1])
    qc.swap(q[1], q[2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [5, 4, 3, 2], [5, 4, 3, 2])
    qc.swap(q[5], q[6])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [5, 4, 3, 0], [5, 4, 3, 0])
    qc.swap(q[5], q[6])
    qc.swap(q[6], q[7])
    qc.swap(q[5], q[6])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 6)), [5, 4, 3, 0], [5, 4, 3, 0])
    qc.swap(q[5], q[6])
    qc.swap(q[6], q[7])

    # gates on second qubit
    qc.h(q[1])
    qc.crz(2 * math.pi / pow(2, 2), q[2], q[1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [5, 4, 3, 1], [5, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [6, 4, 3, 1], [6, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [7, 4, 3, 1], [7, 4, 3, 1])

    # gates on third qubit
    qc.h(q[2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [5, 4, 3, 2], [5, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [6, 4, 3, 2], [6, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [7, 4, 3, 2], [7, 4, 3, 2])

    # gates on fourth qubit
    qc.h(q[5])
    qc.crz(2 * math.pi / pow(2, 2), q[6], q[5])
    qc.crz(2 * math.pi / pow(2, 3), q[7], q[5])

    # gates on fifth qubit
    qc.h(q[6])
    qc.crz(2 * math.pi / pow(2, 2), q[7], q[6])

    # gates on sixth qubit
    qc.h(q[7])
    return qc