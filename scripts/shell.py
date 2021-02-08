import os
import sys
import threading
from time import sleep
from subprocess import Popen, PIPE, STDOUT


class Shell:
    def __init__(self):
        self.process = None
        self.reader = None
        self.writer = None

    def start(self, cmd):
        env = os.environ.copy()
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT, shell=True, env=env)
        self.reader = self.spawn(self.read)
        self.writer = self.spawn(self.write)

    def spawn(self, target):
        thread = threading.Thread(target=target, daemon=True)
        thread.start()
        return thread

    def read(self):
        data = True
        while data:
            data = self.process.stdout.read(1).decode("utf-8")
            sys.stdout.write(data)
            sys.stdout.flush()

    def write(self):
        data = True
        while data:
            data = sys.stdin.read(1)
            self.process.stdin.write(data.encode())
            self.process.stdin.flush()

    @property
    def terminated(self):
        return not self.reader.is_alive() and not self.reader.is_alive()

    def wait(self):
        while not self.terminated:
            sleep(.1)


shell = Shell()
shell.start('nano')
shell.wait()
