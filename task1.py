def task(array: str) -> int:
    """
    Time complexity is O(log n) where n = len(array),
    as function len(array) has O(1) time complexity,
    and we are running the 'while' cycle at most [log n] + 1 times,
    with each iteration taking O(1) time
    """

    low = 0
    high = len(array)
    if high == 0 or array[low] == '0' or array[high-1] == '1':
        return -1
    while low + 1 < high:
        mid = (low+high) // 2
        if array[mid] == '0':
            high = mid
        else:
            low = mid
    return high
