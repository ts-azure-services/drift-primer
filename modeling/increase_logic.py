# Test if it falls outside of the index, number is too large
# Test if it does negative routines


def integer_alignment(
        base_list=None,
        change_list=None,
        target=None,
        ):
    # Get the sum of the base and the list to change
    base_list_sum=sum(base_list)
    change_list_sum=sum(change_list)

    # Compare against the target, and iterate
    if base_list_sum == target:
        pass
    elif base_list_sum < target:
        # Then +1, for each list item
        i = 0
        while change_list_sum != target:
            # Keep iterating through if you come to the end of the list
            if i > len(change_list) - 1:
                i = 0
            else:
                change_list[i] = change_list[i] + 1
                change_list_sum = sum(change_list)
                i += 1
    else:
        # Then -1, for each list item
        i = 0
        while change_list_sum != target:
            if i > len(change_list) - 1:
                i = 0
            else:
                change_list[i] = change_list[i] - 1
                change_list_sum = sum(change_list)
                i += 1
    print(f'original list: {base_list}')
    print(f'new list: {change_list}')
    print(f'target: {target}')
    print(f'sum of original list: {base_list_sum}')
    print(f'sum of new list: {change_list_sum}')
    return base_list, change_list, base_list_sum, change_list_sum

sample_list = [1,2,3,4,5]
new_list = sample_list.copy()
target=150

base_list, change_list, base_list_sum, change_list_sum =\
        integer_alignment(
        base_list=sample_list,
        change_list=new_list,
        target= target,
        )
