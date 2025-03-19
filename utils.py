from qiskit import QuantumCircuit
import numpy as np

def toBinary(x:int, n:int = -1)   -> str:
    """Generates binary string of decimal without annotation(?)

    Args:
        x (int): Decimal int

    Returns:
        str: String of binary equivalent
    """
    ans = bin(x)[2:]
    if n == -1:
        return ans
    n = int(n)
    l = len(ans)
    return (("0"*(n-l )+ans)[:n])

def combineQuantumCircuits(qc1:QuantumCircuit, qc2:QuantumCircuit, total_qubits:int):    
    qc = QuantumCircuit(2*total_qubits)  # The size must be greater than the sum of the sizes of the circuitsz
    qc = qc.compose(qc2)
    qc = qc.compose(qc1, qubits=range(total_qubits, 2*total_qubits))  # qubits from qc2 start at index n
    return qc

def filterWithZeros(binaryStateList:list[str], total_qubits:int, n:int):
    ans = []
    
    l = 2 * int(np.ceil(np.log2(n)))  #Number of bits required to represent the rows and columns (Once for row, once for column)
    I = []
    for i in range (l):
        I.append(i+total_qubits//2)
    # print(I)
    
    for state in binaryStateList:
        # Check if all the characters at the given indices are '0'
        if all(state[i] == '0' for i in I):
            # Remove the characters at those indices
            new_str = ''.join(state[i] for i in range(len(state)) if i not in I)
            ans.append(int(new_str, 2))

    # print("Ans", ans)
    state = np.zeros( int(np.power(2, total_qubits - len(I))))
#The number of elements in the stateVector must be equal to 2^n, where n is the number of qubits in the quantum circuit. 

    probability = 1/( np.sqrt( len(ans) ) )
    for i in ans:
        state[i] = probability
    return state

import sys

def progress_bar(total, prefix='', length=40, fill='█'):
    """
    Displays and updates a progress bar in the terminal.
    
    :param total: Total amount of work or iterations.
    :param prefix: A prefix to display before the progress bar.
    :param length: The length of the progress bar (in characters).
    :param fill: The character used to fill the progress bar.
    """
    def print_progress_bar(current):
        percent = (current / total) * 100
        filled_length = int(length * current // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent:.2f}% Complete')
        sys.stdout.flush()

    # Return a function that you can call to update the progress
    def update_progress(done):
        print_progress_bar(done)
    
    # Initial display
    print_progress_bar(0)
    
    return update_progress

import time

def timer(func):
    """
    A decorator to measure the time taken by a function and return the time along with the result.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # Record end time
        duration = end_time - start_time  # Calculate duration
        return result, round(duration, 2)  # Return the function's result and the time taken
    
    return wrapper


#https://github.com/Qiskit/qiskit-aer/issues/1511
from qiskit_aer import AerSimulator
def simulateAllStates(qc: QuantumCircuit, total_possible_states:int, to_print: bool = False) -> dict[str, int]:
    """Performs random simulations of measurement of the qubits and till all the possible states are found and returns the dict with the result of the simulations.

    Args:
        qc (QuantumCircuit): Quantum circuit to be measured.
        total_possible_states (int): Total number of theoritically possible states
        to_print (bool): Whether or not to print the result to the output console.

    Returns:
        dict[str, int]: Dictionary of key-value pairs representing qubit values and the result counts after 1024 simulations.
    """

    states = set()

    # Transpile the circuit for the simulator
    # compiled_circuit = transpile(qc, simulator)
    simulator = AerSimulator()

    while len(states) < total_possible_states:
        # Initialize the simulator
        new_qc = qc.copy()
        new_qc.measure_all()

        # Run the circuit on the simulator with 1024 shots
        sim_result = simulator.run(new_qc, shots=max(total_possible_states, 64)).result()

        # Get the measurement outcomes (counts)
        state_keys = sim_result.get_counts()

        if to_print:
            print(f"States found so far: {states}")
        
        # Add the measured states to the set
        prev = len(states)
        for k in state_keys.keys():
            states.add(k)
        new = len(states)
        # if new!=prev:
        #     print("Total states", new)
        
    states = list(states)
    states.sort()
    return states

def getAllFilteredStates(qc:QuantumCircuit, total_coords:int, half_qubits:int):
    total_pixels = ( 2**(total_coords) ) **2
    # print(total_pixels)
    states = simulateAllStates(qc, total_pixels)

    # normalizing = 2*half_qubits-1
    control_qubits = [(i) for i in range(total_coords)]
    target_qubits = [ (i+half_qubits) for i in range(total_coords)]

    new_states = []
    for state in states:
        new_states.append(state)
        for i in range(total_coords):
            if state[control_qubits[i]] != state[target_qubits[i]]:
                # print(f"{state}'s ")
                new_states.pop()
                break

    return new_states

def CNotCircuit(qc:QuantumCircuit):
    n = qc.num_qubits//2
    for i in range(n):
        print(i)
        print(n)
        qc.cx(i, i+n)
    print(qc.draw())
    return qc

def getProbArray(total:int, values:list[int]):
    rv = np.zeros(total)
    n = len(values)
    prob = np.sqrt(1/n)
    for val in values:
        rv[val] = prob
    return(rv)

def XORstate(state:str, COLOR_SIZE:int):
    n = len(state)
    first_half = state[:n//2]
    second_half = state[n//2:]
    l = n//2 - COLOR_SIZE
    ans = ""
    for i in range(n//2):
        if i < l:
            ans+=first_half[i]
        else:
            if first_half[i] == second_half[i]:
                ans+="0"
            else:
                ans+="1"
    return ans

def getXorForStates(COLOR_SIZE:int, states:list[str]):
    ans = []
    for state in states:
        ans.append(XORstate(state, COLOR_SIZE))
    return ans





def progress_bar(total, prefix='', length=40, fill='█'):
    """
    Displays and updates a progress bar in the terminal.
    
    :param total: Total amount of work or iterations.
    :param prefix: A prefix to display before the progress bar.
    :param length: The length of the progress bar (in characters).
    :param fill: The character used to fill the progress bar.
    """
    def print_progress_bar(current):
        percent = (current / total) * 100
        filled_length = int(length * current // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        sys.stdout.write(f'\r{prefix} |{bar}| {percent:.2f}% Complete')
        sys.stdout.flush()

    # Return a function that you can call to update the progress
    def update_progress(done):
        print_progress_bar(done)
    
    # Initial display
    print_progress_bar(0)
    
    return update_progress
