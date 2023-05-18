import csv


def read_in_results_from_csv(file_name='game_turns.csv'):
    with open(file_name, 'rt') as f:
        csv_reader = csv.reader(f)
        counter = 0
        for row in csv_reader:
            if len(row) == 0:
                continue
            counter += 1
            temp = row
            # Break down the row into its components
            # Players
            for i in range(6):
                # print(f'Player {i} - {temp[:2]}')
                temp = temp[2:]
            # Superpowers
            for i in range(6):
                # print(f'Superpower {i} - {temp[:14]}')
                temp = temp[18:]
                # Bonds
                for j in range(9):
                    # print(f'Bond {j} for Superpower {i} - {temp[:8]}')
                    temp = temp[8:]

            # Territories
            for i in range(62):
                print(f'Territory {i} - {temp[:12]}')
                temp = temp[12:]

            print(temp)

            print(len(row))
            if counter > 10:
                break


if __name__ == '__main__':
    read_in_results_from_csv(file_name='../game_turns.csv')