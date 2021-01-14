import os
import math
from getpass import getpass
from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import execute

from quantuminspire.src.quantuminspire.qiskit import QI
import matplotlib.pyplot as plt

from quantuminspire.src.project_src.gates import *

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
    #define (qu)bits
    q = QuantumRegister(8)
    b = [ClassicalRegister(1) for i in range(8)]
    qc = QuantumCircuit(q)
    for register in b:
        qc.add_register(register)

    #construct circuit using local and nonlocal gates
    #gates on first qubit
    qc.h(q[0])
    qc.crz(2 * math.pi / pow(2, 2), q[1], q[0])
    qc.crz(2 * math.pi / pow(2, 3), q[2], q[0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [5, 4, 3, 0], [5, 4, 3, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [6, 4, 3, 0], [6, 4, 3, 0])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 6)), [7, 4, 3, 0], [7, 4, 3, 0])

    #gates on second qubit
    qc.h(q[1])
    qc.crz(2 * math.pi / pow(2, 2), q[2], q[1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [5, 4, 3, 1], [5, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [6, 4, 3, 1], [6, 4, 3, 1])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 5)), [7, 4, 3, 1], [7, 4, 3, 1])
    #gates on third qubit
    qc.h(q[2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 2)), [5, 4, 3, 2], [5, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 3)), [6, 4, 3, 2], [6, 4, 3, 2])
    qc = qc.compose(nonlocal_rk(2 * math.pi / pow(2, 4)), [7, 4, 3, 2], [7, 4, 3, 2])
    #gates on fourth qubit
    qc.h(q[5])
    qc.crz(2 * math.pi / pow(2, 2), q[6], q[5])
    qc.crz(2 * math.pi / pow(2, 3), q[7], q[5])
    #gates on fifth qubit
    qc.h(q[6])
    qc.crz(2 * math.pi / pow(2, 2), q[7], q[6])
    #gates on sixth qubit
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


if __name__ == '__main__':
    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

    # TRY ENTANGLER AND DISENTANGLER
    # q = QuantumRegister(5)
    #
    # b0 = ClassicalRegister(1)
    # b1 = ClassicalRegister(1)
    # b2 = ClassicalRegister(1)
    # b3 = ClassicalRegister(1)
    # b4 = ClassicalRegister(1)
    #
    # circuit = QuantumCircuit(q, b0, b1, b2, b3, b4)
    #
    # initial_state = [1/sqrt(3), sqrt(2)/sqrt(3)]
    # entangled_circuit = entangler(initial_state, circuit)
    # disentangled = disentangler(entangled_circuit)
    # q2 = disentangled.qubits
    # b = disentangled.clbits
    # circuit.measure(q2[0], b[0])
    # circuit.measure(q2[1], b[1])
    # circuit.measure(q2[2], b[2])
    # circuit.measure(q2[3], b[3])
    # circuit.measure(q2[4], b[4])

    # TRY TELEPORT
    # state = [1/sqrt(2), 1/sqrt(2)]
    # circuit = teleport(state)
    # q = circuit.qubits
    # b = circuit.clbits
    # circuit.measure(q[0], b[0])
    # circuit.measure(q[1], b[1])
    # circuit.measure(q[2], b[2])
    # circuit.measure(q[3], b[3])

    # TRY CNOT
    # control = [1/sqrt(2), 1/sqrt(2)]
    # target = [1, 0]
    # circuit = nonlocal_cnot(control, target)
    # q = circuit.qubits
    # b = circuit.clbits
    # circuit.measure(q[0], b[0])
    # circuit.measure(q[1], b[1])
    # circuit.measure(q[2], b[2])
    # circuit.measure(q[3], b[3])

    # circuit = qft()
    #
    # control = [0, 1]
    # target = [0, 1]
    # circuit = nonlocal_rk(control, target, 2 * math.pi / pow(2, 3))
    # q = circuit.qubits
    # b = circuit.clbits
    # circuit.measure(q[0], b[0])
    # circuit.measure(q[1], b[1])
    # circuit.measure(q[2], b[2])
    # circuit.measure(q[3], b[3])
    # circuit.measure(q[4], b[4])
    # circuit.measure(q[5], b[5])

    # q = QuantumRegister(8)
    # b = [ClassicalRegister(1) for i in range(8)]
    # circuit = QuantumCircuit(q)
    # for register in b:
    #     circuit.add_register(register)
    #
    # qb1 = [1, 0]
    # qb2 = [1, 0]
    # qb3 = [1, 0]
    # qb4 = [1, 0]
    # qb5 = [1, 0]
    # qb6 = [1, 0]
    #
    # circuit.initialize(qb1, 0)
    # circuit.initialize(qb2, 1)
    # circuit.initialize(qb3, 2)
    # circuit.initialize(qb4, 5)
    # circuit.initialize(qb5, 6)
    # circuit.initialize(qb6, 7)
    #
    # circuit = circuit.compose(qft_2n_L())
    #
    # circuit.measure(q[0], b[0])
    # circuit.measure(q[1], b[1])
    # circuit.measure(q[2], b[2])
    # circuit.measure(q[3], b[3])
    # circuit.measure(q[4], b[4])
    # circuit.measure(q[5], b[5])
    # circuit.measure(q[6], b[6])
    # circuit.measure(q[7], b[7])

    # circuit.draw('mpl')
    # plt.show()

    q = QuantumRegister(9)
    b = [ClassicalRegister(1) for i in range(9)]
    circuit = QuantumCircuit(q)
    for register in b:
        circuit.add_register(register)

    qb1 = [1, 0]
    qb2 = [1, 0]
    qb3 = [1, 0]
    qb4 = [1, 0]
    qb5 = [1, 0]
    qb6 = [1, 0]

    circuit.initialize(qb1, 0)
    circuit.initialize(qb2, 1)
    circuit.initialize(qb3, 4)
    circuit.initialize(qb4, 5)
    circuit.initialize(qb5, 7)
    circuit.initialize(qb6, 8)

    circuit = circuit.compose(qft_3n())

    circuit.measure(q[0], b[0])
    circuit.measure(q[1], b[1])
    circuit.measure(q[2], b[2])
    circuit.measure(q[3], b[3])
    circuit.measure(q[4], b[4])
    circuit.measure(q[5], b[5])
    circuit.measure(q[6], b[6])
    circuit.measure(q[7], b[7])
    circuit.measure(q[8], b[8])


    qi_job = execute(circuit, backend=qi_backend, shots=256)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(circuit)
    print('\nState\tCounts')
    [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    # Print the full state probabilities histogram
    probabilities_histogram = qi_result.get_probabilities(circuit)
    print('\nState\tProbabilities')
    [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]
