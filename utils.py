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
    # Theoretical Benford distribution using formula
    benford_distribution = {str(k): np.log10(1+(1/k)) for k in range(1,10)}
    # Observed data distribution for the input dataset
    observed_distribution = get_data_distribution(filepath)
    
    # Method 1: Compare order and most frequent key in both distirbution
    # checking key order
    # benford_key_order = list(benford_distribution.keys()) 
    # observed_key_order = list(observed_distribution.keys())
    # # if both have same order most probably it follows the law
    # if benford_key_order == observed_key_order:
    #     return True 
    # else:
    #     # checking if the highest value is of 1 or not
    #     observed_max_key = max(observed_distribution,key=observed_distribution.get)
    #     benford_max_key = max(benford_distribution,key=benford_distribution.get)
    #     return True if observed_max_key == benford_max_key else False
    
    # Method 2: Absolute deviation method
    # checking if the absolute deviation between numbers is within limit
    limit = 0.05
    ans = True
    differences = {}
    for k in benford_distribution.keys():
        differences[k] = abs(benford_distribution[k] - observed_distribution[k])
        # check if the absolute deviation for all digits is less than limit or not
        # if differences[k] > limit:
        #     ans = False 
    # Alternatively, we can find the max of all deviations and check if the maximum deviation is greater than set limit or not. Here I am excluding the deviations of first two digits i-e 1 and 2 as they can have more deviation compared to other digits, but in later digits like 7,8,9 the deviation shouldn't exceed 0.5 to conform to Benford's law
    max_deviation = max(list(differences.values())[2:])
    if max_deviation > limit:
        print(f"Max Deviation: {max_deviation}")
        ans = False
    return ans
    