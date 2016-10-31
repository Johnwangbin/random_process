#coding:utf-8
import time
from possion_manager import NegativeExponentialDist, depend_direction
from two_list_contruct import two_list_merge

# 货车走完公路的时间，让每条公路长度相同。
reach_time = 2


class LogisticsHouse(object):
    def __init__(self, left_house, right_house, rate):
        self.queue_system = None
        self.to_left_house = []
        self.to_right_house = []
        self.to_local_truck_left = left_house.to_right_house
        self.to_local_truck_right = right_house.to_left_house
        self.to_local_stream = []
        self.rate = rate

    def initial_queue_system(self, p_lambda, p_miu, n, worker_num):
        self.queue_system = QueueSystem(p_lambda, p_miu, n, worker_num)

    def generate_two_output_streams(self):
        for point in self.queue_system.output_stream:
            if depend_direction(self.rate):
                self.to_left_house.append(point)
            else:
                self.to_right_house.append(point)

    def generate_to_local_truck_stream(self):
        self.to_local_stream.extend(self.to_local_truck_left)
        self.to_local_stream.extend(self.to_local_truck_right)
        self.to_local_stream.sort()


class QueueSystem(object):
    def __init__(self, p_lambda, p_miu, n, worker_num):
        self.servers_intervals = []
        self.service_streams_current_index = [0] * 3
        self.truck_stream       = []
        self.service_streams    = []
        self.waited_truck       = []
        self.truck_reach_time   = []
        self.worker_num = worker_num
        self.waited_num = 0
        self.waited_num_stream  = []
        self.truck_amount       = n
        self.output_stream      = []
        self.truck_dist = NegativeExponentialDist(p_lambda)
        self.service_dist = NegativeExponentialDist(p_miu)
        self.initial()

    def initial(self):
        point = 0.0 + reach_time

        for i in range(self.worker_num):
            self.servers_intervals.append([(point, point)])

        self.truck_stream = list(self.truck_dist.produce_mass_random_num(self.truck_amount))
        for interval in self.truck_stream:
            point = point + interval
            self.truck_reach_time.append(point)

        self.service_streams = []
        for i in range(self.worker_num):
            self.service_streams.append(list(self.service_dist.produce_mass_random_num(self.truck_amount / 3)))

    def server_first_finished(self):
        finished_time = []
        for server_intervals in self.servers_intervals:
            finished_time.append(server_intervals[-1][1])
        min_time = 0.0
        min_index = 0
        for i, point in enumerate(finished_time):
            if point < min_time:
                min_time = point
                min_index = i
        return min_index, min_time

    def add_truck_service_interval(self, server_num, start_time):
        print self.service_streams_current_index[server_num]
        self.servers_intervals[server_num].append((start_time, start_time + self.service_streams[server_num][
            self.service_streams_current_index[server_num]]))
        self.service_streams_current_index[server_num] += 1

    def generate_service_completed_time(self):
        for point in self.truck_reach_time:
            min_index, min_time = self.server_first_finished()
            if min_time >= point:
                self.add_truck_service_interval(min_index, min_time)
            else:
                self.add_truck_service_interval(min_index, point)

    def generate_output_stream(self):
        for server_intervals in self.servers_intervals:
            self.output_stream.extend([server_interval[1] for server_interval in server_intervals])
        self.output_stream.sort()

    def generate_waited_length_stream(self):
        stream = two_list_merge("input", "output", self.truck_stream, self.output_stream)
        for tag, point in stream:
            if tag == "input":
                self.waited_num += 1
            elif tag == "output":
                self.waited_num -= 1
            self.waited_num_stream.append((point, self.waited_num))


def test_queue_system():
    queue_system = QueueSystem(2, 2, 9999, 3)
    queue_system.generate_service_completed_time()
    print queue_system.servers_intervals
    # queue_system.generate_output_stream()
    # queue_system.generate_waited_length_stream()

if __name__ == "__main__":
    test_queue_system()
