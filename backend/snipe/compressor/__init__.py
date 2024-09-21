def build_gap_list(arr):
    alist = []

    if len(arr) > 0:
        alist.append(arr[0])

        for i in range(1, len(arr)):
            alist.append(arr[i] - arr[i - 1])

    return alist
