#!/usr/bin/env python
import time
import subprocess



if __name__ == '__main__':


    c = 0


    while(True):
        print("been running for ",4*c," hours")
        c = c+1
        proc=subprocess.Popen("./live.py")
        time.sleep(60*60*4)
        proc.terminate()


