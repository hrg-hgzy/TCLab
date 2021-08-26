import numpy as np
from scipy.integrate import odeint
from tclab import labtime
import matplotlib.pyplot as plt



if_log = False



class gravtank():
    
    def __init__(self, name='', A=1, Cv=1, hlimit=500):
        self.name = name
        self.A = A
        self.Cv = Cv
        self.hlimit = hlimit
        self._log = []
        self.qin = 0
    
    def qout(self,h):
        return self.Cv*np.sqrt(float(h))
    
    def deriv(self,h,t):
        if h < 0:
          raise ValueError('h is negative')
        dh = (self.qin - self.qout(h))/self.A
        if h >= self.hlimit and dh > 0:
          return 0
        return dh
    
    def plot(self):
        if not self._log:
          return
        t,qout,h = np.asarray(self._log).transpose()
        plt.plot(t,qout,label=self.name + ' qout')
        plt.plot(t,h,label=self.name + ' h')
        plt.legend(loc='best')
    
    def generator(self,dt,IC = 0):
        h = IC
        while True:
            t,dt,self.qin = yield self.qout(h),float(h)
            h = odeint(self.deriv,h,[t,t+dt])[-1]
            if if_log:
              self._log.append([t,self.qout(h),float(h)])
            #t += dt

            
            
class CGravtank():
    
    def __init__(self, name='', tank1={}, tank2={},h1=0,h2=0):

        if not tank1 or not tank2:
          raise ValueError('tank1 and tank2 must be defined')
        
        if h1 < 0 or h2 < 0:
          raise ValueError('h1 and h2 must be positive')

        self.name = name
        self.ifOneTank = False

        if tank1['A'] <= 0 or tank1['Cv'] <= 0 or tank1['hlimit'] <= 0:
          raise ValueError('tank1 A, C1 and hlimit must be great than 0')
        if tank2['A'] <= 0 or tank2['Cv'] <= 0 or tank2['hlimit'] <= 0:
          print("only one tank is simulated!")
          self.ifOneTank = True

        
          

        self.tank1_obj = gravtank('tank1',\
                        tank1['A'],tank1['Cv'],tank1['hlimit'])
        if not self.ifOneTank:
          self.tank2_obj = gravtank('tank2',\
                        tank2['A'],tank2['Cv'],tank2['hlimit'])

        #initialize the generators
        self.tank1 = self.tank1_obj.generator(dt=0.1,IC=h1)
        self.tank1.send(None)
        if not self.ifOneTank:
          self.tank2 = self.tank2_obj.generator(dt=0.1,IC=h2)
          self.tank2.send(None)

        labtime.start()
        self._log = []
        #self.tlast = labtime.time()
        self.tlast = 0
        self.qin1 = 0
        self.maxstep = 0.1
    
    def plot(self):
      if not if_log:
        return
      self.tank1_obj.plot()
      self.tank2_obj.plot()  
    def Qin(self,qin):
        if qin < 0:
          raise ValueError('qin is negative')
        self.update()
        self.qin1 = qin
      
    def H1(self):
        self.update()
        return self.h1
    def H2(self):
        self.update()
        return self.h2

    def update(self):
        if(self.tlast == 0):
          self.tlast = labtime.time()
          return

        now = labtime.time()
        t = now - self.tlast
        
        teuler = self.tlast
        while True:
          dt = min(self.maxstep, now - teuler)
          if dt <= 0:
            break
          qout1,self.h1 = self.tank1.send((teuler,dt,self.qin1))

          if not self.ifOneTank:
            qout2,self.h2 = self.tank2.send((teuler,dt,qout1))
          teuler += dt
          if teuler == t:
            break
        self.tlast = now 

    
def test():
  import tclab
  import time
  labtime.set_rate(10)

  t = CGravtank(name='test',tank1={'A':4,'Cv':15,'hlimit':12},\
              tank2={'A':6,'Cv':10,'hlimit':20},h1=0,h2=0) 
  labtime_start = labtime.time()
  time_start = time.time()
  print("start simulation:") 
  for i in tclab.clock(400,step =1,adaptive=False):
    t_real = time.time() - time_start
    t_lab = labtime.time() - labtime_start
    #print("real time = {0:4.1f}    lab time = {1:4.1f}    m.time = {1:4.1f}".format(t_real, t_lab,m.time))
    #print("real time = {0:4.1f}    lab time = {1:4.1f}    ".format(t_real, t_lab))
    print("tclab clock is {}".format(i))
    t.Qin(20) 
    labtime.stop()
    if if_log:
      plt.clf()
      t.plot()
      plt.pause(0.02)
    labtime.start()
  if if_log:
    plt.show()
  print("plot")
  input("Press Enter to continue...")

  
def create_tank(name,A1,Cv1,hlimit1,\
                A2,Cv2,hlimit2,h1,h2):
  tank1 = {
    'A':A1,
    'Cv':Cv1,
    'hlimit':hlimit1
  }
  tank2 = {
    'A':A2,
    'Cv':Cv2,
    'hlimit':hlimit2
  }
  return CGravtank(name=name,tank1=tank1,
                   tank2=tank2,h1=h1,h2=h2) 

if __name__ == '__main__':
    test()

    
    