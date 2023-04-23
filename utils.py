# some utility functions here 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 

# This function checks if the input string is numeric or not
def isnumeric(x):
    try:
        x = int(x)
        return True 
    except:
        return False 

# This function will sort the dictionary by key
def sort_dictionary_by_key(input_dict):
    return {k: input_dict[k] for k in sorted(input_dict.keys())}
    
# This function will return probability distribution of first significant digit for the given dataset file
def get_data_distribution(filepath):
    # read csv
    df = pd.read_csv(filepath)
    # get the leading digit of all rows
    df['leading_digit'] = df.iloc[:,0].apply(lambda x:str(x)[0])
    # get value counts for each digit
    leading_digits_count = df['leading_digit'].value_counts()
    # convert to dictionary
    leading_digits_dict = leading_digits_count.to_dict()
    # filter out the non numeric values and 0
    filtered_dict = {}
    for k in leading_digits_dict:
        if isnumeric(k):
            if int(k) > 0:
                filtered_dict[k] = leading_digits_dict[k]
    # calculate probability distribution
    probability_dict = {k: filtered_dict[k]/sum(filtered_dict.values()) for k in filtered_dict.keys()}
    # sort the dictionary for plotting
    sorted_dict = sort_dictionary_by_key(probability_dict)
    # plot bar graph for each digit and their frequency
    fig = plt.figure(figsize=(10,5))
    plt.bar(sorted_dict.keys(),sorted_dict.values())
    plt.xlabel("Leading Digits")
    plt.ylabel("Probability")
    plt.title("Probability distribution of first significant digit")
    plt.savefig("static/result_img.png")
    # return the observed distribution
    return probability_dict

def check_benford_law(filepath):
    benford_distribution = {str(k): np.log10(1+(1/k)) for k in range(1,10)}
    observed_distribution = get_data_distribution(filepath)
    
    # Here I have considered 2 methods for checking for Benford's law. In the first method I will compare the order of observed distribution with order of benford's distribution. If order is same it follows the law, but if the order is not same I will check if the most frequent first digit is 1 or not, if it is 1 then also Benford's law is true. In the 2nd method, I have tried using the absolute deviation between the numbers and checking if it is within the limit or not. I have commented out the 2nd method and used the 1st method.
    
    # checking key order
    benford_key_order = list(benford_distribution.keys()) 
    observed_key_order = list(observed_distribution.keys())
    # if both have same order most probably it follows the law
    if benford_key_order == observed_key_order:
        return True 
    else:
        # checking if the highest value is of 1 or not
        observed_max_key = max(observed_distribution,key=observed_distribution.get)
        benford_max_key = max(benford_distribution,key=benford_distribution.get)
        return True if observed_max_key == benford_max_key else False
    
    # checking if the absolute deviation between numbers is within limit
    # limit = 0.05
    # ans = True
    # differences = {}
    # for k in benford_distribution.keys():
    #     differences[k] = abs(benford_distribution[k] - observed_distribution[k])
    #     if differences[k] > limit:
    #         ans = False 
    
    # print(differences)
    # return ans
    