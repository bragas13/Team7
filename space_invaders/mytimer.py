import time
import threading
import sys

class Timer:
    should_blink = False
    run_time = 1
    timer_thread = 0
    kill_order = False

    def kill_thread(self):
        self.kill_order = True

    def start_timer(self):
       self.timer_thread = threading.Thread(target=self.start_timer2)
       self.timer_thread.start()

    def start_timer2(self):
        if self.kill_order:
            return
        while(self.run_time > 0):
            start = time.time()
            time.sleep(0.1)
            end = time.time()
            self.run_time -= (end - start)
           
        if self.should_blink == True:
            self.should_blink = False
        elif self.should_blink == False:
            self.should_blink = True
        self.restart()

    def restart(self):
        self.run_time = 1
        self.start_timer2()

    def get_status(self):
        return self.should_blink