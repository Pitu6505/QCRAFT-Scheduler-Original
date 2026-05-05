from __future__ import annotations

import time
import os
import json
from typing import Optional, Any

import numpy as np


def _load_braket() -> tuple[Any, Any, Any, Any]:
    """
    Import Braket components only when AWS execution is actually needed.
    """
    try:
        from braket.circuits import Circuit
        from braket.devices import LocalSimulator
        from braket.aws import AwsDevice
        from braket.aws.aws_quantum_task import AwsQuantumTask
    except ImportError as exc:
        raise ImportError(
            "Amazon Braket is not available or is incompatible with the installed version. "
            "Local scheduler startup does not require it, but AWS execution paths do."
        ) from exc

    return Circuit, LocalSimulator, AwsDevice, AwsQuantumTask


def code_to_circuit_aws(code_str: str) -> Any:
    """
    Transforms a string representation of a circuit into a Braket circuit.

    Args:
        code_str (str): The string representation of the Braket circuit.

    Returns:
        The circuit object.
    """
    Circuit, _, _, _ = _load_braket()

    try:
        lines = code_str.strip().split('\n')
        circuit = Circuit()
        safe_namespace = {'np': np, 'pi': np.pi}

        for line in lines:
            if line.startswith("circuit."):
                operation = line.split('circuit.')[1]
                gate_name = operation.split('(')[0]

                if gate_name in ['rx', 'ry', 'rz', 'gpi', 'gpi2', 'phaseshift']:
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubit = int(args[0].split('+')[0]) + int(args[0].split('+')[1].strip(') ')) if '+' in args[0] else int(args[0].strip(') ').strip())
                    angle = eval(args[1], {"__builtins__": None}, safe_namespace)
                    getattr(circuit, gate_name)(target_qubit, angle)
                elif gate_name in ['xx', 'yy', 'zz'] or 'cphase' in gate_name:
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-1]]
                    angle = eval(args[-1], {"__builtins__": None}, safe_namespace)
                    getattr(circuit, gate_name)(*target_qubits, angle)
                elif gate_name == 'ms':
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args[:-3]]
                    angles = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args[-3:]]
                    getattr(circuit, gate_name)(*target_qubits, *angles)
                else:
                    args = operation.split('(')[1].strip(')').split(',')
                    target_qubits = [int(arg.split('+')[0]) + int(arg.split('+')[1].strip(') ')) if '+' in arg else int(arg.strip(') ').strip()) for arg in args if not any(c.isalpha() for c in arg)]
                    params = [eval(arg, {"__builtins__": None}, safe_namespace) for arg in args if any(c.isalpha() for c in arg)]
                    getattr(circuit, gate_name)(*target_qubits)
    except Exception:
        raise ValueError("Invalid circuit code")

    return circuit


def get_transpiled_circuit_depth_aws(circuit: Any, backend) -> None:
    """
    Transpiles a circuit and returns its depth.

    Args:
        circuit: The circuit to transpile.
        backend: The machine to transpile the circuit.
    """
    # TODO
    return None


def retrieve_result_aws(id: int) -> dict:
    """
    Retrieves the results of a circuit execution from the AWS cloud based on a task id.
    """
    _, _, AwsDevice, _ = _load_braket()

    task = AwsDevice.retrieve(id)
    return recover_task_result(task).measurement_counts


def recover_task_result(task_load: Any) -> dict:
    """
    Waits for the task to complete and recovers the results of the circuit execution.
    """
    _, _, _, AwsQuantumTask = _load_braket()

    sleep_times = 0
    while sleep_times < 100000:
        status = task_load.state()
        print('Status of (reconstructed) task:', status)
        print('\n')
        if status == 'COMPLETED':
            return task_load.result()
        time.sleep(1)
        sleep_times += 1

    print("Quantum execution time exceeded")
    return None


def runAWS(machine: str, circuit: Any, shots: int, s3_folder: Optional[str] = None) -> dict:
    """
    Executes a circuit in the AWS cloud.
    """
    _, LocalSimulator, AwsDevice, _ = _load_braket()

    x = int(shots)

    if machine == "local":
        device = LocalSimulator()
        result = device.run(circuit, shots=x).result()
        counts = result.measurement_counts
        print(counts)
        return counts

    device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:
        s3_folder = ('amazon-braket-jorgecs', 'test/')
        task = device.run(circuit, s3_folder, shots=x, poll_timeout_seconds=5 * 24 * 60 * 60)
        counts = recover_task_result(task).measurement_counts
        return counts

    task = device.run(circuit, s3_folder, shots=x)
    counts = task.result().measurement_counts
    return counts


def runAWS_save(machine: str, circuit: Any, shots: int, users: list, qubit_number: list, circuit_names: list, s3_folder: Optional[str] = None) -> dict:
    """
    Executes a circuit in the AWS cloud and saves the task id if the machine crashes.
    """
    _, LocalSimulator, AwsDevice, _ = _load_braket()

    x = int(shots)

    if machine == "local":
        device = LocalSimulator()
        result = device.run(circuit, shots=x).result()
        counts = result.measurement_counts
        print(counts)
        return counts

    device = AwsDevice(machine)

    if "sv1" not in machine and "tn1" not in machine:
        s3_folder = ('amazon-braket-jorgecs', 'test/')

        task = device.run(circuit, s3_folder, shots=x, poll_timeout_seconds=5 * 24 * 60 * 60)

        id = task
        user_shots = [shots] * len(circuit_names)
        provider = 'aws'
        script_dir = os.path.dirname(os.path.realpath(__file__))
        ids_file = os.path.join(script_dir, 'ids.txt')
        with open(ids_file, 'a') as file:
            file.write(json.dumps({id: (users, qubit_number)}))
            file.write(json.dumps({id: (users, qubit_number, user_shots, provider, circuit_names)}))
            file.write('\n')

        counts = recover_task_result(task).measurement_counts

        with open(ids_file, 'r') as file:
            lines = file.readlines()
        with open(ids_file, 'w') as file:
            for line in lines:
                line_dict = json.loads(line.strip())
                if list(line_dict.keys())[0] != id:
                    file.write(line)

        return counts

    task = device.run(circuit, s3_folder, shots=x)
    counts = task.result().measurement_counts
    return counts