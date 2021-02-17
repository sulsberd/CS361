
arr = [[1, 22, 11, 2, 2, 3, 4, 55, 22]]



def merge_sort(array, flag=0):
    """Merge sort algorithm implementation."""
    if len(array) <= 1:  # base case
        return array

    if flag is 1:
        # divide array in half and merge sort recursively
        half = len(array) // 2
        left = merge_sort(array[:half], 1)
        right = merge_sort(array[half:], 1)

        return merge_reviews(left, right, 1)

    else:
    # divide array in half and merge sort recursively
        half = len(array) // 2
        left = merge_sort(array[:half])
        right = merge_sort(array[half:])

        return merge(left, right)

def merge_reviews(left, right, sort_number):
    """Merge sort merging function."""

    left_index, right_index = 0, 0
    result = []
    while left_index < len(left) and right_index < len(right):
        lefty = left[left_index]
        righty = right[right_index]

        left_first = lefty[5]
        right_first = righty[5]

        if left_first < right_first:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result += left[left_index:]
    result += right[right_index:]
    return result

result = merge_sort(arr, 1)
print(result)