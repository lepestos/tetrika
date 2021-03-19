from typing import Dict, List


def intervals_union(array: List) -> List:
    """
    Given an array of intervals where lower bounds
    are placed, in ascending order return union
    of those intervals
    """
    # array = sum(sorted([[x, y] for x, y
    #                     in zip(array[::2], array[1::2])]), [])
    n = len(array) // 2
    if n <= 1:
        return array.copy()
    low = array[0]  # lower bound of the current interval
    high = array[1]  # upper bound of the current interval
    res = []
    for i in range(n):
        if array[2 * i] <= high:
            # expand the current interval
            high = max(high, array[2 * i + 1])
        else:
            # current interval does not intersect the i-th
            # interval, so we can simply add it to res
            res += [low, high]
            low, high = array[2 * i], array[2 * i + 1]
    # we never added the last interval, so we must do it now
    res += [low, high]
    return res


def appearance(intervals: Dict) -> int:
    """
    We are assuming that 'pupil' and 'tutor' lists
    are positioned in such a way that lower bounds of
    their respective intervals are in ascending order,
    which is in my opinion a fair assumption,
    considering the context of the task.
    Otherwise, we should sort them in
    'intervals union' function
    """
    start, end = intervals['lesson']
    pupil = intervals_union(intervals['pupil'])
    tutor = intervals_union(intervals['tutor'])
    # numbers of respective intervals
    n_pupil = len(pupil) // 2
    n_tutor = len(tutor) // 2
    i = j = 0
    res = 0
    # iterate over intervals
    while i < n_pupil and j < n_tutor:
        low = max(pupil[2 * i], tutor[2 * j], start)
        high = min(pupil[2 * i + 1], tutor[2 * j + 1], end)
        if low <= high:
            res += high - low
        # interval with the lowest high point is now irrelevant
        if pupil[2 * i + 1] >= tutor[2 * j + 1]:
            j += 1
        else:
            i += 1
    return res
