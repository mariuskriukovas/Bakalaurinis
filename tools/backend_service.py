from qiskit import IBMQ, Aer
from qiskit import execute
from qiskit.providers.ibmq import least_busy

from git.Bakalaurinis.tools.IO_service import write_results

number_of_shots = 1024


# number_of_shots = 10

def request_least_busy_backend(nqubits):
    # IBMQ.save_account(get_TOKEN())
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= nqubits
                                                             and not x.configuration().simulator
                                                             and x.status().operational == True))
    print("least busy backend: ", backend)
    return backend


def request_yorktown_backend():
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = provider.get_backend('ibmq_5_yorktown')
    print("ibmq_5_yorktown available: ", backend)
    return backend


def request_lima_backend():
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = provider.get_backend('ibmq_lima')
    print("ibmq_lima available: ", backend)
    return backend


def request_quito_backend():
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    backend = provider.get_backend('ibmq_quito')
    print("ibmq_quito available: ", backend)
    return backend



def request_local_backend():
    return Aer.get_backend('qasm_simulator')


def request_unitary_backend():
    return Aer.get_backend('unitary_simulator')


def request_state_vector_backend():
    return Aer.get_backend('statevector_simulator')


def simulate(qc, backend):
    job = execute(qc, backend, shots=number_of_shots)
    return job.result()


def simulate_all(q_arr, dir_name, name, back):
    for i, qi in enumerate(q_arr):
        file_name = f'{name}_{str(i)}'
        (qr, cr, qc) = qi
        result = simulate(qc, back)
        write_results(result, dir_name, file_name)

import threading

def thread_execute_experiment(name, i, qi, back, dir_name):
    file_name = f'{name}_{str(i)}'
    (qr, cr, qc) = qi
    result = simulate(qc, back)
    write_results(result, dir_name, file_name)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def simulate_all_parallel(q_arr, dir_name, name, back):
    threads_arr = []
    for i, qi in enumerate(q_arr):
        x = threading.Thread(target=thread_execute_experiment, args=(name, i, qi, back, dir_name))
        threads_arr.append(x)

    threads_chunks_arr = list(chunks(threads_arr, 5))
    for t_arr in threads_chunks_arr:
        for t in t_arr:
            t.start()
        for t in t_arr:
            t.join()

# MAX 5 qubits
def simulate_on_yorktown_all(q_arr, dir_name, name):
    back = request_yorktown_backend()
    name = f'{name}_Y'
    dir_name = f'{dir_name}_Y'
    # simulate_all(q_arr, dir_name, name, back)
    simulate_all_parallel(q_arr, dir_name, name, back)
    print("DONE")


# mock_arr = [mock.get_MOCK_circuit()]
# simulate_on_yorktown_all(mock_arr, "mock", "TEST")

def simulate_local_all(q_arr, dir_name, name):
    back = request_local_backend()
    name = f'{name}_L'
    simulate_all(q_arr, dir_name, name, back)
    # simulate_all_parallel(q_arr, dir_name, name, back)
    print("DONE")


def simulate_lima_all(q_arr, dir_name, name):
    back = request_lima_backend()
    name = f'{name}_Lima'
    simulate_all(q_arr, dir_name, name, back)
    print("DONE")


def simulate_quito_all(q_arr, dir_name, name):
    back = request_quito_backend()
    name = f'{name}_Quito'
    # simulate_all(q_arr, dir_name, name, back)
    simulate_all_parallel(q_arr, dir_name, name, back)
    print("DONE")


# mock_arr = [mock.get_MOCK_circuit(), mock.get_MOCK_circuit()]
# simulate_local_all(mock_arr, "mock_local", "TEST")

def simulate_unitary(q):
    (qr, cr, qc) = q
    back = request_unitary_backend()
    job = execute(qc, back)
    return job.result()


def simulate_state_vector(q):
    (qr, cr, qc) = q
    back = request_state_vector_backend()
    out_state = execute(qc, back).result().get_statevector()
    return out_state
