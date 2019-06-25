'''
 use the Travelling Salesman algorithm DP
 Time Complexity: O(n^2 * 2^n)
 Space Complexity: O(n * 2^n)
'''


import json

class CarBookingOrderSolver:

    class CarBooking:
        def __init__(self, id, start, end, label):
            self.id = id
            self.start_location = start
            self.end_location = end
            self.label = label

    def __init__(self):
        # variables for car booking info
        self.car_bookings = []
        self.car_booking_label_map = {}
        self.distance_matrix_size = 0
        self.distance_matrix = []

        # variables for dp
        self.dp_memo = []
        self.min_cost_prev_index = []


    def solve(self, file_path):
        # setup necessary variables before starting to solve problem
        self._setup(file_path)
        self._solve()
        return self

    def get_cost(self):
        return self.dp_memo[0][1]

    def get_booking_order(self):
        path = []
        pointer = 0
        state = 1
        while pointer != self.distance_matrix_size:
            next_pointer = self.min_cost_prev_index[pointer][state]
            if next_pointer == -1:
                break
            state = state | (1 << next_pointer)
            # need to convert the next_pointer to booking id, since we are using a label when creating the distance matrices
            # we also skipped the first city since that is our sentinel node that doesn't need to be included in the path
            path.append(self.car_booking_label_map[next_pointer].id)
            pointer = next_pointer
        return path

    def _setup(self, file_path):
        self._parse_file_to_booking(file_path)
        self._setup_distance_matrix()
        self._setup_dp()

    def _parse_file_to_booking(self, file_path):
        f = open(file_path, "r")
        json_array = json.load(f)
        id_label = 1
        for data in json_array:
            car_booking = CarBookingOrderSolver.CarBooking(data['id'], data['start'], data['end'], id_label)
            self.car_booking_label_map[id_label] = car_booking
            self.car_bookings.append(car_booking)
            id_label += 1

    def _setup_distance_matrix(self):
        # use +1 for sentinel node as our starting city
        self.distance_matrix_size = len(self.car_bookings) + 1
        self.distance_matrix = [[0] * self.distance_matrix_size for _ in range(0, self.distance_matrix_size)]
        self.distance_matrix[0][0] = -1

        # setup distance matrices(this represent the relocation costs)
        for elem in self.car_bookings:
            for elem2 in self.car_bookings:
                if elem == elem2:
                    self.distance_matrix[elem.label][elem.label] = -1
                elif elem.end_location != elem2.start_location:
                    self.distance_matrix[elem.label][elem2.label] = 1

    def _setup_dp(self):
        # setup memoization matrix
        # use bit flag as a way to identify whether nodes are already visited or not (can also use boolean arrays)
        number_of_possible_states = (1 << self.distance_matrix_size)

        # DP arrays
        # used for caching results
        self.dp_memo = [[-1] * number_of_possible_states for _ in range(0, self.distance_matrix_size)]

        # used for remembering the previous node which has the best result in get_path
        self.min_cost_prev_index = [[-1] * number_of_possible_states for _ in range(0, self.distance_matrix_size)]

    def _solve(self):
        current_node = 0
        current_visited_state = 1
        self._dp(current_node, current_visited_state)

    def _dp(self, current_node, current_visited_state):
        # the current city state has been calculated previously
        if self.dp_memo[current_node][current_visited_state] != -1:
            return self.dp_memo[current_node][current_visited_state]

        # all cities has been visited return 0
        if current_visited_state == ((1 << (len(self.distance_matrix))) - 1):
            return 0

        min_cost = 9999999999
        best_prev_index = -1
        for next_node in range(0, len(self.distance_matrix)):
            # only recurse down the path if it has not been visited before
            if (((1 << next_node) & current_visited_state) == 0):
                next_visited_state = current_visited_state | (1 << next_node)
                cost = self._dp(next_node, next_visited_state) + self.distance_matrix[current_node][next_node]
                if (cost < min_cost):
                    min_cost = cost
                    best_prev_index = next_node

        # cache off the best result for current node and state
        self.dp_memo[current_node][current_visited_state] = min_cost
        self.min_cost_prev_index[current_node][current_visited_state] = best_prev_index
        return min_cost

def main():
    input_file_path = raw_input("Enter json file name containing booking orders (use data.json for default data):")
    output_file_path = raw_input("Enter output json file: ")
    cb = CarBookingOrderSolver()
    cb.solve(input_file_path)
    print("minimum relocation cost is: ", cb.get_cost())
    print("The optimum order is: ", cb.get_booking_order())
    with open(output_file_path, 'wb') as outfile:
        json.dump(cb.get_booking_order(), outfile)


if __name__== "__main__":
    main()


