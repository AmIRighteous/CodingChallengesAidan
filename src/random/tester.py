# def do_thing(A: list[int]):
#     possible_sums = set()
#     for i in range(1, len(A)):
#         possible_sums.add(A[i] + A[i - 1])
#     output = {num: 0 for num in possible_sums}
#     for curr in possible_sums:
#         i = 1
#         while i < len(A):
#             if A[i] + A[i - 1] == curr:
#                 output[curr] += 1
#                 i += 2
#             else:
#                 i += 1
#     return max(output.values())

# def gsg_func(s: str) -> dict[str]:
#     substrings = [s[i:j] for i in range(len(s)) for j in range(i+1, len(s)+1)]
#     output = {k: substrings.count(k) for k in set(substrings)}
#     return output
#


def gsg_func(s: str) -> dict[str]:
    occ_by_substr = {}
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            prime = s[i:j]
            print("prime = ", prime)
            if prime in occ_by_substr:
                occ_by_substr[prime] += 1
            else:
                occ_by_substr[prime] = 1
    return occ_by_substr


if __name__ == "__main__":
    # print(do_thing([10, 1, 3, 1, 2, 2, 1, 0, 4]))
    # print(do_thing([5, 3, 1, 3, 2, 3]))
    # print(do_thing([9, 9, 9, 9]))
    # print(do_thing([1, 5, 2, 4, 3, 3]))
    print("Hello worlddd")
    # print(gsg_func("bbbbb"))
    print(gsg_func("abcdef"))
    # print(gsg_func("abababa"))
