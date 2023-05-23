import time 

cur_time = 0.0 #الوقت الحالي
cur_seconds = 0
def reset():
  global cur_time
  cur_time = 0.0

def curTime():
  global cur_time
  cur_time = int(time.time())
  return cur_time

def nowTime():  
  return int(time.time())


def cSeconds():
  global cur_seconds
  cur_seconds  = int(time.time())

def nowSeconds():
  nowSeconds  = int(time.time())
  return nowSeconds




