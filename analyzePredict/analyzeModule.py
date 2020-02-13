def play_mod():
    print('module works')
    
### START FUNCTION
def five_num_summary(items):
    items.sort()
    new_items1 = []
    new_items2 = []
    if len(items) % 2 != 0:
        median = items[len(items)//2]
        new_items1 = items[0:items.index(median)]
        new_items2 = items[items.index(median)+1:]
        q1 = (new_items1[len(new_items1)//2] + new_items1[len(new_items1)//2 - 1]) / 2
        q3 = (new_items2[len(new_items2)//2] + new_items2[len(new_items2)//2 - 1]) / 2
        
    elif len(items) % 2 == 0:
        median = (items[len(items)//2] + items[len(items)//2 - 1]) / 2
        new_items1 = items[0:int(len(items)/2)]
        new_items2 = items[int(len(items)/2):]
        q1 = (new_items1[len(new_items1)//2] + new_items1[len(new_items1)//2 - 1]) / 2
        q3 = (new_items2[len(new_items2)//2] + new_items2[len(new_items2)//2 - 1]) / 2
       
    
    summary = {"max": max(items),"median": round(median,2),"min": min(items), "q1": round(q1,2),"q3": round(q3,2)}
    return summary
    

### END FUNCTION

### START FUNCTION
def five_num_summary(items):
    summary_dict = {}
    summary = np.quantile(items,[1, 0.5, 0, 0.25, 0.75])
    list1 = ["max","median","min","q1","q3"]
    for i in range(len(list1)):
        summary_dict[list1[i]] = summary[i]
                                 
    return summary_dict

### END FUNCTION


### START FUNCTION
def five_num_summary(items):
    summary_dict = {}                                         # initialise an empty dictionary
    summary = np.quantile(items,[1, 0.5, 0, 0.25, 0.75])      
    list1 = ["max","median","min","q1","q3"]                  # create labels for the outputs
    for i in range(len(list1)):
        summary_dict[list1[i]] = summary[i]
                                 
    return summary_dict

### END FUNCTION