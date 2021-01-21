import os
import math
from getpass import getpass
from quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit import execute
from qiskit import IBMQ, Aer

from quantuminspire.qiskit import QI
import matplotlib.pyplot as plt

from qiskit.quantum_info import state_fidelity
from qiskit.providers.aer.extensions.snapshot_statevector import *

from qfts import *
from fidelity import *

QI_EMAIL = os.getenv('QI_EMAIL')
QI_PASSWORD = os.getenv('QI_PASSWORD')
QI_URL = os.getenv('API_URL', 'https://api.quantum-inspire.com/')
# import os
# import math
# import random
# import numpy as np
# # from getpass import getpass
# # from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication
#
# from qiskit import execute
#
# # from quantuminspire.src.quantuminspire.qiskit import QI
# from qfts import *
# from fidelity import *
# import matplotlib.pyplot as plt
#
# from qiskit.quantum_info import state_fidelity
# from qiskit.providers.aer.extensions.snapshot_statevector import *
# from qiskit.providers.aer.noise import depolarizing_error
# from qiskit.providers.aer.noise import NoiseModel
# from qiskit import IBMQ, Aer
# from qiskit.visualization import plot_bloch_multivector

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

    circuit.snapshot_statevector('snapshot1')
    circuit = circuit.compose(qft_arbitraryn(n_nodes, node_qubits))
    circuit.snapshot_statevector('snapshot2')

    circuit.draw('mpl')
    plt.show()

    print("\nResult from the local Qiskit simulator backend:\n")
    backend = Aer.get_backend("qasm_simulator")
    result = execute(circuit, backend=backend, shots=1000).result()

    baselinestate = result.data()['snapshots']['statevector']['snapshot1'][0]

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
    print(1)
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

        print(2)
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

    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

    n_nodes = 1
    n_qpn = 3
    F = Fidelity_calc_arb(n_nodes, n_qpn, 1)
    print(F)