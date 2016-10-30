#coding:utf-8
import time
from possion_manager import expntl
import threading

# 货车走完公路的时间，让每条公路长度相同。
reach_time = 2

class LogisticsHouse(object):
    def __init__(self, logistics_house_left, logistics_house_right):
        self.from_local_truck = []
        self.to_local_truck = []
        self.rate = []
        self.to_local_truck_left = logistics_house_left.to_local_truck
        self.to_local_truck_right = logistics_house_right.to_local_truck
        self.waited = 0
        self.worker_num = 0
        self.p_lambda = 0.0
        self.p_miu    = 0.0

