import subprocess
import time
import multiprocessing

def start():
    print("starting live.py")
    subprocess.call("./live.py", shell=True)


if __name__ == '__main__':
    while(True):
        proc = multiprocessing.Process(target=start, name="start", args=())
        proc.start()
        time.sleep(60*60*4)
        proc.terminate()
        proc.join()

