import sys
import time
# 自定义进度条

# 进度条：总进度，当前进度
class ProgressBar():
    def __init__(self, max,mode='standard', hint='Progress', ):
        self.mode=mode
        self.hint=hint
        self.max=max
        self.progress=0
    def set_mode(self,mode):self.mode=mode
    def set_hint(self,hint):self.hint=hint
    def start(self):
        if self.mode!='simple':self.start_ = time.perf_counter()
    def next(self,info=''):
        self.progress+=1
        progress=self.progress
        all_work=self.max
        i = int(progress / all_work * 100)
        if self.mode=='simple':

            print("\r", end="")
            print(self.hint+": {}%: ".format(i), "▋" * (i // 2), end="")
            sys.stdout.flush()
        elif self.mode=='standard':
            scale=100
            a = "*" * i
            b = "." * (scale - i)
            c = (i / scale) * 100
            try:
                dur = time.perf_counter() - self.start_
                print( "\r"+self.hint+ " "+info+" {:^3.0f}%[{}->{}]{:.2f}s".format(c, a, b, dur),end='')
            except:
                print("ProgressBar:你没有start")

def test():
    num = 1000
    bar=ProgressBar(hint='train',max=num)
    bar.start()
    for i in range(1, num):
        bar.next(info="epoch"+str(i))
        time.sleep(0.01)