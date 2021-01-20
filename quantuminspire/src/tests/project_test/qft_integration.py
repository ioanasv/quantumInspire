import unittest
import os
from getpass import getpass
from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit import execute

from quantuminspire.src.quantuminspire.qiskit import QI
from quantuminspire.src.project_src.qfts import *
import numpy as np
from qiskit.circuit.library import QFT

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


class QftIntegrationTests(unittest.TestCase):

    def test_qft_2n(self):
        authentication = get_authentication()
        QI.set_authentication(authentication, QI_URL)
        qi_backend = QI.get_backend('QX single-node simulator')

        qubit_count = 8
        q = QuantumRegister(qubit_count)
        b = [ClassicalRegister(1) for i in range(qubit_count)]
        circuit = QuantumCircuit(q)
        for register in b:
            circuit.add_register(register)

        qb1 = [1, 0]
        qb2 = [1, 0]
        qb3 = [1, 0]
        qb4 = [1, 0]
        qb5 = [1, 0]
        qb6 = [1, 0]
        # qb1 = [0, 1]
        # qb2 = [0, 1]
        # qb3 = [0, 1]
        # qb4 = [0, 1]
        # qb5 = [0, 1]
        # qb6 = [0, 1]

        circuit.initialize(qb1, 0)
        circuit.initialize(qb2, 1)
        circuit.initialize(qb3, 2)
        circuit.initialize(qb4, 5)
        circuit.initialize(qb5, 6)
        circuit.initialize(qb6, 7)

        circuit = circuit.compose(qft_2n())

        circuit.measure(q[0], b[0])
        circuit.measure(q[1], b[1])
        circuit.measure(q[2], b[2])
        circuit.measure(q[3], b[3])
        circuit.measure(q[4], b[4])
        circuit.measure(q[5], b[5])
        circuit.measure(q[6], b[6])
        circuit.measure(q[7], b[7])

        qi_job = execute(circuit, backend=qi_backend, shots=256)
        qi_result = qi_job.result()
        histogram = qi_result.get_counts(circuit)

        for i, prob in enumerate(qubit_probabilities(histogram)):
            print(i, " is |1> with probability ", prob)
        self.assertEqual(True, True)

    def test_qft_3n(self):
            authentication = get_authentication()
            QI.set_authentication(authentication, QI_URL)
            qi_backend = QI.get_backend('QX single-node simulator')

            qubit_count = 9
            q = QuantumRegister(qubit_count)
            b = [ClassicalRegister(1) for i in range(qubit_count)]
            circuit = QuantumCircuit(q)
            for register in b:
                circuit.add_register(register)

            qb1 = [1, 0]
            qb2 = [1, 0]
            qb3 = [1, 0]
            qb4 = [1, 0]
            qb5 = [1, 0]
            qb6 = [1, 0]
            # qb1 = [0, 1]
            # qb2 = [0, 1]
            # qb3 = [0, 1]
            # qb4 = [0, 1]
            # qb5 = [0, 1]
            # qb6 = [0, 1]

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

            for i, prob in enumerate(qubit_probabilities(histogram)):
                print(i, " is |1> with probability ", prob)
            self.assertEqual(True, True)

    def test_qft_2n_inverse(self):
        authentication = get_authentication()
        QI.set_authentication(authentication, QI_URL)
        qi_backend = QI.get_backend('QX single-node simulator')

        qubit_count = 8
        q = QuantumRegister(qubit_count)
        b = [ClassicalRegister(1) for i in range(qubit_count)]
        circuit = QuantumCircuit(q)
        for register in b:
            circuit.add_register(register)

        one = [0, 1]
        zero = [1, 0]

        circuit.initialize(one, 0)
        circuit.initialize(one, 1)
        circuit.initialize(one, 2)
        circuit.initialize(one, 5)
        circuit.initialize(one, 6)
        circuit.initialize(one, 7)

        circuit = circuit.compose(qft_2n())

        # construct and add native inverse qft
        inverse_qft = QFT(num_qubits=6, inverse=True, do_swaps=False)
        circuit = circuit.compose(inverse_qft, qubits=[0, 1, 2, 5, 6, 7])

        circuit.measure(q[0], b[0])
        circuit.measure(q[1], b[1])
        circuit.measure(q[2], b[2])
        circuit.measure(q[3], b[3])
        circuit.measure(q[4], b[4])
        circuit.measure(q[5], b[5])
        circuit.measure(q[6], b[6])

        qi_job = execute(circuit, backend=qi_backend, shots=256)
        qi_result = qi_job.result()
        histogram = qi_result.get_counts(circuit)

        for i, prob in enumerate(qubit_probabilities(histogram)):
            print(i, " is |1> with probability ", prob)
        self.assertEqual(True, True)

    def test_local_qft_inverse(self):
        authentication = get_authentication()
        QI.set_authentication(authentication, QI_URL)
        qi_backend = QI.get_backend('QX single-node simulator')

        q = QuantumRegister(6)
        b = [ClassicalRegister(1) for i in range(6)]
        circuit = QuantumCircuit(q)
        for register in b:
            circuit.add_register(register)

        input = [0, 0, 0, 0, 1, 1]
        circuit = circuit.compose(local_qft(6, input))

        # construct and add native inverse qft
        inverse_qft = QFT(num_qubits=6, inverse=True, do_swaps=True)
        circuit = circuit.compose(inverse_qft)

        circuit.measure(q[0], b[0])
        circuit.measure(q[1], b[1])
        circuit.measure(q[2], b[2])
        circuit.measure(q[3], b[3])
        circuit.measure(q[4], b[4])
        circuit.measure(q[5], b[5])

        qi_job = execute(circuit, backend=qi_backend, shots=256)
        qi_result = qi_job.result()
        histogram = qi_result.get_counts(circuit)

        result_probabilities = qubit_probabilities(histogram)
        # Need to reverse order because local_qft does so
        result_probabilities.reverse()
        for i, prob in enumerate(result_probabilities):
            print(i, " is |1> with probability ", prob)
        right_answers = [int(a) == int(b) for (a, b) in zip (result_probabilities, input)]
        self.assertEqual(False, right_answers.__contains__(False))


if __name__ == '__main__':
    unittest.main()
