from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np

# Definición explícita de registros
qreg_q = QuantumRegister(5, 'q')
creg_c = ClassicalRegister(5, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# --- 1. Preparación del Estado Inicial ---
# Crea un estado entrelazado complejo antes de aplicar la QFT
circuit.h(qreg_q[4])
circuit.cx(qreg_q[4], qreg_q[3])
circuit.cx(qreg_q[3], qreg_q[2])
circuit.cx(qreg_q[2], qreg_q[1])
circuit.cx(qreg_q[1], qreg_q[0])

# --- 2. Algoritmo QFT (Quantum Fourier Transform) ---
# Qubit 4
circuit.h(qreg_q[4])
circuit.cp(np.pi / 2, qreg_q[4], qreg_q[3])
circuit.cp(np.pi / 4, qreg_q[4], qreg_q[2])
circuit.cp(np.pi / 8, qreg_q[4], qreg_q[1])
circuit.cp(np.pi / 16, qreg_q[4], qreg_q[0])

# Qubit 3
circuit.h(qreg_q[3])
circuit.cp(np.pi / 2, qreg_q[3], qreg_q[2])
circuit.cp(np.pi / 4, qreg_q[3], qreg_q[1])
circuit.cp(np.pi / 8, qreg_q[3], qreg_q[0])

# Qubit 2
circuit.h(qreg_q[2])
circuit.cp(np.pi / 2, qreg_q[2], qreg_q[1])
circuit.cp(np.pi / 4, qreg_q[2], qreg_q[0])

# Qubit 1
circuit.h(qreg_q[1])
circuit.cp(np.pi / 2, qreg_q[1], qreg_q[0])

# Qubit 0
circuit.h(qreg_q[0])

# Inversión final (Swaps)
circuit.swap(qreg_q[0], qreg_q[4])
circuit.swap(qreg_q[1], qreg_q[3])

# --- 3. Barrera y Mediciones ---
circuit.barrier()

circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])
circuit.measure(qreg_q[4], creg_c[4])