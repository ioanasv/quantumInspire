from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit

from quantuminspire.src.quantuminspire.qiskit import QI
from quantuminspire.src.project_src.qfts import *
import matplotlib.pyplot as plt
import numpy as np


def generate_statistics(circuit):
    cdepth = circuit.depth()
    csize = circuit.size()
    opdic = circuit.count_ops()

    if 'measure' in opdic.keys():
        n_measurements = opdic['measure']
    else:
        n_measurements = 0

    if 'x' in opdic.keys():
        n_x = opdic['x']
    else:
        n_x = 0

    if 'z' in opdic.keys():
        n_z = opdic['z']
    else:
        n_z = 0

    if 'h' in opdic.keys():
        n_h = opdic['h']
    else:
        n_h = 0

    if 'crz' in opdic.keys():
        n_crz = opdic['crz']
    else:
        n_crz = 0

    if 'cx' in opdic.keys():
        n_cx = opdic['cx']
    else:
        n_cx = 0

    n_1qbgate = n_h + n_x + n_z
    n_2qbgate = n_crz + n_cx
    n_clctrlgate = n_x + n_z
    n_comm = n_h - circuit.width()/2 - n_measurements/2
    stats = [cdepth, csize, n_measurements, n_1qbgate, n_2qbgate, n_clctrlgate, n_comm]
    print(stats)

    return stats


def compare_node_distributions(n_inputqb, doplot=True):
    primefactors = get_primefactors(n_inputqb)
    stats = np.empty([len(primefactors), 7])
    for i in range(len(primefactors)):
        n_nodes = primefactors[i]
        qc = qft_arbitraryn(n_nodes, n_inputqb // n_nodes + 1)
        stats[i, :] = generate_statistics(qc)
    if doplot:
        fig, axs = plt.subplots(2)
        # axs[0].title("QFT circuit depth and size for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[0].plot(primefactors, stats[:, 0], '.-', label="Circuit depth")
        axs[0].plot(primefactors, stats[:, 1], '.-', label="Circuit size")
        # axs[0].plot(primefactors, stats[:, 1]*n_inputqb/np.array(primefactors))
        # axs[0].loglog(primefactors, stats[:, 0],'.-' , label="Circuit depth")
        # axs[0].loglog(primefactors, stats[:, 1],'.-' , label="Circuit size")
        axs[0].set_xlabel("Amount of nodes")
        axs[0].set_ylabel("Amount of operations")
        axs[0].grid()
        # axs[0].set_ylim([0, stats[-1, 1]*1.1])
        axs[0].legend()

        # axs[1].title("Amounts of operations for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[1].plot(primefactors, stats[:, 2],'.-' , label="Measurements")
        axs[1].plot(primefactors, stats[:, 3],'.-' , label="Single qubit gates (classically controlled or not)")
        axs[1].plot(primefactors, stats[:, 4],'.-' , label="2-qubit gates")
        axs[1].plot(primefactors, stats[:, 6],'.-' , label="Shared entangled qubits")
        axs[1].set_xlabel("Amount of nodes")
        axs[1].set_ylabel("Amount of operations")
        # axs[1].set_ylim([0, stats[-1,0]])
        axs[1].grid()
        axs[1].legend()
        fig.show()
    return stats


def compare_input_qubits(n_nodes, input_array, doplot=True):
    stats = np.empty([len(input_array), 7])
    for i in range(len(input_array)):
        qc = qft_arbitraryn(n_nodes, input_array[i] // n_nodes + 1)
        stats[i, :] = generate_statistics(qc)
    if doplot:
        fig, axs = plt.subplots(2)
        # axs[0].title("QFT circuit depth and size for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[0].plot(input_array, stats[:, 0],'.-' , label="Circuit depth for {} nodes".format(n_nodes))
        axs[0].plot(input_array, stats[:, 1],'.-' , label="Circuit size for {} nodes".format(n_nodes))
        # axs[0].loglog(input_array, stats[:, 0],'.-' , label="Circuit depth")
        # axs[0].loglog(input_array, stats[:, 1],'.-' , label="Circuit size")
        axs[0].set_xlabel("Amount of input qubits")
        axs[0].set_ylabel("Amount of operations")
        axs[0].grid()
        axs[0].legend()

        # axs[1].title("Amounts of operations for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[1].plot(input_array, stats[:, 2],'.-' , label="Measurements for {} nodes".format(n_nodes))
        axs[1].plot(input_array, stats[:, 3],'.-' , label="Single qubit gates (classically controlled or not) for {} nodes".format(n_nodes))
        axs[1].plot(input_array, stats[:, 4],'.-' , label="2-qubit gates for {} nodes".format(n_nodes))
        axs[1].plot(input_array, stats[:, 6],'.-' , label="Shared entangled qubits for {} nodes".format(n_nodes))
        axs[1].set_xlabel("Amount of input qubits")
        axs[1].set_ylabel("Amount of operations")
        axs[1].grid()
        axs[1].legend()
        fig.show()
    return stats


def compare_multinode_input_scaling(n_nodes, max_input, doplot=True):

    # stats = np.empty([len(n_nodes), len(n_nodes)])
    for n_node in n_nodes:
        input_array = range(n_node, max_input, n_node)
        stats = np.empty(len(input_array))
        for i in range(len(input_array)):

            qc = qft_arbitraryn(n_node, input_array[i] // n_node + 1)
            stats[i] = generate_statistics(qc)[1]
        plt.plot(input_array, stats, '.-', label="Circuit size for {} nodes".format(n_node))
    plt.xlabel("Amount of input qubits")
    plt.ylabel("Circuit size")
    plt.grid()
    plt.legend()
    plt.show()
    # if doplot:
    #     fig, axs = plt.subplots(2)
    #     # axs[0].title("QFT circuit depth and size for different amounts of nodes and {} input qubits".format(n_inputqb))
    #     axs[0].plot(input_array, stats[:, 0], '.-', label="Circuit depth for {} nodes".format(n_nodes))
    #     # axs[0].plot(input_array, stats[:, 1], '.-', label="Circuit size for {} nodes".format(n_nodes))
    #     # axs[0].loglog(input_array, stats[:, 0],'.-' , label="Circuit depth")
    #     # axs[0].loglog(input_array, stats[:, 1],'.-' , label="Circuit size")
    #     axs[0].set_xlabel("Amount of input qubits")
    #     axs[0].set_ylabel("Amount of operations")
    #     axs[0].grid()
    #     axs[0].legend()


def compare_multinode_total_scaling(n_nodes, max_input, doplot=True):

    # stats = np.empty([len(n_nodes), len(n_nodes)])
    for n_node in n_nodes:
        input_array = range(n_node, max_input, n_node)
        stats = np.empty(len(input_array))
        for i in range(len(input_array)):

            qc = qft_arbitraryn(n_node, input_array[i] // n_node + 1)
            stats[i] = generate_statistics(qc)[1]
        plt.log(np.array(input_array) + n_node, stats, '.-', label="Circuit depth for {} nodes".format(n_node))
    plt.xlabel("Total amount of qubits")
    plt.ylabel("Circuit depth")
    plt.grid()
    plt.legend()
    plt.show()
    # if doplot:
    #     fig, axs = plt.subplots(2)
    #     # axs[0].title("QFT circuit depth and size for different amounts of nodes and {} input qubits".format(n_inputqb))
    #     axs[0].plot(input_array, stats[:, 0], '.-', label="Circuit depth for {} nodes".format(n_nodes))
    #     # axs[0].plot(input_array, stats[:, 1], '.-', label="Circuit size for {} nodes".format(n_nodes))
    #     # axs[0].loglog(input_array, stats[:, 0],'.-' , label="Circuit depth")
    #     # axs[0].loglog(input_array, stats[:, 1],'.-' , label="Circuit size")
    #     axs[0].set_xlabel("Amount of input qubits")
    #     axs[0].set_ylabel("Amount of operations")
    #     axs[0].grid()
    #     axs[0].legend()


def compare_node_scaling(node_size, n_nodes_array, doplot=True):

    stats = np.empty([len(n_nodes_array), 7])
    for i in range(len(n_nodes_array)):
        qc = qft_arbitraryn(n_nodes_array, node_size)
        stats[i, :] = generate_statistics(qc)
    if doplot:
        n_qubits = n_nodes_array*node_size
        fig, axs = plt.subplots(2)
        # axs[0].title("QFT circuit depth and size for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[0].plot(n_qubits, stats[:, 0],'.-' , label="Circuit depth for {} nodes".format(n_nodes))
        axs[0].plot(n_qubits, stats[:, 1],'.-' , label="Circuit size for {} nodes".format(n_nodes))
        # axs[0].loglog(primefactors, stats[:, 0],'.-' , label="Circuit depth")
        # axs[0].loglog(primefactors, stats[:, 1],'.-' , label="Circuit size")
        axs[0].set_xlabel("Amount of input qubits")
        axs[0].set_ylabel("Amount of operations")
        axs[0].grid()
        axs[0].legend()

        # axs[1].title("Amounts of operations for different amounts of nodes and {} input qubits".format(n_inputqb))
        axs[1].plot(n_qubits, stats[:, 2],'.-' , label="Measurements for {} nodes".format(n_nodes))
        axs[1].plot(n_qubits, stats[:, 3],'.-' , label="Single qubit gates (classically controlled or not) for {} nodes".format(n_nodes))
        axs[1].plot(n_qubits, stats[:, 4],'.-' , label="2-qubit gates for {} nodes".format(n_nodes))
        axs[1].plot(n_qubits, stats[:, 6],'.-' , label="Shared entangled qubits for {} nodes".format(n_nodes))
        axs[1].set_xlabel("Amount of input qubits")
        axs[1].set_ylabel("Amount of operations")
        axs[1].grid()
        axs[1].legend()
        fig.show()
    return stats


def get_primefactors(n):
    factors = []
    for i in range(1, n+1):
        if n % i == 0:
            factors.append(i)
    return factors


if __name__ == '__main__':
    # qc = qft_arbitraryn(2, 3)
    # stats = generate_statistics(qc)
    # qc.draw('mpl', filename="qcirc.png")

    compare_node_distributions(12)
    # n_nodes = 2
    # compare_input_qubits(n_nodes, range(n_nodes, 36, n_nodes))
    # compare_node_scaling(4, range(1, 9))
    # compare_multinode_input_scaling(n_nodes=get_primefactors(45), max_input=46)
    # compare_multinode_total_scaling(n_nodes=get_primefactors(30), max_input=31)

