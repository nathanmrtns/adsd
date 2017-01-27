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
            time_elapsed = self.shoot(command)
            self.write_data(self.rate, time_elapsed, iteration)

    def shoot(self, command):
        start_time = time.time()
        p = check_output(command.split(' '))
        time_elapsed = time.time() - start_time
        return time_elapsed

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
    def write_data(self, rate, duration, iteration):
        fd = open(self.output, 'a')
        output = csv.writer(fd, delimiter=' ')
        output.writerow([rate, duration, iteration])
        fd.close()

if __name__ == '__main__':
    tester = TesterADSD(10, 10, output='output.csv')
    tester.set_target('35.165.5.104')
    tester.set_mode(1)
    tester.start()
