import os
import random
from scipy import rand

from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit import execute

from quantuminspire.qiskit import QI
from qfts import *
from main import *
import numpy as np
from qiskit.circuit.library import QFT
import matplotlib.pyplot as plt

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')


def qubit_probabilities(histogram):
    qubit_count = len(list(histogram.keys())[0].split())
    print(qubit_count)
    zeros = np.zeros((qubit_count, 1))
    ones = np.zeros((qubit_count, 1))
    for k, count in histogram.items():
        qubit_vals = k.split()
        # For each qubit in the result, add count to
        for i, val in enumerate(qubit_vals):
            if int(val) == 0:
                zeros[i] += count
            else:
                ones[i] += count

    # print(zeros, ones)
    means_list = [float(one) / float(zero+one) for (zero, one) in zip(zeros, ones)]
    # print(means_list)
    return means_list


def two_way_qft_arbitraryn_error(n_nodes, n_qpn, error):

    n_total = n_nodes * n_qpn

    q = QuantumRegister(n_total)
    b = [ClassicalRegister(1) for i in range(n_total)]
    circuit = QuantumCircuit(q)
    for register in b:
        circuit.add_register(register)

    # # this list is used for circuit input and for output correction
    # input = []
    # for i in range(n_total):
    #     if not (i % n_qpn) == n_qpn - 1:
    #         input.append(int(0.5 + rand()))
    #     else:
    #         input.append(0)
    #
    # zero_state = [1, 0]
    # one_state = [0, 1]
    # for i, state in enumerate(input):
    #     if state == 0:
    #         circuit.initialize(zero_state, i)
    #     else:
    #         circuit.initialize(one_state, i)

    # create qft_arbitraryn circuit with the error given as input

    circuit = circuit.compose(qft_arbitraryn(n_nodes, n_qpn, error))

    # construct and add native inverse qft
    communication_qubit_indices = [n_qpn - 1 + i*n_qpn for i in range(n_nodes)]
    computation_qubit_indices = list(range(n_total))

    for index in communication_qubit_indices:
        computation_qubit_indices.remove(index)

    # append inverse QFT to relevant (computation/input) qubits
    inverse_qft = QFT(num_qubits=n_total - n_nodes, inverse=True, do_swaps=False)
    circuit = circuit.compose(inverse_qft, qubits=computation_qubit_indices)

    # TODO: take snapshot

    # # Need to reverse order
    # result_probabilities.reverse()
    # for i, prob in enumerate(result_probabilities):
    #     print(i, " is |1> with probability ", prob)
    # right_answers = [int(a) == int(b) for (a, b) in zip(result_probabilities, input)]

    # TODO: calculate fidelity
    return circuit

def Fidelity_calc_arb(n_nodes, n_qpn, error=0):
    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

    # define possible single qubit inputstates
    state1 = [1, 0]
    state2 = [math.sqrt(1 / 2), math.sqrt(1 / 2)]
    state3 = [math.sqrt(1 / 2), - math.sqrt(1 / 2)]
    state4 = [math.sqrt(1 / 2), 1j * math.sqrt(1 / 2)]
    state5 = [math.sqrt(1 / 2), -1j * math.sqrt(1 / 2)]
    state6 = [0, 1]

    states = [state1, state2, state3, state4, state5, state6]

    # for all possible inputstates
    F = []
    for j in range(100):
        #make a random selection of input states
        input = []
        for i in range((n_qpn-1) * n_nodes):
            input.append(states[random.randint(0, 5)])

        # make a qft circuit
        q = QuantumRegister(n_qpn * n_nodes)
        b = [ClassicalRegister(1) for i in range(n_qpn * n_nodes)]
        circuit = QuantumCircuit(q)
        for register in b:
            circuit.add_register(register)
        # initialize control qubits
        for i in range(n_nodes):
            for j in range(n_qpn - 1):
                circuit.initialize(input[(i * (n_qpn - 1) + j)], (i * n_qpn + j))

        circuit.snapshot_statevector('snapshot_start')
        circuit = circuit.compose(two_way_qft_arbitraryn_error(n_nodes, n_qpn, error))
        circuit.snapshot_statevector('snapshot_end')

        circuit.draw('mpl')
        plt.show()
        backend = Aer.get_backend("qasm_simulator")
        result = execute(circuit, backend=backend, shots=1000).result()
        inputstate = result.data()['snapshots']['statevector']['snapshot_start'][0]
        outputstate = result.data()['snapshots']['statevector']['snapshot_end'][0]

        Fidelity = state_fidelity(inputstate, outputstate)
        print(inputstate)
        print(outputstate)
        print(Fidelity)
        F.append(Fidelity)

    return F

