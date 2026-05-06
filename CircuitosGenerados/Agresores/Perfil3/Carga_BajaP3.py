from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_q = QuantumRegister(5, 'q')
creg_c = ClassicalRegister(5, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# --- INICIO DEL MURO DE SE�UELOS ---

# Capa de se�uelo 1
circuit.delay(677, qreg_q[0], unit='dt')
circuit.y(qreg_q[0])
circuit.delay(2412, qreg_q[1], unit='dt')
circuit.s(qreg_q[1])
circuit.delay(1805, qreg_q[2], unit='dt')
circuit.h(qreg_q[2])
circuit.delay(346, qreg_q[3], unit='dt')
circuit.x(qreg_q[3])
circuit.delay(1942, qreg_q[4], unit='dt')
circuit.h(qreg_q[4])
circuit.barrier()

# Capa de se�uelo 2
circuit.delay(1289, qreg_q[0], unit='dt')
circuit.h(qreg_q[0])
circuit.delay(908, qreg_q[1], unit='dt')
circuit.h(qreg_q[1])
circuit.delay(386, qreg_q[2], unit='dt')
circuit.y(qreg_q[2])
circuit.delay(2618, qreg_q[3], unit='dt')
circuit.h(qreg_q[3])
circuit.delay(1085, qreg_q[4], unit='dt')
circuit.h(qreg_q[4])
circuit.barrier()

# Capa de se�uelo 3
circuit.delay(915, qreg_q[0], unit='dt')
circuit.h(qreg_q[0])
circuit.delay(405, qreg_q[1], unit='dt')
circuit.s(qreg_q[1])
circuit.delay(2843, qreg_q[2], unit='dt')
circuit.x(qreg_q[2])
circuit.delay(2990, qreg_q[3], unit='dt')
circuit.s(qreg_q[3])
circuit.delay(834, qreg_q[4], unit='dt')
circuit.h(qreg_q[4])
circuit.barrier()

# Capa de se�uelo 4
circuit.delay(2002, qreg_q[0], unit='dt')
circuit.s(qreg_q[0])
circuit.delay(1087, qreg_q[1], unit='dt')
circuit.z(qreg_q[1])
circuit.delay(2845, qreg_q[2], unit='dt')
circuit.y(qreg_q[2])
circuit.delay(669, qreg_q[3], unit='dt')
circuit.h(qreg_q[3])
circuit.delay(2588, qreg_q[4], unit='dt')
circuit.h(qreg_q[4])
circuit.barrier()

# Capa de se�uelo 5
circuit.delay(2063, qreg_q[0], unit='dt')
circuit.x(qreg_q[0])
circuit.delay(570, qreg_q[1], unit='dt')
circuit.s(qreg_q[1])
circuit.delay(1392, qreg_q[2], unit='dt')
circuit.y(qreg_q[2])
circuit.delay(752, qreg_q[3], unit='dt')
circuit.h(qreg_q[3])
circuit.delay(1749, qreg_q[4], unit='dt')
circuit.x(qreg_q[4])
circuit.barrier()

# Mediciones finales
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])
circuit.measure(qreg_q[3], creg_c[3])
circuit.measure(qreg_q[4], creg_c[4])
