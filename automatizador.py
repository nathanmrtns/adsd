import os
import csv
import time
from subprocess import check_output
from subprocess import Popen

LEITURA = 0
ESCRITA_E_LEITURA = 1
COMMAND_FORMAT = {}
COMMAND_FORMAT['httperf'] = ("httperf --hog --server={server}"
                             " --port={port} --num-conns={requests}"
                             " --rate={rate} --uri={uri} --print-reply=body")

class TesterADSD(object):
    def __init__(self, rate, repetitions, output=None, mode=LEITURA):
        self.rate = rate
        self.repetitions = repetitions
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
        command = self.build_command()
        for iteration in range(self.repetitions):
            response = self.shoot(command)
            time_elapsed = response[0]
            bd_time = response[1].split(" ")[0]
            cpu_usage = response[1].split(" ")[1]
            if(command.split(' ')[6] == "--uri=/write_and_read"):
                self.write_data(self.rate, time_elapsed, iteration, 'write', bd_time, cpu_usage)
            else: self.write_data(self.rate, time_elapsed, iteration, 'read', bd_time, cpu_usage)

    def shoot(self, command):
        start_time = time.time()
        p = check_output(command.split(' '))
        time_elapsed = time.time() - start_time
        bd_time = p.split("\n")[1].split(":")[1]
        return [time_elapsed, bd_time]

    def build_command(self):
        command = COMMAND_FORMAT['httperf']
        if self.mode == LEITURA:
            uri = '/read'
        else:
            uri = '/write_and_read'
        final_command = command.format(
            server=self.url,
            port=5000,
            requests=self.rate,
            rate=self.rate,
            uri=uri
        )

        return final_command

    # salva os dados no arquivo definido
    def write_data(self, rate, duration, iteration, command, bd_duration, cpu_usage):
        fd = open(self.output, 'a')
        output = csv.writer(fd, delimiter=' ')
        output.writerow([rate, duration, iteration, command, bd_duration, cpu_usage])
        fd.close()

if __name__ == '__main__':
    tester = TesterADSD(1, 10, output='output.csv')
    tester.set_target('127.0.0.1')
    tester.set_mode(1) # 0 = leitura | 1 = escrita
    tester.start()
