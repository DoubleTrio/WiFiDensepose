# NOTE - THIS IS STILL WIP

# pylint: disable=import-error, missing-function-docstring, invalid-name
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from scipy.ndimage import uniform_filter
from scipy.signal import medfilt

def complex_converter(txt: str) -> complex:
    """
    Converts a string to a complex number
    Example: "20+-30i" -> 20-30j
    """
    txt = txt.replace("+-", "-").replace("i", "j")
    return complex(txt)

def process_csv(df: pd.DataFrame) -> list[np.ndarray]:
    """
    Converts a Pandas dataframe to np.ndarray of matrixes of the CSI matrix
    """
    results = []
    count = 0
    for _, row in enumerate(df):
        # Make sure CSI column exists by checking if it's a string...
        if (isinstance(row[18], str)):
            results.append(process_csi_row(row, count))
            count += 1

    return results

def process_csi_row(row: np.ndarray, count: int) -> np.ndarray:
    """
    Process a row in the csv file 
    
    Parameters 
    row: ndarray(N)
        The Nth row of the csv file
    row[0] = field length (int)
    row[1] = timestamp (int)
    row[2] = CSI length (int)
    row[3] = 
    row[4]
    ...
    row[9] = NR
    row[10] = NC
    row[18] = CSI
    Returns
    -------
    csi: The CSI matrix
    """
    timestamp_idx = 1
    num_tones_idx = 8
    row_idx = 9
    col_idx = 10
    csi_idx = 18

    timestamp = row[timestamp_idx]
    num_tones = row[num_tones_idx]
    num_rows = row[row_idx]
    num_cols = row[col_idx]
    csi_info = row[csi_idx]
    res, amp_results, unwrapped_phase_results, phase_results = process_csi(num_rows, num_cols, num_tones, csi_info)
    if count == 50:
        plot_amps(amp_results, timestamp, filter_none, "")
        plot_phases(unwrapped_phase_results, timestamp, filter_none, "u")
        plot_phases(phase_results, timestamp, filter_none, "")
        plot_phases(unwrapped_phase_results, timestamp, lambda x: uniform_filter(medfilt(x, [5]), 5), "uni_med")
        plot_phases(unwrapped_phase_results, timestamp, lambda x: linear_fitting(uniform_filter(medfilt(x, [5]), 5)), "linear_uni_med")
        plot_phases(unwrapped_phase_results, timestamp, linear_fitting, "u_linear")

    return res

def filter_none(values):
    return values

def linear_fitting(phases):
    F = len(phases)
    a1 = (phases[-1] - phases[0]) / (2 * np.pi * F)
    a0 = 1 / F * np.sum(phases)
    f = np.arange(F)
    linear_fitted_phases = phases - ((a1 * f) + a0)
    return linear_fitted_phases

#https://github.com/Retsediv/WIFI_CSI_based_HAR/blob/master/data_retrieval/run_visualization_server.py
def plot_phases(phases, timestamp: int, filter, postfix: str = "") -> None:
    for _, phase in enumerate(phases):
        phase = filter(phase)
        plt.plot(phase)
    f_name = sys.argv[1].split("_")[0]

    figname = f_name + "_" + "phase" + str(timestamp) + postfix + ".png"
    plt.xlabel("Subcarrier Index")
    plt.ylabel("Phases")
    plt.savefig(figname)   
    plt.cla()
    plt.close('all')

def plot_amps(amps, timestamp: int, filter, postfix: str = "") -> None:
    for _, amp in enumerate(amps):
        amp = filter(amp)
        plt.plot(amp)
    f_name = sys.argv[1].split("_")[0]

    figname = f_name + "_" + "amp" + str(timestamp) + postfix + ".png"
    plt.xlabel("Subcarrier Index")
    plt.ylabel("Amplitudes")
    plt.savefig(figname)   
    plt.cla()
    plt.close('all')
        
def process_csi(rows: int, cols: int, num_tones: int, csi_str: str) -> np.ndarray:
    """
    Converts a CSI string to a matrix 
    Example: "20+-30i 50+30i ..." -> np.ndarray[num_rows][num_cols][num_tones][1]
    """
    csi_mat = np.empty([rows, cols, num_tones, 2], dtype = 'float')
    semi_split = csi_str.split("; ")
    amp_results = []
    phase_results = []
    phase_unwrapped_results = []
    for _, bar_split in enumerate(semi_split):
        bar_split = bar_split.split("| ")
        for _, complex_nums in enumerate(bar_split):
            complex_nums = complex_nums.split(" ")

            # Offset the CSI, there's a chance that the split on " " causes an extra element
            complex_nums = complex_nums[len(complex_nums) - num_tones:]
            complex_nums = np.array(list(map(complex_converter, complex_nums)))
            amps = get_amp(complex_nums)
            phases = get_phase(complex_nums, False)
            unwrapped_phases = get_phase(complex_nums)

            amp_results.append(amps)
            phase_results.append(phases)
            phase_unwrapped_results.append(unwrapped_phases)

    # results = np.array(results).reshape((rows, cols, num_tones))
    reshaped_amp_results = np.array(amp_results).reshape((rows, cols, num_tones))
    reshaped_phase_results = np.array(phase_unwrapped_results).reshape((rows, cols, num_tones))

    csi_mat[:, :, :, 0] = reshaped_amp_results
    csi_mat[:, :, :, 1] = reshaped_phase_results
    return csi_mat, amp_results, phase_unwrapped_results, phase_results
 
def get_amp(complex_num) -> float:
    """
    Converts a complex number to amplitude
    Example: -56. -6.j -> 56.
    """
    imag = np.imag(complex_num)
    real = np.real(complex_num)
    result = np.sqrt(np.power(real, 2), np.power(imag, 2))
    return result

def get_phase(complex_num, unwrap = True) -> float:
    """
    Converts a complex number to the phase
    Example: -5.-49.j -> -1.67248518
    """
    imag = np.imag(complex_num)
    real = np.real(complex_num)
    result = np.arctan2(imag, real)
    if unwrap:
        result = np.unwrap(result)
    return result

def print_shapes(results: list[np.ndarray]) -> None:
    print("SHAPES: ")
    for row in results:
      print(row.shape)

def main(path: str) -> None:
    df = pd.read_csv(path)
    df = df.to_numpy()
    results = process_csv(df)
    print(f"Total rows successfully parsed: {len(results)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 csv_csi_parser.py <csv_file>")
        sys.exit(1)
    csv_path = sys.argv[1]
    main(csv_path)
