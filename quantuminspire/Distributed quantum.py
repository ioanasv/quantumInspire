import os
import math
from getpass import getpass
from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import execute

from quantuminspire.src.quantuminspire.qiskit import QI
import matplotlib.pyplot as plt

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')

def get_authentication():
    """ Gets the authentication for connecting to the Quantum Inspire API."""
    token = load_account()
    if token is not None:
        return get_token_authentication(token)
    else:
        if QI_EMAIL is None or QI_PASSWORD is None:
            print('Enter email:')
            email = input()
            print('Enter password')
            password = getpass()
        else:
            email, password = QI_EMAIL, QI_PASSWORD
        return get_basic_authentication(email, password)


# def entangler(initial_state, circuit):
#     circuit.initialize(initial_state, 0)
#     zero_state = [1, 0]
#     circuit.initialize(zero_state, 1)
#     circuit.initialize(zero_state, 2)
#     circuit.initialize(zero_state, 3)
#     circuit.initialize(zero_state, 4)
#
#     circuit.h(q[1])
#     circuit.cx(q[1], q[2])
#     circuit.cx(q[2], q[3])
#     circuit.cx(q[3], q[4])
#     circuit.cx(q[0], q[1])
#
#     circuit.measure(1, b1)
#
#     circuit.x(q[1]).c_if(b1, 1)
#     circuit.x(q[2]).c_if(b1, 1)
#     circuit.x(q[3]).c_if(b1, 1)
#     circuit.x(q[4]).c_if(b1, 1)
#     return circuit
#
#
# def disentangler(circuit):
#     circuit.h(q[2])
#     circuit.h(q[3])
#     circuit.h(q[4])
#
#     circuit.measure(q[2], b2)
#     circuit.measure(q[3], b3)
#     circuit.measure(q[4], b4)
#
#     circuit.z(q[0]).c_if(b2, 1)
#     circuit.z(q[0]).c_if(b3, 1)
#     circuit.z(q[0]).c_if(b4, 1)
#
#     circuit.x(q[2]).c_if(b2, 1)
#     circuit.x(q[3]).c_if(b3, 1)
#     circuit.x(q[4]).c_if(b4, 1)
#     return circuit
#
#
# def teleport(state):
#     q = QuantumRegister(4)
#     b0 = ClassicalRegister(1)
#     b1 = ClassicalRegister(1)
#     b2 = ClassicalRegister(1)
#     b3 = ClassicalRegister(1)
#     qc = QuantumCircuit(q, b0, b1, b2, b3)
#     qc.initialize(state, 0)
#     zero_state = [1, 0]
#     qc.initialize(zero_state, 1)
#     qc.initialize(zero_state, 2)
#     qc.initialize(zero_state, 3)
#
#     qc.h(q[1])
#     qc.cx(q[1], q[2])
#     qc.cx(q[0], q[1])
#     qc.measure(q[1], b1)
#     qc.x(q[1]).c_if(b1, 1)
#     qc.x(q[2]).c_if(b1, 1)
#     qc.h(q[0])
#     qc.measure(q[0], b0)
#     qc.x(q[0]).c_if(b0, 1)
#     qc.x(q[2]).c_if(b0, 1)
#     qc.swap(q[2], q[3])
#     return qc


def qft():
    q = QuantumRegister(6)
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    b4 = ClassicalRegister(1)
    b5 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3, b4, b5)

    zero_state = [1, 0]
    qc.initialize(zero_state, 2)
    qc.initialize(zero_state, 3)

    one_state = [0, 1]
    qc.initialize(one_state, 0)
    qc.initialize(one_state, 1)
    qc.initialize(one_state, 4)
    qc.initialize(one_state, 5)

    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])

    qc.h(q[2])
    qc.cx(q[2], q[3])

    qc.cx(q[4], q[3])
    qc.measure(q[3], b3)
    qc.x(q[2]).c_if(b3, 1)
    qc.x(q[3]).c_if(b3, 1)

    qc.crz(2 * math.pi / pow(2, 3), q[2], q[0])
    qc.h(q[2])
    qc.measure(q[2], b2)

    qc.x(q[2]).c_if(b2, 1)
    qc.z(q[4]).c_if(b2, 1)

    qc.h(q[2])
    qc.cx(q[2], q[3])

    qc.cnot(q[5], q[3])
    qc.measure(q[3], b3)

    qc.x(q[2]).c_if(b3, 1)
    qc.x(q[3]).c_if(b3, 1)

    qc.crz(2 * math.pi / pow(2, 4), q[2], q[0])
    qc.h(q[2])
    qc.measure(q[2], b2)

    qc.x(q[2]).c_if(b2, 1)
    qc.z(q[5]).c_if(b2, 1)

    qc.h(q[2])
    qc.cx(q[2], q[3])

    qc.cx(q[4], q[3])
    qc.measure(q[3], b3)

    qc.x(q[2]).c_if(b3, 1)
    qc.x(q[3]).c_if(b3, 1)

    qc.h(q[1])
    qc.crz(2 * math.pi / pow(2, 2), q[2], q[1])

    qc.h(q[2])
    qc.measure(q[2], b2)

    qc.x(q[2]).c_if(b2, 1)
    qc.z(q[4]).c_if(b2, 1)

    qc.h(q[2])
    qc.cx(q[2], q[3])

    qc.cx(q[5], q[3])
    qc.measure(q[3], b3)
    qc.x(q[2]).c_if(b3, 1)
    qc.x(q[3]).c_if(b3, 1)

    qc.crz(2 * math.pi / pow(2, 3), q[2], q[1])
    qc.h(q[2])
    qc.measure(q[2], b2)

    qc.x(q[2]).c_if(b2, 1)
    qc.z(q[4]).c_if(b2, 1)
    qc.h(q[4])
    qc.crz(2 * math.pi / pow(2, 2), q[5], q[4])
    qc.h(q[5])

    return qc
def qft2():
    #define (qu)bits
    q = QuantumRegister(6)
    b = [ClassicalRegister(1) for i in range(6)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    #construct circuit using local and nonlocal gates
    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [4, 3, 2, 0], [4, 3, 2, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [5, 3, 2, 0], [5, 3, 2, 0])
    qc.h(q[1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [4, 3, 2, 1], [4, 3, 2, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [5, 3, 2, 1], [5, 3, 2, 1])
    qc.h(q[4])
    qc.crz(2 * math.pi / pow(2, 2), q[4], q[5])
    qc.h(q[5])
    return qc

def qft_6n():
    n_q = 12
    q = QuantumRegister(n_q)
    b = [ClassicalRegister(1) for i in range(n_q)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    qc.h(q[0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [2, 3, 1, 0], [2, 3, 1, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [4, 5, 1, 0], [4, 5, 1, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [6, 7, 1, 0], [6, 7, 1, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [8, 9, 1, 0], [8, 9, 1, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 6)), [10, 11, 1, 0], [10, 11, 1, 0])

    qc.h(q[2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [4, 5, 3, 2], [4, 5, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [6, 7, 3, 2], [6, 7, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [8, 9, 3, 2], [8, 9, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [10, 11, 3, 2], [10, 11, 3, 2])

    qc.h(q[4])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [6, 7, 5, 4], [6, 7, 5, 4])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [8, 9, 5, 4], [8, 9, 5, 4])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [10, 11, 5, 4], [10, 11, 5, 4])

    qc.h(q[6])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [8, 9, 7, 6], [8, 9, 7, 6])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [10, 11, 7, 6], [10, 11, 7, 6])

    qc.h(q[8])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [10, 11, 9, 8], [10, 11, 9, 8])

    qc.h(q[10])

    return qc

def nonlocal_rk(theta):
    q = QuantumRegister(4)
    c0 = ClassicalRegister(1)
    c1 = ClassicalRegister(1)
    c2 = ClassicalRegister(1)
    c3 = ClassicalRegister(1)
    qc = QuantumCircuit(q, c0, c1, c2, c3)
    # qc.initialize(control, 0)
    # qc.initialize(target, 3)
    # zero_state = [1, 0]
    # qc.initialize(zero_state, 1)
    # qc.initialize(zero_state, 2)

    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.measure(q[1], c1)
    qc.barrier(q[1], q[2])

    qc.x(q[1]).c_if(c1, 1)
    qc.x(q[2]).c_if(c1, 1)
    qc.crz(theta, q[2], q[3])
    qc.h(q[2])
    qc.measure(q[2], c2)
    qc.barrier(q[0], q[2])

    qc.z(q[0]).c_if(c2, 1)
    qc.x(q[2]).c_if(c2, 1)

    return qc


def nonlocal_cnot():
    q = QuantumRegister(4)
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3)

    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.measure(q[1], b1)
    qc.x(q[1]).c_if(b1, 1)
    qc.x(q[2]).c_if(b1, 1)
    qc.cx(q[2], q[3])
    qc.h(q[2])
    qc.measure(q[2], b2)
    qc.z(q[0]).c_if(b2, 1)
    qc.x(q[2]).c_if(b2, 1)

    return qc


if __name__ == '__main__':
    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

    # define (qu)bits
    q = QuantumRegister(12)
    b = [ClassicalRegister(1) for i in range(12)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    # qb1 = [1, 0];
    # qb2 = [1, 0];
    # qb3 = [1, 0];
    # qb4 = [1, 0];
    #
    # qc.initialize(qb1, 0)
    # qc.initialize(qb2, 1)
    # qc.initialize(qb3, 4)
    # qc.initialize(qb4, 5)

    for i in range(12):
        qc.initialize([1,0], i)

    # qc = qc.compose(qft2())
    qc = qc.compose(qft_6n())

    for i in range(12):
        qc.measure(q[i], b[i])


    qc.draw('mpl')
    plt.show()


    qi_job = execute(qc, backend=qi_backend, shots=256)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(qc)
    print('\nState\tCounts')
    [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    # Print the full state probabilities histogram
    probabilities_histogram = qi_result.get_probabilities(qc)
    print('\nState\tProbabilities')
    [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]