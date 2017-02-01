import os
import csv
import time
from subprocess import check_output
from subprocess import Popen
import httplib

LEITURA = 0
ESCRITA_E_LEITURA = 1

class TesterADSD(object):
    def __init__(self, rate, req_per_min, output=None, mode=LEITURA):
        self.rate = rate
        self.requests = req_per_min
        self.mode = mode
        self.output = output
        self.url = None

    def set_target(self, url):
        self.url = url

    def set_mode(self, mode):
        self.mode = mode

    def start(self):
        if not self.url:
            raise Exception("Target not set.")
        total_test_timei = time.time()
        if(self.requests == 10):
            self.paced_shooter(self.url, 1, self.requests, self.mode, 6) #10 requests per minute
        else:
            self.paced_shooter(self.url, 1, self.requests, self.mode, 0.24) #250 requests per minute
        print "Done!" + "Total test time: " + str(time.time() - total_test_timei) + "s"

    def paced_shooter(self, url, observation_time, requests, command, wait_time):
        #observation_time is in minutes
        for i in range(observation_time):
            counter = 0
            while(counter < requests):
                conn = httplib.HTTPConnection(url)

                if(command == ESCRITA_E_LEITURA):
                    print "Write"
                    conn.request("GET", "/write_and_read")
                else:
                    print "Read"
                    conn.request("GET", "/read")

                total_timei = time.time()
                r1 = conn.getresponse()
                total_timef = time.time() - total_timei
                response = r1.read().split(" ")
                time_elapsed = response[0]
                bd_time = response[1]
                cpu_usage = response[2]

                if(command == ESCRITA_E_LEITURA):
                    self.write_data('write', total_timef, time_elapsed, bd_time, cpu_usage)
                else:
                    self.write_data('read',  total_timef, time_elapsed, bd_time, cpu_usage)
                counter += 1
                time.sleep(wait_time)

    # saves the data
    def write_data(self, command, total_time, server_response, bd_response, cpu_usage):
        fd = open(self.output, 'a')
        output = csv.writer(fd, delimiter=' ')
        output.writerow([command, total_time, server_response, bd_response, cpu_usage])
        fd.close()

if __name__ == '__main__':
    tester = TesterADSD(1, 10, output='output.csv')
    tester.set_target('127.0.0.1:5000')
    tester.set_mode(0) # 0 = leitura | 1 = escrita
    tester.start()
