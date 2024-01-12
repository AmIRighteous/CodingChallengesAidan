"""
    1. Sketch out the vision - what is the application going to do at a high level.
    -general sort that just sorts lexicographically via opening a file & dumping to STDOUT
    - -u removes all duplicate lines in the file (maybe have a set that holds all the words that exist, as well as a list?)
    - -[radix/merge/quick/heap]-sort or -sort=[radix/merge/quick/heap]
    - R or -random-sort or -sort=random for random sorting

    2. Break down the application into building blocks
    -CLI parser obvy
    -flag

    3. Build the core of one or more of the fundamental blocks using test driven development.

    4. Build a walking skeleton - once I’ve built any fundamental blocks, I like to build a walking skeleton.
    A walking skeleton is a tiny implementation of a system that performs a very small end-to-end function.

    5. Flesh out the functionality - Once I have a walking skeleton I start to add flesh to it. Adding more end-to-end slices of functionality by writing tests and then the code to pass them, for the minimum functionality I will need for each block, to deliver the end-to-end slice. Repeat until all the functionality is there.

    6. Refactor - This isn’t really step 6, I tend to refactor as I go.
    As the software evolves I will have to change things that were done to enable the development of a walking skeleton
"""


if __name__ == '__main__':
    print("Hello! World!!")