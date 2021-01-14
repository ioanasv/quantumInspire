import os
from getpass import getpass
from quantuminspire.src.quantuminspire.credentials import load_account, get_token_authentication, get_basic_authentication

from qiskit import execute

from quantuminspire.src.quantuminspire.qiskit import QI
from quantuminspire.src.project_src.qfts import *
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


if __name__ == '__main__':
    authentication = get_authentication()
    QI.set_authentication(authentication, QI_URL)
    qi_backend = QI.get_backend('QX single-node simulator')

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

    circuit = circuit.compose(qft_2n_L())

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


    qi_job = execute(circuit, backend=qi_backend, shots=256)
    qi_result = qi_job.result()
    histogram = qi_result.get_counts(circuit)
    print('\nState\tCounts')
    [print('{0}\t\t{1}'.format(state, counts)) for state, counts in histogram.items()]
    # Print the full state probabilities histogram
    probabilities_histogram = qi_result.get_probabilities(circuit)
    print('\nState\tProbabilities')
    [print('{0}\t\t{1}'.format(state, val)) for state, val in probabilities_histogram.items()]
