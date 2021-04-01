import time
import itertools
import os
import matplotlib
import numpy as np
from multiprocessing import Process, Manager
from keras.models import model_from_json
from keras.preprocessing import sequence
from scipy import interp
from datetime import datetime

# basePath="/home/bkcs/Downloads/ZendApp3/tool/dgaDetectionSystem"
basePath="."
class DgaPredict():
    def _init_(self):
       print("loaded model")
    #Load Model
    def loadModelBinary(self,model,weight): 
        # load json and create model
        json_file = open(model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model_binary = model_from_json(loaded_model_json)
        # load weights into new model
        self.model_binary.load_weights(weight)
        print("Loaded model from disk")
    
    #Load Model   
    def loadModelMulti(self,model,weight): 
        # load json and create model
        json_file = open(model, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model_dga = model_from_json(loaded_model_json)
        # load weights into new model
        self.model_dga.load_weights(weight)
        print("Loaded model from disk")
    
    #Preprocess    
    def preprocess(self,domain):
        x = [[self.valid_chars[i] for i in domain]]
        x = sequence.pad_sequences(x, maxlen=self.maxlen)
        return x

    #Preprocess 
    def preprocessDga(self,domain):
        x = [[self.valid_chars_dga[i] for i in domain]]
        x = sequence.pad_sequences(x, maxlen=self.maxlendga)
        return x
    
    def predict_binary(self,domain):
            dm = self.preprocess(domain)
            y_pred = self.model_binary.predict_proba(dm)
            return y_pred[0] 

    def predict(self,domain):
        try:
            dm = self.preprocess(domain)
            # print dm
            y_pred = self.model_binary.predict_proba(dm)
            if(y_pred[0]<=0.5):
                return 38
            else:
                dmdga = self.preprocessDga(domain)
                y_pred_dga = self.model_dga.predict(dmdga)
                dga = np.argmax(y_pred_dga[0])
                # print 'Domain %s may be generated by Botnet' % domain
                return dga
        except:
            return 39
            # print 'Domain %s is legitimate' % domain
        # else:
            # dm = sequence.pad_sequences(dm, maxlen=49)
            # y_pred_dga = self.model_dga.predict(dm)
            # dga = np.argmax(y_pred_dga[0])
            #      
    def loadModelInit(self):
        self.valid_chars = {
            '-': 1,'.': 2,'1': 3, '0': 4, '3': 5, '2': 6, '5': 7, '4': 8, '7': 9, '6': 10,
            '9': 11, '8': 12, '_': 13, 'a': 14, 'c': 15, 'b': 16, 'e': 17, 'd': 18, 'g': 19, 'f': 20,
            'i': 21, 'h': 22, 'k': 23, 'j': 24, 'm': 25, 'l': 26, 'o': 27, 'n': 28, 'q': 29, 'p': 30,
            's': 31, 'r': 32, 'u': 33, 't': 34, 'w': 35, 'v': 36, 'y': 37, 'x': 38, 'z': 39
        }
        self.valid_chars_dga = {
            '-': 1, '.': 2, '1': 3, '0': 4, '3': 5, '2': 6, '5': 7, '4': 8, '7': 9, '6': 10, '9': 11, '8': 12, 'a': 13, 'c': 14, 'b': 15, 'e': 16, 'd': 17, 'g': 18, 'f': 19, 'i': 20, 'h': 21, 'k': 22, 'j': 23, 'm': 24, 'l': 25, 'o': 26, 'n': 27, 'q': 28, 'p': 29, 's': 30, 'r': 31, 'u': 32, 't': 33, 'w': 34, 'v': 35, 'y': 36, 'x': 37, 'z': 38
        }
        self.list_dga = {'geodo': 0, 'murofet': 2, 'pykspa': 3, 'fobber': 19, 'ramnit': 5, 'Volatile': 6, 'locky': 12, 'simda': 9, 'ramdo': 10, 'suppobox': 11, 'ranbyus': 7, 'tempedreve': 13, 'qadars': 14, 'symmi': 15, 'banjori': 16, 'beebone': 1, 'hesperbot': 18, 'qakbot': 8, 'corebot': 22, 'dyre': 20, 'cryptowall': 21, 'tinba': 17, 'padcrypt': 4, 'P': 23, 'bedep': 24, 'matsnu': 25, 'ptgoz': 26, 'necurs': 27, 'pushdo': 28, 'cryptolocker': 29, 'dircrypt': 30, 'shifu': 31, 'bamital': 32, 'kraken': 33, 'nymaim': 34, 'shiotob': 35, 'virut': 36}
        self.maxlen = 73
        self.maxlendga = 49
        basePath="."
        model_binary = basePath+"/Model/model_binary.json"
        model_weight_bi = basePath+"/Model/model_binary.h5"
        model_dga = basePath+"/Model/model_dga.json"
        model_weight_dga = basePath+"/Model/model_dga.h5"
        self.loadModelBinary(model_binary,model_weight_bi)
        self.loadModelMulti(model_dga,model_weight_dga)
   
  
           
                
           

                    

                        
        			
                    

        			 
    
 