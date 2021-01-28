import os
import math
import statistics
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
    return A

if __name__ == '__main__':

    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

    # n_nodes = 2
    # n_qpn = 4
    # F = fidelity_calc_arb(n_nodes, n_qpn, 0, 0.2)
    #
    # n_nodes = 3
    # n_qpn = 3
    # F = fidelity_calc_arb(n_nodes, n_qpn, 0, 0.2)

    # error = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
    # error = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    # error[:] = [x / 10 for x in error]
    # nodes = [1, 2, 3, 6]
    #
    # F1 = [0.9680183001046634, 0.968887093085254, 0.9731031578152627, 0.968272084366767, 0.9713578354645237, 0.9693104373845137, 0.9667457755261211, 0.9730457028085607, 0.9715751926926203, 0.9689132843936221, 0.9720653584420776, 0.9712266046757123, 0.9731583831020721, 0.9707055032171785, 0.970705562179441, 0.9714603894836484, 0.9674419638183691, 0.9672283789154709, 0.9695182839384042, 0.9693537727463255, 0.9669959601251708]
    # F2 = [0.9695343109113815, 0.9352870587290791, 0.8377740777887099, 0.7069086997249321, 0.5706280351038949, 0.43139847517494956, 0.32840593348967767, 0.234938097630175, 0.1926485238761473, 0.12023950821664021, 0.10895120097628337, 0.07419464403318846, 0.04775421783207794, 0.03246235516869507, 0.021610442681792692, 0.012451172850851344, 0.006116058863756617, 0.002225930194310251, 0.0005053746000580023, 3.452040028127723e-05, 1.3078073781862266e-65]
    # F3 = [0.9689823695832717, 0.9098852077182528, 0.7658327199767109, 0.5681183049909776, 0.402315417306892, 0.24385569246821256, 0.16586926891593848, 0.09936928052677019, 0.04520490748876834, 0.035615708759370805, 0.026070464063412613, 0.016128380900751433, 0.0099523824420318, 0.004215586906667261, 0.0025896628747120835, 0.0012279415778952065, 0.0003957302018274117, 9.148874438062099e-05, 1.0142270173335847e-05, 1.8427534584540538e-07, 4.3139755057737894e-98]
    # F4 = [0.9700084369798555, 0.8670527242706386, 0.6187331847639885, 0.35694605272448615, 0.16735621424518948, 0.0721426928393579, 0.029661056849064265, 0.010233856526971825, 0.0034347834345732934, 0.001203128263479192, 0.0003290451757665023, 0.00016852757884739183, 7.069577885880324e-05, 2.3858074351140087e-05, 6.4825594811109624e-06, 1.2984625127285893e-06, 1.491117604465369e-07, 7.0802645855502486e-09, 7.70793692050764e-11, 2.3211623893160605e-14, 1.2661205131230175e-195]
    #
    #
    #
    # for i in nodes:
    #     print(1)
    #     n_nodes = i
    #     n_qpn = math.floor(6/n_nodes) + 1
    #     print(n_nodes)
    #     print(n_qpn)
    #     F = fidelity_node_comparisson(n_nodes, n_qpn)
    #     plt.plot(error, F)
    #
    # # plt.plot(error, F1)
    # # plt.plot(error, F2)
    # # plt.plot(error, F3)
    # # plt.plot(error, F4)
    # plt.xlabel('overshoot')
    # plt.ylabel('Average fidelity')
    # plt.title('Average fidelity as a function of overshoot percentage')
    # # plt.legend('ry gate overshoot', 'ry and x gate overshoot')
    # plt.legend(['1 node', '2 nodes', '3 nodes', '6 nodes'])
    # plt.show()

    q = QuantumRegister(4)
    b = [ClassicalRegister(1) for i in range(4)]
    circuit = QuantumCircuit(q)
    for register in b:
        circuit.add_register(register)
    circuit = circuit.compose(qft_arbitraryn(2, 2, ry_error=0.1, x_error=0.1))
    circuit.draw('mpl')
    plt.show()


