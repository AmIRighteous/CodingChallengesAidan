
def do_thing(A: list[int]):
    possible_sums = set()
    for i in range(1, len(A)):
        possible_sums.add(A[i] + A[i - 1])
    output = {num: 0 for num in possible_sums}
    for curr in possible_sums:
        i = 1
        while i < len(A):
            if A[i] + A[i - 1] == curr:
                output[curr] += 1
                i += 2
            else:
                i += 1
    return max(output.values())


if __name__ == '__main__':
    print(do_thing([10,1,3,1,2,2,1,0,4]))
    print(do_thing([5,3,1,3,2,3]))
    print(do_thing([9,9,9,9]))
    print(do_thing([1,5,2,4,3,3]))
