import csv
import numpy as np

class Csv(object):
    

    def leer_csv(self,nombre,delimitador):
        archivo=np.loadtxt(nombre,dtype=np.str,delimiter=delimitador,skiprows=1)
        return archivo
        pass
    pass


