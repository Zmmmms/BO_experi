
import numpy as np
import pandas as pd

def hurst(ts):
    ts = list(ts)
    N = len(ts)
    if N < 20:
        raise ValueError("Time series is too short! input series ought to have at least 20 samples!")

    max_k = int(np.floor(N/2))
    R_S_dict = []
    for k in range(10,max_k+1):
        R,S = 0,0
        # split ts into subsets
        subset_list = [ts[i:i+k] for i in range(0,N,k)]
        if np.mod(N,k)>0:
            subset_list.pop()
            #tail = subset_list.pop()
            #subset_list[-1].extend(tail)
        # calc mean of every subset
        mean_list=[np.mean(x) for x in subset_list]
        for i in range(len(subset_list)):
            cumsum_list = pd.Series(subset_list[i]-mean_list[i]).cumsum()
            R += max(cumsum_list)-min(cumsum_list)
            S += np.std(subset_list[i])
        R_S_dict.append({"R":R/len(subset_list),"S":S/len(subset_list),"n":k})
    
    log_R_S = []
    log_n = []
    
    # print(R_S_dict)


    for i in range(len(R_S_dict)):
        R_S = (R_S_dict[i]["R"]+np.spacing(1)) / (R_S_dict[i]["S"]+np.spacing(1))
        log_R_S.append(np.log10(R_S))
        log_n.append(np.log10(R_S_dict[i]["n"]))

    Hurst_exponent, b = np.polyfit(log_n,log_R_S,1)
    return Hurst_exponent, b, log_n, log_R_S



def ehurst( ts):
    ts = list(ts)
    N = len(ts)
    if N < 20:
        raise ValueError("Time series is too short! input series ought to have at least 20 samples!")

    max_k = N

    ERS_dics = list()

    for k in range(2,max_k+1):
        n = k
        item = 0
        for r in range(1, n): item += np.sqrt( (n-r)/r )
        ersn = ((n-0.5)/ (n*np.sqrt(np.pi*n/2))) * item

        ERS_dics.append({
            "ersn": ersn,
            "n": n
        })
    
    log_n = []
    log_ers = []
    for dic in ERS_dics:
        log_ers.append( np.log10(dic['ersn']) )
        log_n.append( np.log10(dic['n']) )
    
    print( 'fitting...')
    EH, b = np.polyfit( log_n, log_ers, 1)
    return EH, b, log_n, log_ers