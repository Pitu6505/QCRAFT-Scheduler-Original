from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

qreg_q = QuantumRegister(3, 'q')
creg_c = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qreg_q, creg_c)

# Esperando 3000 dt antes de activar el espía...
circuit.delay(3000, qreg_q[0], unit='dt')
circuit.delay(3000, qreg_q[1], unit='dt')
circuit.delay(3000, qreg_q[2], unit='dt')
circuit.barrier()

# Activando espía (Superposición equitativa)
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.h(qreg_q[2])
circuit.barrier()

# Escuchando el ruido (Crosstalk) durante 1500 dt...
circuit.delay(1500, qreg_q[0], unit='dt')
circuit.delay(1500, qreg_q[1], unit='dt')
circuit.delay(1500, qreg_q[2], unit='dt')
circuit.barrier()

# Cerrando espía y materializando el error
circuit.h(qreg_q[0])
circuit.h(qreg_q[1])
circuit.h(qreg_q[2])
circuit.barrier()

# Mediciones finales
circuit.measure(qreg_q[0], creg_c[0])
circuit.measure(qreg_q[1], creg_c[1])
circuit.measure(qreg_q[2], creg_c[2])