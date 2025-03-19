from neqr import neqr
from utils import getAllFilteredStates, combineQuantumCircuits, getXorForStates
# from qiskit import QuantumCircuit
# from utils import CNotCircuit, getProbArray, simulateAllStates

DEBUGMODE = True
# DEBUGMODE = False

def encrypt(M1:list[list[int]], M2:list[list[int]], l:int, COLOR_SIZE:int = 8) -> list[list[int]]:
    """_summary_

    Args:
        M1 (list[list[int]]): _description_
        M2 (list[list[int]]): _description_
        l (int): Total bits taken by a coordinate(row bits + col bits)
        COLOR_SIZE (int, optional): _description_. Defaults to 8.
    """
    qc1 = neqr(M1, COLOR_SIZE=COLOR_SIZE)
    qc2 = neqr(M2, COLOR_SIZE=COLOR_SIZE)
    total_qubits = l + COLOR_SIZE
    total_pixels = 2**(l)
    qc_combined = combineQuantumCircuits(qc1, qc2, total_qubits=total_qubits)

    filtered_arr = getAllFilteredStates(qc_combined, total_coords=l, half_qubits=total_qubits)
    # print(filtered_arr)
    states = getXorForStates(COLOR_SIZE, filtered_arr)
    states.sort()

    row = len(M1)
    col = len(M1[0])

    rv = []

    ## Nothing is WRoing is something here

    for i in range(row):
        row_lst = []
        for j in range(col):
            row_lst.append(int(states[i*row+j][l:], 2))
        rv.append(row_lst)

    # rv = [
    #     [int(states[0][l:], 2), int(states[1][l:], 2)],
    #     [int(states[2][l:], 2), int(states[3][l:], 2)]
    # ]

    return rv

