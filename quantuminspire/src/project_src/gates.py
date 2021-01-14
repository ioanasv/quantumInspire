from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit


def entangler(initial_state, circuit):
    circuit.initialize(initial_state, 0)
    zero_state = [1, 0]
    circuit.initialize(zero_state, 1)
    circuit.initialize(zero_state, 2)
    circuit.initialize(zero_state, 3)
    circuit.initialize(zero_state, 4)

    circuit.h(q[1])
    circuit.cx(q[1], q[2])
    circuit.cx(q[2], q[3])
    circuit.cx(q[3], q[4])
    circuit.cx(q[0], q[1])

    circuit.measure(1, b1)

    circuit.x(q[1]).c_if(b1, 1)
    circuit.x(q[2]).c_if(b1, 1)
    circuit.x(q[3]).c_if(b1, 1)
    circuit.x(q[4]).c_if(b1, 1)
    return circuit


def disentangler(circuit):
    circuit.h(q[2])
    circuit.h(q[3])
    circuit.h(q[4])

    circuit.measure(q[2], b2)
    circuit.measure(q[3], b3)
    circuit.measure(q[4], b4)

    circuit.z(q[0]).c_if(b2, 1)
    circuit.z(q[0]).c_if(b3, 1)
    circuit.z(q[0]).c_if(b4, 1)

    circuit.x(q[2]).c_if(b2, 1)
    circuit.x(q[3]).c_if(b3, 1)
    circuit.x(q[4]).c_if(b4, 1)
    return circuit


def teleport(state):
    q = QuantumRegister(4)
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3)
    qc.initialize(state, 0)
    zero_state = [1, 0]
    qc.initialize(zero_state, 1)
    qc.initialize(zero_state, 2)
    qc.initialize(zero_state, 3)

    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.measure(q[1], b1)
    qc.x(q[1]).c_if(b1, 1)
    qc.x(q[2]).c_if(b1, 1)
    qc.h(q[0])
    qc.measure(q[0], b0)
    qc.x(q[0]).c_if(b0, 1)
    qc.x(q[2]).c_if(b0, 1)
    qc.swap(q[2], q[3])
    return qc


def nonlocal_rk(theta):
    q = QuantumRegister(4)
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3)
    # qc.initialize(control, 0)
    # qc.initialize(target, 3)
    # zero_state = [1, 0]
    # qc.initialize(zero_state, 1)
    # qc.initialize(zero_state, 2)

    qc.h(q[1])
    qc.cx(q[1], q[2])
    qc.cx(q[0], q[1])
    qc.measure(q[1], b1)
    qc.x(q[1]).c_if(b1, 1)
    qc.x(q[2]).c_if(b1, 1)
    qc.crz(theta, q[2], q[3])
    qc.h(q[2])
    qc.measure(q[2], b2)
    qc.z(q[0]).c_if(b2, 1)
    qc.x(q[2]).c_if(b2, 1)

    return qc


def nonlocal_cnot():
    q = QuantumRegister(4)
    b0 = ClassicalRegister(1)
    b1 = ClassicalRegister(1)
    b2 = ClassicalRegister(1)
    b3 = ClassicalRegister(1)
    qc = QuantumCircuit(q, b0, b1, b2, b3)
    # qc.initialize(control, 0)
    # qc.initialize(target, 3)
    # zero_state = [1, 0]
    # qc.initialize(zero_state, 1)
    # qc.initialize(zero_state, 2)

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
