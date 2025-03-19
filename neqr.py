from qiskit import QuantumCircuit
from utils import toBinary, simulateAllStates
import numpy as np

def neqr(M:list[list[int]], COLOR_SIZE:int = 8):

    n = max( len(M), len(M[0]) )      #Number of rows and columns
    l = 2 * int(np.ceil(np.log2(n)))  #Number of bits required to represent the rows and columns (Once for row, once for column)
    total_qubits  = l + COLOR_SIZE

    bitstring_lst = []

    for i in range(n):  #Row
        for j in range (n): #Column
            bitstring_lst.append(f"{toBinary(i, l/2)}{toBinary(j, l/2)}{toBinary(M[i][j], COLOR_SIZE)}")

    probability = 1/( n )

    state = np.zeros( int(np.power(2, total_qubits))) #state = np.zeros(16, dtype=complex)
    #The number of elements in the stateVector must be equal to 2^n, where n is the number of qubits in the quantum circuit. 

    for bitstring in bitstring_lst:
        state_index = int(bitstring, 2)
        state[ state_index ] = probability

    qc = QuantumCircuit(total_qubits)

    try:
        qc.initialize(state, [x for x in range(total_qubits)])
    except:
        print("The sum was wrongly found to be: ")
        temp = 0
        for s in state:
            if s:
                print(s)
                temp += (s*s)
        print(temp)

    return qc


def deneqr(qc: QuantumCircuit, l:int, COLORSIZE = 8)  -> list[list[int]]:
    # state_vector = quantumStatevectorDict(qc, True)
    total_pixels = 2**(l)
    state_vector = simulateAllStates(qc, total_pixels)
    state_vector.sort()
    n = 2**(l//2) #Cuz l = number_of_bits_to_represent_rows + number_of_bits_to_represent_col
    M = []
    print()
    for i in range(n):
        row = []
        for j in range(n):
            row.append(int( state_vector[i*n+j] [l:], 2))
        # print(row)
        M.append(row)
    # print(M)
    return M
