我将tclab fork出来，主要是使用labtime这个类来做仿真加速实现Gravity-Drained Tanks ，具体物理背景的介绍可以参考John教授的视频https://www.youtube.com/watch?v=FMs00ovzpoI ,抱歉，我不想学rst文件的语法了，链接凑合看吧。

TCLab: Temperature Control Laboratory
=====================================

Master:

.. image:: https://travis-ci.org/jckantor/TCLab.svg?branch=master
    :target: https://travis-ci.org/jckantor/TCLab

.. image:: https://readthedocs.org/projects/tclab/badge/?version=latest
    :target: http://tclab.readthedocs.io/en/latest/?badge=latest

.. image:: https://badge.fury.io/py/tclab.svg
    :target: https://badge.fury.io/py/tclab

Development:

.. image:: https://travis-ci.org/jckantor/TCLab.svg?branch=development
    :target: https://travis-ci.org/jckantor/TCLab

``TCLab`` provides a Python interface to the
`Temperature Control Lab <http://apmonitor.com/pdc/index.php/Main/ArduinoTemperatureControl>`_
implemented on an Arduino microcontroller over a USB interface.
``TCLab`` is implemented as a Python class within
the ``tclab`` package.  The ``tclab`` package also includes:

* ``clock`` A Python generator for soft real-time implementation of
  process control algorithms.
* ``Historian`` A Python class to log results of a process control
  experiment.
* ``Plotter`` Provides an historian with real-time plotting within a
  Jupyter notebook.
* ``TCLabModel`` An embedded model of the temperature control lab
  for off-line and faster-than-realtime simulation of process control
  experiments. No hardware needs to be attached to use ``TCLabModel``.

The companion Arduino firmware for device operation is available at the
`TCLab-Sketch repository <https://github.com/jckantor/TCLab-sketch>`_.

The `Arduino Temperature Control Lab <http://apmonitor.com/pdc/index.php/Main/ArduinoTemperatureControl>`_
is a modular, portable, and inexpensive solution for hands-on process
control learning.  Heat output is adjusted by modulating current flow to
each of two transistors. Thermistors measure the temperatures. Energy
from the transistor output is transferred by conduction and convection
to the temperature sensor. The dynamics of heat transfer provide rich
opportunities to implement single and multivariable control systems.
The lab is integrated into a small PCB shield which can be mounted to
any `Arduino <https://www.arduino.cc/>`_ or Arduino compatible
microcontroller.

Installation
------------

Install using ::

   pip install tclab
   
To upgrade an existing installation, use the command ::

   pip install tclab --upgrade


The development version contains new features, but may be less stable. To install the development version use the command ::

   pip install --upgrade https://github.com/jckantor/TCLab/archive/development.zip


Hardware setup
--------------

1. Plug a compatible Arduino device (UNO, Leonardo, NHduino) with the
   lab attached into your computer via the USB connection. Plug the DC
   power adapter into the wall.

2. (optional) Install Arduino Drivers

   *If you are using Windows 10, the Arduino board should connect
   without additional drivers required.*

   For Arduino clones using the CH340G, CH34G or CH34X chipset you may need additional drivers. Only install these if you see a message saying "No Arduino device found." when connecting.

   * `macOS <https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver>`__.
   * `Windows <http://www.wch.cn/downfile/65>`__.

3. (optional) Install Arduino Firmware

   ``TCLab`` requires the one-time installation of custom firmware on
   an Arduino device. If it hasn't been pre-installed, the necessary
   firmware and instructions are available from the
   `TCLab-Sketch repository <https://github.com/jckantor/TCLab-sketch>`_.

Checking that everything works
------------------------------

Execute the following code ::

    import tclab
    with tclab.TCLab() as lab:
        print(lab.T1)

If everything has worked, you should see the following output message ::

    Connecting to TCLab
    TCLab Firmware Version 1.2.1 on NHduino connected to port XXXX
    21.54
    TCLab disconnected successfully.

The number returned is the temperature of sensor T1 in °C.


Troubleshooting
---------------

If something went wrong in the above process, refer to our troubleshooting guide
in TROUBLESHOOTING.md.

Next Steps
----------

The notebook directory provides examples on how to use the TCLab module.
The latest documentation is available at
`Read the Docs <http://tclab.readthedocs.io/en/latest/index.html>`_.

Course Websites
---------------

Additional information, instructional videos, and Jupyter notebook
examples are available at the following course websites.

* `Arduino temperature control lab page <http://apmonitor.com/pdc/index.php/Main/ArduinoTemperatureControl>`__ on the BYU Process Dynamics and Control course website.
* `CBE 30338 <http://jckantor.github.io/CBE30338/>`__ for the Notre Dame
  Chemical Process Control course website.
* `Dynamics and Control <https://github.com/alchemyst/Dynamics-and-Control>`__ for notebooks developed at the University of Pretoria.
