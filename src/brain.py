import aiml

class Brain(object):

    def __init__(self, aiml_file='std-startup.xml'):
        self.kernel = aiml.Kernel()
        self.kernel.learn(aiml_file)
