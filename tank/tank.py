import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import odeint
import tclab
from tclab import labtime



class gravtank():
    
    def __init__(self, name='', A=1, Cv=1):
        self.name = name
        self.A = A
        self.Cv = Cv
        self._log = []
        self.qin = 0
        self.tstart = labtime.time()  # start time
        self.tlast = self.tstart      # last update time
    
    def qout(self,h):
        return self.Cv*np.sqrt(float(h))
    
    def deriv(self,h,t):
        dh = (self.qin - self.qout(h))/self.A
        return dh
    
    def plot(self):
        t,qout,h = np.asarray(self._log).transpose()
        plt.plot(t,qout,label=self.name + ' qout')
        plt.plot(t,h,label=self.name + ' h')
        plt.legend(loc='best')
    
    def generator(self,dt,IC = 0):
        h = IC
        while True:
            print('before in '+self.name)
            t,dt,self.qin = yield self.qout(h),float(h)
            print('after in ' + self.name)
            h = odeint(self.deriv,h,[t,t+dt])[-1]
            self._log.append([t,self.qout(h),float(h)])
            t += dt
            
            
class CGravtank():
    
    def __init__(self, name='', tank1={}, tank2={},h1=0,h2=0):

        if not tank1 or not tank2:
          raise ValueError('tank1 and tank2 must be defined')

        self.name = name
        self.ifOneTank = False

        if tank1['A'] == 0 and tank1['C1'] == 0:
          raise ValueError('tank1 A and C1 must great than 0')
        if tank2['A'] == 0 and tank2['C1'] == 0:
          self.ifOneTank = True
          

        self.tank1_obj = gravtank('tank1',\
                        tank1['A'],tank1['Cv'])
        if not self.ifOneTank:
          self.tank2_obj = gravtank('tank2',\
                        tank2['A'],tank2['Cv'])

        #initialize the generators
        self.tank1 = self.tank1_obj.generator(dt=0.1,IC=h1)
        self.tank1.send(None)
        if not self.ifOneTank:
          self.tank2 = self.tank2_obj.generator(dt=0.1,IC=h2)
          self.tank2.send(None)

        self._log = []
        self.tstart = labtime.time()  # start time
        self.tlast = self.tstart      # last update time
        self.qin1 = 0
        self.maxstep = 0.1
    
    def plot(self):
      plt.clf()
      self.tank1_obj.plot()
      self.tank2_obj.plot()  
    def Qin(self,qin):
        self.qin1 = qin
        self.update()
      
    def H1(self):
        self.update()
        return self.h1
    def H2(self):
        self.update()
        return self.h2

    def update(self):
        now = labtime.time()
        t = now 
        teuler = self.tlast
        while True:
          dt = min(self.maxstep, t - teuler)
          qout1,self.h1 = self.tank1.send((teuler,dt,self.qin1))
          if not self.ifOneTank:
            qout2,self.h2 = self.tank2.send((teuler,dt,qout1))
          self.tlast = now 
          teuler += dt
          if teuler == t:
            break
    
          
def test():
  labtime.set_rate(10)
  t = CGravtank(name='test',tank1={'A':5,'Cv':1},\
              tank2={'A':10,'Cv':2},h1=10,h2=10) 
  
  for i in tclab.clock(400,adaptive=False):
    t.Qin(10) 
    labtime.stop()
    t.plot()
    plt.draw()
    plt.pause(0.01)
    labtime.start()
  print("plot")
  input("Press Enter to continue...")

  
  
  
  
  
  
  

if __name__ == '__main__':
    test()

    
    
