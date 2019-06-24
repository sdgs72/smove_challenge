'''
 use the Travelling Salesman algortihm DP
 Time Complexity: O(n^2 * 2^n)
 Space Complexity: O(n * 2^n)
'''


import json

class CarBooking:
    def __init__(self, id, start, end, label):
        self.id = id
        self.start_location = start
        self.end_location = end
        self.label = label
        
def main():
    file_path = raw_input("Enter json file name containing booking orders (use data.json for default data):")
    f = open(file_path,"r")
    json_array = json.load(f)

    car_bookings = []
    id_label = 1
    car_booking_label_map = {}
    for data in json_array:
        car_booking = CarBooking(data['id'], data['start'], data['end'], id_label)
        car_booking_label_map[id_label] = car_booking
        car_bookings.append(car_booking)
        id_label += 1

    # use +1 for sentinel node as our starting city
    distance_matrix_size = len(car_bookings)+1
    distance_matrix = [[0]* distance_matrix_size for _ in range(0,distance_matrix_size)]
    distance_matrix[0][0] = -1

    # setup matrix
    for elem in car_bookings:
        for elem2 in car_bookings:
            if elem == elem2:
                distance_matrix[elem.label][elem.label] = -1
            elif elem.end_location != elem2.start_location:
                distance_matrix[elem.label][elem2.label] = 1

    # setup memoization matrix
    # use bit flag as a way to identify whether nodes are already visited or not (can also use boolean arrays)
    current_visited_state = 1
    number_of_possible_states = (1 << distance_matrix_size)

    # DP arrays
    # used for caching results
    dp_memo = [[-1] * number_of_possible_states for _ in range(0, distance_matrix_size)]
    # used for remembering the previous node which has the best result
    min_cost_prev_index = [[-1] * number_of_possible_states for _ in range(0, distance_matrix_size)]
    min_cost = tsp_dp(0, distance_matrix, dp_memo, current_visited_state, min_cost_prev_index)
    print("minimum relocation cost is: ", min_cost)
    optimum_order = rebuild_path(distance_matrix_size, car_booking_label_map, min_cost_prev_index)
    print("The optimum order is: ", optimum_order)


def tsp_dp(current_node, distance_matrix, memo, current_visited_state, min_cost_prev_index):

    # the current city state has been calculated previously
    if memo[current_node][current_visited_state] != -1:
        return memo[current_node][current_visited_state]

    # all cities has been visited return 0
    if current_visited_state == ((1 << (len(distance_matrix))) - 1):
        return 0
    
    min_cost = 9999999999
    best_prev_index = -1
    for next_node in range(0,len(distance_matrix)):
        # only recurse down the path if it has not been visited before
        if( ((1 << next_node) & current_visited_state) == 0):
            next_visited_state = current_visited_state | (1 << next_node)
            cost = tsp_dp(next_node, distance_matrix, memo, next_visited_state, min_cost_prev_index) + distance_matrix[current_node][next_node]
            if(cost < min_cost):
                min_cost = cost
                best_prev_index = next_node

    # cache off the best result for current node and state
    memo[current_node][current_visited_state] = min_cost
    min_cost_prev_index[current_node][current_visited_state] = best_prev_index
    return min_cost

def rebuild_path(distance_matrix_size, car_booking_label_map, min_cost_prev_index):
    path = []
    pointer = 0
    state = 1
    while pointer != distance_matrix_size:
        next_pointer = min_cost_prev_index[pointer][state]
        if next_pointer == -1:
            break
        state = state | (1 << next_pointer)
        # need to convert the next_pointer to booking id, since we are using a label when creating the distance matrices
        # we also skipped the first city since that is our sentinel node that doesn't need to be included in the path
        path.append(car_booking_label_map[next_pointer].id)
        pointer = next_pointer
    return path



if __name__== "__main__":
    main()


