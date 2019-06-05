# Importar la libreria Pandas 
import pandas as pd
# Pa'l path
import os

import numpy as np

path = os.path.dirname(os.path.abspath(__file__)) 
# Get dataset
df = pd.read_csv(path+'/SMSSpamCollection', 
                   sep='\\t', 
                   names=['label','sms_message'],
                   engine='python')

## Imprime primeras 5 filas
# Conversion:
   # 1: spam
   # 0: no spam (ham)
df['label'] = df.label.map({'ham':0, 'spam':1})

# Visualizar las dimensiones de los datos
a = np.array(df)
print (a.shape)
