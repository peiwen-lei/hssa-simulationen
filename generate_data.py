from bays import *
import pandas as pd
import os
import time


# Calculate the sum of extra movements when putting all containers into the bay
def calc_extra_moves(bay, sequence):
    input_containers = sequence.get_iterator(bay)
    extra_move_sum = 0
    for container in input_containers:
        extra_move_sum += bay.put(container)
    return extra_move_sum


# Calculate the sum of rehandling when retrieving all containers from the bay
def calc_rehandling(bay, sequence):
    output_containers = sequence.get_iterator(bay)
    rehandling_sum = 0
    for container in output_containers:
        rehandling_sum += bay.take(container.weight)
    return rehandling_sum


# Define the height and width of the bay
HEIGHTS = [4, 5, 6]
WIDTHS = [6, 7, 8]

SAMPLE_COUNT = 30000

for w in WIDTHS:
    for h in HEIGHTS:

        print('Generating data for height {0}, width {1}, sampling size {2}'.format(h, w, SAMPLE_COUNT))
        exec_start = time.time()

        extra_moves = {
            'vertical_bay': [],
            'hybrid_bay': [],
            'hybrid_left_bay': [],
            'hybrid_right_bay': [],
            'width': [w] * SAMPLE_COUNT,
            'height': [h] * SAMPLE_COUNT
        }

        rehandling = {
            'random_bay': [],
            'vertical_bay': [],
            'hybrid_bay': [],
            'hybrid_left_bay': [],
            'hybrid_right_bay': [],
            'width': [w] * SAMPLE_COUNT,
            'height': [h] * SAMPLE_COUNT
        }

        for _ in range(SAMPLE_COUNT):
            hybrid_bay = HybridBay(w, h)
            hybrid_right_bay = HybridRightBay(w, h)
            hybrid_left_bay = HybridLeftBay(w, h)
            vertical_bay = VerticalBay(w, h)
            random_bay = RandomBay(w, h)

            input_sequence = ContainerGenerator(w * h, True)
            output_sequence = ContainerGenerator(w * h, False)

            # Calculate statistics related to hybrid bay
            extra_moves['hybrid_bay'].append(calc_extra_moves(hybrid_bay, input_sequence))
            rehandling['hybrid_bay'].append(calc_rehandling(hybrid_bay, output_sequence))

            # Calculate statistics related to hybrid left bay
            extra_moves['hybrid_left_bay'].append(calc_extra_moves(hybrid_left_bay, input_sequence))
            rehandling['hybrid_left_bay'].append(calc_rehandling(hybrid_left_bay, output_sequence))

            # Calculate statistics related to hybrid right bay
            extra_moves['hybrid_right_bay'].append(calc_extra_moves(hybrid_right_bay, input_sequence))
            rehandling['hybrid_right_bay'].append(calc_rehandling(hybrid_right_bay, output_sequence))

            # Calculate statistics related to vertical bay
            extra_moves['vertical_bay'].append(calc_extra_moves(vertical_bay, input_sequence))
            rehandling['vertical_bay'].append(calc_rehandling(vertical_bay, output_sequence))

            # Calculate statistics related to random bay
            calc_extra_moves(random_bay, input_sequence)
            rehandling['random_bay'].append(calc_rehandling(random_bay, output_sequence))

        exec_end = time.time()
        print('Calculation takes {0:0.2f} seconds to finish'.format(exec_end - exec_start))

        extra_moves_df = pd.DataFrame(extra_moves)
        rehandling_df = pd.DataFrame(rehandling)

        directory = "./data/w{0}_h{1}_s{2}".format(w, h, SAMPLE_COUNT)
        if not os.path.exists(directory):
            os.mkdir(directory)
        extra_moves_df.to_csv(directory + "/extra_move.csv", index=False)
        rehandling_df.to_csv(directory + "/rehandling.csv", index=False)
