

if __name__ == '__main__':
    array1 = input('First set of scores: ')
    array2 = input('Second set of scores: ')
    array3 = input('Third set of scores: ')

    l1 = [i.strip() for i in array1.split(',')]
    l2 = [i.strip() for i in array2.split(',')]
    l3 = [i.strip() for i in array3.split(',')]

    for i in range(len(l1)):
        print(f'Game {i + 1} & {l1[i]} & {l2[i]} & {l3[i]} \\\\\n\\hline')

    print('Done')
