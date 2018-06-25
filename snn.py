import math as m
import numpy as np

class SNN_network():
	def __init__(self,hiddenSize):
		self.layerSizes = [3, hiddenSize, 3]
		self.I = [0]*3
		self.t_start = 0
		self.t_end   = 20
		self.spike_input = [[False for y in range(self.t_start,self.t_end)] for x in range(0,self.layerSizes[0])]
		self.spike_hidden= [[False for y in range(self.t_start,self.t_end)] for x in range(0,self.layerSizes[1])]
		self.spikes_out = [[],[],[]]
		self.v_in = [0]*self.layerSizes[0]

		self.v_hid= [0]*self.layerSizes[1]
		self.x_hid= [0]*self.layerSizes[1]
		self.y_hid= [0]*self.layerSizes[1]

		self.v_out= [0]*self.layerSizes[2]
		self.x_out= [0]*self.layerSizes[2]
		self.y_out= [0]*self.layerSizes[2]
        
        
	def setWeights(self, w1, w2, w3):
		self.w1 = w1	#Weights between hidden and input layer
		self.w2 = w2	#Weights between output and hidden layer
		self.w3 = w3
		len1 = len(w1)
		len2 = len(w2)
		len3 = len(w3)
		self.g1 = [0]*len1	# Synapse eligiblity trace (thesis pg-21)
		self.g2 = [0]*len2
		self.g3 = [0]*len3

	def updateIn(self,t): #update input layer
		dvdt = [0]*self.layerSizes[0]
		for i in range(0,self.layerSizes[0]):
			self.spike_input[i][t] = False
			dvdt[i] = self.I[i]+0.025
			self.v_in[i] += dvdt[i]
			if(self.v_in[i]>=1.0):
				self.v_in[i] = 0.
				self.spike_input[i][t] = True
    
	def synapse1(self,t): #propagate spikes from input to hidden
		for i in range(0,self.layerSizes[0]):
			if(self.spike_input[i][t]):
				for j in range(0,self.layerSizes[1]):
					self.y_hid[j] += self.w1[i*self.layerSizes[1]+j]
    
	def synapse2(self,t): #propagate spikes from hidden to output
		for i in range(0,self.layerSizes[1]):
			if(self.spike_hidden[i][t]):
				self.y_out[0] += self.w2[i]
				self.y_out[1] += self.w2[i+self.layerSizes[1]]

	def update_weights(self):
					
    
	def calcResult(self): #calc result according to thesis
		for s in self.spikes_out[0]:
			thisA = p.alpha * ((self.t_end-s)/self.t_end)
			self.res[0] += thisA*m.exp(p.beta*(s-self.t_end))-p.gamma
		for s in self.spikes_out[1]:
			thisA = p.alpha * ((self.t_end-s)/self.t_end)
			self.res[1] += thisA*m.exp(p.beta*(s-self.t_end))-p.gamma
		for s in self.spikes_out[2]:
			thisA = p.alpha * ((self.t_end-s)/self.t_end)
			self.res[2] += thisA*m.exp(p.beta*(s-self.t_end))-p.gamma
		for i in range(3):    
			self.final_res[i] = self.res[i]

	def forward_simulate(self):
		for t in range(self.t_start,self.t_end):
			self.updateIn(t)
			self.synapse1(t)
			self.updateHid(t)

			self.synapse2(t)
			self.updateOut(t)

		self.calcResult()