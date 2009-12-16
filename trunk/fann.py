from pyfann.libfann import neural_net,SIGMOID_SYMMETRIC_STEPWISE

connectionRate = 1
learningRate = 0.7
neuronsHiddenNum = 4

desiredError = 0.00005
maxIterations = 100000
iterationsBetweenReports = 1000
inNum=4
outNum=1
class NeuNet(neural_net):
	def __init__(self):
		neural_net.__init__(self)
		#~ neural_net.create_sparse_array(self,connectionRate,(inNum,neuronsHiddenNum, outNum))
		neural_net.create_standard_array(self,(inNum,outNum))
		neural_net.set_learning_rate(self,learningRate)
		neural_net.set_activation_function_output(self,SIGMOID_SYMMETRIC_STEPWISE)
	
	def train_on_file(self,fileName):
		neural_net.train_on_file(self,fileName,maxIterations,iterationsBetweenReports,desiredError)
	
	#~ def 
#~ ann = libfann.neural_net()
#~ ann.create_sparse_array(connection_rate, (num_input, num_neurons_hidden, num_output))
#~ ann.set_learning_rate(learning_rate)
#~ ann.set_activation_function_output(libfann.SIGMOID_SYMMETRIC_STEPWISE)

#~ ann.train_on_file("../../examples/xor.data", max_iterations, iterations_between_reports, desired_error)

#~ ann.save("xor_float.net")

