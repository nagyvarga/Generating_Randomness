MIN_LENGTH = 100
APPROPRIATE_SYMBOLS = ('0', '1')
all_filtered_text = ''
triads = {}
capital = 1000


def filter_text(text):
    filtered_text = [character for character in text if character in APPROPRIATE_SYMBOLS]
    return ''.join(filtered_text)


def prediction(random_text):
    predicted_string = random_text[:3]
    test_length = len(random_text)
    for j in range(test_length - 3):
        last_three_chars = random_text[j:3 + j]
        if triads[last_three_chars][0] >= triads[last_three_chars][1]:
            appended_char = '0'
        else:
            appended_char = '1'
        predicted_string += appended_char
    return predicted_string


def prediction_probability(cut_random_text, cut_predicted_string):
    number_of_same_chars = 0
    cut_test_length = len(cut_random_text)
    for j in range(cut_test_length):
        if cut_random_text[j] == cut_predicted_string[j]:
            number_of_same_chars += 1
    return [number_of_same_chars, cut_test_length]


def update_triads(text):
    for i in range(len(text) - 3):
        triad_key = text[i:i + 3]
        after_triad = text[i + 3]

        if after_triad == '0':
            actual_triad = {triad_key: [triads.get(triad_key, [0, 0])[0] + 1, triads.get(triad_key, [0, 0])[1]]}
        else:
            actual_triad = {triad_key: [triads.get(triad_key, [0, 0])[0], triads.get(triad_key, [0, 0])[1] + 1]}
        triads.update(actual_triad)


print('\nPlease give AI some data to learn...\nThe current data length is 0, 100 symbols left')

while True:
    user_input = input('Print a random string containing 0 or 1:\n\n')
    all_filtered_text += filter_text(user_input)
    all_text_length = len(all_filtered_text)

    if all_text_length >= MIN_LENGTH:
        print(f'\nFinal data string:\n{all_filtered_text}\n')
        break
    else:
        left_symbols = MIN_LENGTH - all_text_length
        print(f'Current data length is {all_text_length}, {left_symbols}')

update_triads(all_filtered_text)
sorted_triads_keys = list(triads.keys())
sorted_triads_keys.sort()

# for triad_key in sorted_triads_keys:
#     print(f'{triad_key}: {triads[triad_key][0]},{triads[triad_key][1]}')

print('You have $1000. Every time the system successfully predicts your next press, you lose $1. '
      'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')

while True:
    print('\nPrint a random string containing 0 or 1:')
    random_string = input()
    if random_string == 'enough':
        break
    filtered_random_string = filter_text(random_string)
    if len(filtered_random_string) > 3:
        predicted_text = prediction(filtered_random_string)
        print("prediction:")
        print(predicted_text)
        random_string_probability = prediction_probability(filtered_random_string[3:], predicted_text[3:])
        random_string_probability_percent = round(100 * random_string_probability[0] / random_string_probability[1], 2)
        print(f'\nComputer guessed right {random_string_probability[0]} out of {random_string_probability[1]} symbols '
              f'({random_string_probability_percent} %)')
        capital += random_string_probability[1] - 2 * random_string_probability[0]
        print(f'Your capital is now ${capital}')
        update_triads(filtered_random_string)

print('Game over!')
