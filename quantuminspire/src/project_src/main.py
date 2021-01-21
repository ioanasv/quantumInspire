import os
import math
import random
import numpy as np
# from getpass import getpass
# from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit import execute

# from quantuminspire.src.quantuminspire.qiskit import QI
from qfts import *
import matplotlib.pyplot as plt

from qiskit.quantum_info import state_fidelity
from qiskit.providers.aer.extensions.snapshot_statevector import *
from qiskit.providers.aer.noise import depolarizing_error
from qiskit.providers.aer.noise import NoiseModel
from qiskit import IBMQ, Aer
from qiskit.visualization import plot_bloch_multivector

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

def create_error(qubits, intensity):
    # make an empty noise model
    noise_model = NoiseModel()

    # Add depolarizing error to all single qubits
    error = depolarizing_error(intensity, 1)
    for i in range(qubits):
        noise_model.add_quantum_error(error, ['h', 'x', 'measure'], [i])

    # Add depolareizing error for double gates
    error = depolarizing_error(intensity, 2)
    for i in range(qubits):
        for j in range(i):
            if j != i:
                noise_model.add_quantum_error(error, ['cx', 'crz'], [i, j])
    # # Print noise model info
    # print(noise_model)
    return noise_model

def Fidelity_calc(qubits, intensity, n_nodes):
    """
        calculate the fidelity between output of circuit with and without error
        :param n_nodes: amount of nodes, must be an integer and 1 or higher
        :param qubits: total amount of qubits (input qubits plus 1 communication qubit per node)
        :return: F: fidelity
        """

    input_qubits = qubits - n_nodes
    node_qubits = int(qubits / n_nodes)

    #define single qubit inputstates
    state1 = [1, 0]
    state2 = [math.sqrt(1/2), math.sqrt(1/2)]
    state3 = [math.sqrt(1/2), - math.sqrt(1/2)]
    state4 = [math.sqrt(1/2), 1j * math.sqrt(1/2)]
    state5 = [math.sqrt(1/2), -1j * math.sqrt(1/2)]
    state6 = [0, 1]

    states = [state1, state2, state3, state4, state5, state6]

    #make a qft circuit
    q = QuantumRegister(qubits)
    b = [ClassicalRegister(1) for i in range(qubits)]
    circuit = QuantumCircuit(q)
    for register in b:
        circuit.add_register(register)

    # make a teststate of control qubits
    teststate = []
    for i in range(input_qubits):
        teststate.append(states[3])

    #initialize control qubits
    for i in range(n_nodes):
        for j in range(node_qubits-1):
            circuit.initialize(teststate[(i * (node_qubits-1) + j)], (i * node_qubits + j))

    circuit = circuit.compose(qft_arbitraryn(n_nodes, node_qubits))
    circuit.snapshot_statevector('snapshot')

    circuit.draw('mpl')
    plt.show()

    print("\nResult from the local Qiskit simulator backend:\n")
    backend = Aer.get_backend("qasm_simulator")
    result1 = execute(circuit, backend=backend, shots=1000).result()

    baselinestate = result1.data()['snapshots']['statevector']['snapshot'][0]

    error_model = create_error(qubits, intensity)
    result2 = execute(circuit, backend=backend, shots=1000, noise_model=error_model).result()
    errorstate = result2.data()['snapshots']['statevector']['snapshot'][0]

    F = state_fidelity(baselinestate, errorstate)
    print(F)
    return F

def fidelity_calc2():
    n_nodes = 2
    node_qubits = 4
    # define single qubit inputstates
    state1 = [1, 0]
    state2 = [math.sqrt(1 / 2), math.sqrt(1 / 2)]
    state3 = [math.sqrt(1 / 2), - math.sqrt(1 / 2)]
    state4 = [math.sqrt(1 / 2), 1j * math.sqrt(1 / 2)]
    state5 = [math.sqrt(1 / 2), -1j * math.sqrt(1 / 2)]
    state6 = [0, 1]
    states = [state1, state2, state3, state4, state5, state6]

    #for all possible inputstates
    F = []

    for j in range(100):
        teststate = []
        for i in range(6):
            teststate.append(states[random.randint(0,5)])
        print(teststate)
        # make a qft circuit
        q = QuantumRegister(8)
        b = [ClassicalRegister(1) for i in range(8)]
        circuit1 = QuantumCircuit(q)
        circuit2 = QuantumCircuit(q)
        for register in b:
            circuit1.add_register(register)
            circuit2.add_register(register)


        # initialize control qubits
        for i in range(n_nodes):
            for j in range(node_qubits - 1):
                circuit1.initialize(teststate[(i * (node_qubits - 1) + j)], (i * node_qubits + j))
                circuit2.initialize(teststate[(i * (node_qubits - 1) + j)], (i * node_qubits + j))

        circuit1 = circuit1.compose(qft_2n())
        circuit2 = circuit2.compose(qft_2n_error(1))

        circuit1.snapshot_statevector('snapshot')
        circuit2.snapshot_statevector('snapshot')

        backend = Aer.get_backend("qasm_simulator")
        result = execute(circuit1, backend=backend, shots=1000).result()
        state1 = result.data()['snapshots']['statevector']['snapshot'][0]

        result = execute(circuit2, backend=backend, shots=1000).result()
        state2 = result.data()['snapshots']['statevector']['snapshot'][0]

        F.append(state_fidelity(state2, state1))

#                         print(a1)
    # # plot_bloch_multivector()
    # # plt.show()
    # # print(state1)
    # # print(state2)
    # # circuit.draw('mpl')
    # # plt.show()
    #
    print(F)
    A = np.avarage(F)
    print(A)
    return F

if __name__ == '__main__':
    # #fidelity for circuit with 6 input qubits and 2 nodes
    # F = Fidelity_calc(8, 0.005, 2)
    #
    # # fidelity for circuit with 6 input qubits and 3 nodes
    # F = Fidelity_calc(9, 0.005, 3)

    # fidelity_calc2()
    q = QuantumRegister(8)
    b = [ClassicalRegister(1) for i in range(8)]
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
    circuit.initialize(qb3, 2)
    circuit.initialize(qb4, 5)
    circuit.initialize(qb5, 6)
    circuit.initialize(qb6, 7)

    circuit = circuit.compose(qft_arbitraryn(2, 4, 0.1))

    circuit.measure(q[0], b[0])
    circuit.measure(q[1], b[1])
    circuit.measure(q[2], b[2])
    circuit.measure(q[3], b[3])
    circuit.measure(q[4], b[4])
    circuit.measure(q[5], b[5])
    circuit.measure(q[6], b[6])
    circuit.measure(q[7], b[7])

    circuit.draw('mpl')
    plt.show()


    # qi_job = execute(circuit, backend=qi_backend, shots=256)
    # qi_result = qi_job.result()
    # histogram = qi_result.get_counts(circuit)
    # print('\nState\tCounts')
    # [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    # # Print the full state probabilities histogram
    # probabilities_histogram = qi_result.get_probabilities(circuit)
    # print('\nState\tProbabilities')
    # [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]
