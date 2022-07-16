import time
from timints import *

tic()
time.sleep(3)
toc()

with Timer("As a context manager"):
    time.sleep(3)
    
timer1 = Timer("As a verbose object")
timer1.tic()
time.sleep(3)
timer1.toc()

timer2 = Timer()
timer2.tic()
time.sleep(3)
diff = timer2.toc()
print(diff)

timer3 = Timer("As another verbose object")

timer1.tic()
timer3.tic()
time.sleep(3)
timer1.toc()
time.sleep(3)
timer3.toc()

@tictoc
def long_operation():
    time.sleep(3)
    
long_operation()

timer4 = Timer("Using the decorator")
@timer4.tictoc
def another_long_operation():
    time.sleep(3)
    
another_long_operation()

tic()
time.sleep(1)
toctic()
time.sleep(1)
toctic()
time.sleep(1)
toc()

with TIMER:
    time.sleep(3)

with Timer("As a context manager for an error"):
    raise Exception("Something wrong")