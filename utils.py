# some utility functions here 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

def isnumeric(x):
    try:
        x = int(x)
        return True 
    except:
        return False 
    

def get_data_distribution(filepath):
    df = pd.read_csv(filepath)
    df['leading_digit'] = df.iloc[:,0].apply(lambda x:str(x)[0])
    leading_digits_count = df['leading_digit'].value_counts()
    leading_digits_dict = leading_digits_count.to_dict()
    filtered_dict = {}
    for k in leading_digits_dict:
        if isnumeric(k):
            if int(k) > 0:
                filtered_dict[k] = leading_digits_dict[k]
    probability_dict = {k: filtered_dict[k]/sum(filtered_dict.values()) for k in filtered_dict.keys()}
    fig = plt.figure(figsize=(10,5))
    plt.bar(probability_dict.keys(),probability_dict.values())
    plt.xlabel("Leading Digits")
    plt.ylabel("Probability")
    plt.title("Probability distribution of first significant digit")
    plt.savefig("data_distribution.png")
    plt.show()
    return probability_dict

def check_benford_law(filepath):
    benford_distribution = {str(k): np.log10(1+(1/k)) for k in range(1,10)}
    observed_distribution = get_data_distribution(filepath)
    
    # I think all these 3 methods are valid to check for Benford law so combining all 3 methods not sure if it is valid or not, should try chi square test
    
    # checking key order
    benford_key_order = list(benford_distribution.keys()) 
    observed_key_order = list(observed_distribution.keys())
    if benford_key_order == observed_key_order:
        return True 
    else:
        # checking if the highest value is of 1 or not
        observed_max_key = max(observed_distribution,key=observed_distribution.get)
        benford_max_key = max(benford_distribution,key=benford_distribution.get)
        return True if observed_max_key == benford_max_key else False
    
    # checking if the absolute deviation between numbers is within limit
    # limit = 0.02 
    # ans = True
    # differences = {}
    # for k in benford_distribution.keys():
    #     differences[k] = abs(benford_distribution[k] - observed_distribution[k])
    #     if differences[k] > limit:
    #         ans = False 
    
    # print(differences)
    # return ans
    