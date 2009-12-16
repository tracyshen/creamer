import fann
from pyfann import libfann

ann=fann.NeuNet()
ann.train_on_file("cream.data")
ann.save("cream.net")

#~ ann=fann.NeuNet()
#~ ann.create_from_file("cream.net")

def test(l,res):
	print "%s should be %s"%(ann.run(l),res)
	
test([350,0.83,0.8],True)
test([114,0.94,0.98,0.96],True)
test([38,0.7,0,0.0],False)
test([32, 0.42, 0, 0],-1)
test_data = libfann.training_data()
test_data.read_train_from_file("cream.data")
ann.test_data(test_data)
print "MSE error on test data: %f" % ann.get_MSE()

#~ calc_out=ann.run([350,0.83,0.8])
#~ print calc_out,' should be: ','True'
#~ print ann.run([114,0.94,0.98,0.96]),[114,0.94,0.98,0.96]
#~ print ann.run([38,0.7,0,0.0]),'should be: False'
