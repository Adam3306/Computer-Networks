import sys
import csv
import json
from collections import deque
from subprocess import PIPE, Popen
from itertools import islice
from datetime import datetime

max_workers = 5

class p_r:
    def __init__(self, fileName):
        self.pingArr = []
        self.traceArr = []
        self.commands = []
        self.readfile(fileName)

        self.runProcesses()
        self.writeFile()
    
    def readfile(self, fileName):
        #read the first 10 elements
        with open(fileName) as csv_file: 
                csv_reader = csv.reader(csv_file, delimiter=',')
                for i, row in csv_reader:
                    self.commands.append("ping -c 10 " + row)
                    # self.commands.append("ping -n 10 " + row)
                    self.commands.append("traceroute -h 30 " + row)
                    # self.commands.append("tracert -h 30 " + row)
                    if (9 < int(i)):
                        break

        # read the last 10 elements - 11.55
        with open(fileName) as fin:
            deq=deque(csv.reader(fin),10)

        for sub_list in deq:
            self.commands.append("ping -c 10 " + sub_list[1])
            # self.commands.append("ping -n 10 " + sub_list[1])
            self.commands.append("traceroute -h 30 " + sub_list[1])
            # self.commands.append("tracert -h 30 " + sub_list[1])

    def writeFile(self):
        date = datetime.today().strftime('%Y%m%d')
        platform = "windows" if sys.platform == "win32" else "linux"
        pings = {
            "date": date,
            "system": platform,
            "pings": self.pingArr
        }

        traces = {
            "date": date,
            "system": platform,
            "traces": self.traceArr
        }

        with open("ping.json", "w") as write_file:
            json.dump(pings, write_file)
        
        with open("traceroute.json", "w") as write_file:
            json.dump(traces, write_file)


    def runProcesses(self):
        processes = (Popen(cmd.split(" "), stdout = PIPE) for cmd in self.commands)
        running_processes = list(islice(processes, max_workers))        # start new processes
        while running_processes:
            for i, process in enumerate(running_processes):
                response = process.poll()
                if response is not None:                          # the process has finished
                    output = process.communicate()[0]
                    output = output.decode("utf-8")
                    output = output.replace("\r", "")
                    target = process.args[3]
                    action = process.args[0]
                    tmpObj = {
                                "target": target,
                                "output": output
                    }

                    tmpObj = json.dumps(tmpObj) 

                    if (action == "ping"):
                        self.pingArr.append(tmpObj)
                    else:
                        self.traceArr.append(tmpObj)
                    
                    running_processes[i] = next(processes, None)        # start new process
                    if running_processes[i] is None:                    # no new processes
                        del running_processes[i]
                        break

p1 = p_r(sys.argv[1])