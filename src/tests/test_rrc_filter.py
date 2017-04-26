# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 20:11:26 2017

@author: Calil
"""

import unittest
import numpy as np
import matplotlib.pylab as plt

from rrc_filter import RRCFilter

class RRCFilterTest(unittest.TestCase):
    
    def setUp(self):
        # Flag for plotting
        self.plot_flag = True
        
        # Filter 1
        self.filter1 = RRCFilter(100,0.8,1e-3,2e6,8)
        
    def test_N(self):
        self.assertEqual(self.filter1.N,100)
        
    def test_alpha(self):
        self.assertEqual(self.filter1.alpha,0.8)
        
    def test_Ts(self):
        self.assertEqual(self.filter1.Ts,1e-3)
        
    def test_Fs(self):
        self.assertEqual(self.filter1.Fs,2e6)
        
    def test_up_factor(self):
        self.assertEqual(self.filter1.up_factor,8)
        
    def test_up_sample(self):
        symbs = np.ones(10)
        up_symbs = self.filter1.upsample(symbs)
        self.assertEqual(len(up_symbs),80)
        self.assertEqual(np.sum(up_symbs),10)
        
    def test_filter_response(self):
        h, t = self.filter1.filter_response(100,0.8,1e-3,2e6)
        self.assertAlmostEqual(np.sum(abs(h)**2),1.0,delta=1e-5)
        self.assertTrue(np.all(h == self.filter1.response))
        self.assertTrue(np.all(t == self.filter1.time))
        
    def test_plot(self):
        if self.plot_flag:
            #Define variables
            N = 1000
            alpha = 0.8
            Ts = 1e-4
            Fs = 1e3
            
            # Calculate response
            h, t = self.filter1.filter_response(N,alpha,Ts,Fs)
            
            plt.plot(t,h)
            plt.xlabel("Time [s]")
            plt.ylabel("Impulse response")
            tit = "N=" + str(N) + " alpha=" + str(alpha) + " Ts=" + str(Ts) +\
                " Fs=" + str(Fs/1e6) + "MHz"
            plt.title(tit)
            plt.show()
            
            sig = np.zeros(1000)
            sig[0] = 2
            sig[500] = 1
            filt_sig = self.filter1.apply_filter(h,Fs,sig)
            
            plt.plot(filt_sig)
            plt.xlabel("Time [s]")
            plt.ylabel("Filtered signal")
            plt.show()            
        
if __name__ == '__main__':
    unittest.main()