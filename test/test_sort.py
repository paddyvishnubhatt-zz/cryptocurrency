
def sort(input):
    output = []
    #for each req combo
    for c_item in input:

        # split the reqs
        i_item = c_item.split("_")[0]
        o_item = c_item.split("_")[1]
        # if req is first get inside, else continue
        if c_item.startswith(i_item):
            # if req already in list
            if i_item in output:
                # if other req is also in list
                if o_item in output:
                    # check for both already in list
                    i_idx = output.index(i_item)
                    o_idx = output.index(o_item)
                    if i_idx <= o_idx:
                        #swap
                        output[i_idx] = o_item
                        output[o_idx] = i_item
                #second item is not in list - so add
                else:
                    # add
                    output.append(o_item)
            # first item not in list - so add
            else:
                # add
                output.append(i_item)

    print output

if __name__ == "__main__":
    baseline = ['r1','r2','r3']
    #input:
    #r1_r2
    #r1_r3
    #r3_r2
    input = ['r1_r2', 'r3_r1', 'r2_r3']
    #output:
    #r1,r3,r2
    sort(input)