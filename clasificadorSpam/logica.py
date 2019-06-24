import os
import pandas as pd
import collections
import numpy as np
from operator import itemgetter
import heapq
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

STOP_WORDS = [
    "a", "about", "above", "across", "after", "afterwards", 
    "again", "all", "almost", "alone", "along", "already", "also",    
    "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "as", "at", "be", "became", "because", "become","becomes", "becoming", "been", "before", "behind", "being", "beside", "besides", "between", "beyond", "both", "but", "by","can", "cannot", "cant", "could", "couldnt", "de", "describe", "do", "done", "each", "eg", "either", "else", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "find","for","found", "four", "from", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "i", "ie", "if", "in", "indeed", "is", "it", "its", "itself", "keep", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mine", "more", "moreover", "most", "mostly", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next","no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part","perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "she", "should","since", "sincere","so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "take","than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they",
    "this", "those", "though", "through", "throughout",
    "thru", "thus", "to", "together", "too", "toward", "towards",
    "under", "until", "up", "upon", "us",
    "very", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", 
    "who", "whoever", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"
]

class Clasificador:
    DICCIONARIO = None             # Almacena las palabras consideradas para la clasificación (conjunto de características)

    PROBABILIDAD_PALABRAS = None   # Matriz de Nx3, donde N es la cantidad de palabras del diccionario
                                        # La 1era columna es la palabra en cuestión
                                        # La 2da  columna es la probabilidad de que la palabra se encuentre en un mensaje SPAM
                                        # La 3era columna es la probabilidad de que la palabra se encuentre en un mensaje HAM
                                        
    PI_SPAM = None                 # La probabilidad de que, dentro del dataset de entrenamiento, un mensaje sea SPAM
    PI_HAM = None                  # La probabilidad de que, dentro del dataset de entrenamiento, un mensaje sea HAM

    DATASET_ORIGINAL = None        # Es el dataset original, etiqueta y mensaje, respectivente



def entrenar_clasificador():
    path = os.path.dirname(os.path.abspath(__file__)) 
    # PREPARANDO EL DATASET
    df = pd.read_csv(path+'/SMSSpamCollection', 
                    sep='\\t', 
                    names=['etiqueta','mensaje'],
                    engine='python')
    # Seteamos el Dataset original
    Clasificador.DATASET_ORIGINAL = df
    df = df.replace('\d+', 'number', regex=True)
    df = df.apply(lambda x: x.astype(str).str.lower()) # To lower case
    df['mensaje'] = df['mensaje'].str.replace('http\S+|www.\S+', 'httpaddr', case=False) # Reemplazamos urls
    df['mensaje'] = df['mensaje'].replace('\d+', ' number ', regex=True) # Reemplazamos los números
    df['mensaje'] = df['mensaje'].replace('[,.;@#?!&$]+', '', regex=True) # Eliminamos los símbolos
    msj_entrenar, msj_test, etiqueta_entrenar, etiqueta_test = train_test_split(df['mensaje'], df['etiqueta'], random_state=1)
    cont = CountVectorizer()
    cont.fit(msj_entrenar)
    palabras=cont.get_feature_names()
    arr_palabras=cont.transform(msj_entrenar).toarray()
    matriz_frecuen=pd.DataFrame(data=arr_palabras,columns=palabras)
    arr=np.ndarray(dtype=np.int32, shape=(1, len(matriz_frecuen.keys())))
    for i, palabra in enumerate(matriz_frecuen):
        arr.itemset(i, sum(matriz_frecuen[palabra]))
    arr = np.ravel(arr)
    data=pd.DataFrame({'palabra' : palabras , 'ocurrencia':arr})
    data = data[~data['palabra'].isin(STOP_WORDS)]
    data_ordenada=data.sort_values(by='ocurrencia', ascending=False)
    Clasificador.DICCIONARIO=data_ordenada.head(3000)
    
    # INICIO DE ENTRENAMIENTO
    entrenamiento=pd.DataFrame({'mensaje' : msj_entrenar , 'etiqueta':etiqueta_entrenar})
    spam=entrenamiento[entrenamiento['etiqueta'] =='spam']['mensaje']
    ham=entrenamiento[entrenamiento['etiqueta'] =='ham']['mensaje']
    conts=CountVectorizer()
    lista_palabras_aux = Clasificador.DICCIONARIO['palabra']

    # Para SPAM
    conts.fit(spam)
    pspam=conts.get_feature_names()
    arr_pspam=conts.transform(spam).toarray()
    mf_spam=pd.DataFrame(data=arr_pspam,columns=pspam)
    mf_spam_actualizado = np.ndarray(dtype=np.int64, shape=(1,len(Clasificador.DICCIONARIO)))
    for i, palabra in enumerate(lista_palabras_aux):
        if palabra in mf_spam:
            mf_spam_actualizado.itemset(i, sum(mf_spam[palabra]))
        else:
            mf_spam_actualizado.itemset(i, 0)
    mf_spam_actualizado = np.ravel(mf_spam_actualizado)

    # Para HAM
    conts.fit(ham)
    pham=conts.get_feature_names()
    arr_pham=conts.transform(ham).toarray()
    mf_ham=pd.DataFrame(data=arr_pham,columns=pham)
    mf_ham_actualizado = np.ndarray(dtype=np.int64, shape=(1,len(Clasificador.DICCIONARIO)))
    for i, palabra in enumerate(lista_palabras_aux):
        if palabra in mf_ham:
            mf_ham_actualizado.itemset(i, sum(mf_ham[palabra]))
        else:
            mf_ham_actualizado.itemset(i, 0)
    mf_ham_actualizado = np.ravel(mf_ham_actualizado)
    mf_ham_diccionario = pd.DataFrame({'palabra':np.array(lista_palabras_aux), 'ocurrencia':mf_ham_actualizado})
    
    # Aplicación de las probabilidades
    a=0.001
    l=len(Clasificador.DICCIONARIO)
    p=sum(mf_ham_actualizado)
    probh = np.ndarray(dtype=np.float, shape=(1,l))
    for i in range(0,len(mf_ham_actualizado)):
        probh.itemset(i,(mf_ham_actualizado[i]+a)/(p+(a*l)))
    p1=sum(mf_spam_actualizado)
    probs = np.ndarray(dtype=np.float, shape=(1,l))    
    for i in range(0,len(mf_spam_actualizado)):
        probs.itemset(i,(mf_spam_actualizado[i]+a)/(p+(a*l)))
    probs=np.ravel(probs)
    probh=np.ravel(probh)
    Clasificador.PROBABILIDAD_PALABRAS=pd.DataFrame({'Palabras':lista_palabras_aux,'Probabilidad_Spam':probs,'Probabilidad_Ham':probh})
    Clasificador.PI_HAM=len(mf_ham.index)/(len(mf_ham.index)+len(mf_spam.index))
    Clasificador.PI_SPAM=len(mf_spam.index)/(len(mf_ham.index)+len(mf_spam.index))

def freq(str): 
    str = str.split()          
    str2 = [] 
    for i in str: 
        if i not in str2:
            str2.append(i)  
    for i in range(0, len(str2)):
        str2[i]=(str2[i],str.count(str2[i]))
    return np.array(str2)

def freq_diccionario(str):
    freq_total = freq(str)
    freq_coincidentes = []
    arr_palabras_diccionario = np.array(Clasificador.DICCIONARIO["palabra"])
    for palabra, frecuencia in freq_total:
        if(palabra in arr_palabras_diccionario): # Palabra pertenece al diccionario
            freq_coincidentes.append((palabra, frecuencia))
    return freq_coincidentes

def convertir_string_clasificador(mensaje):
    # PROCESO DE CONVERSIÓN
    df1 = pd.DataFrame({"mensaje":[mensaje]})
    df1 = df1.apply(lambda x: x.astype(str).str.lower()) # To lower case
    df1 = df1['mensaje'].str.replace('http\S+|www.\S+', 'httpaddr', case=False) # Reemplazamos urls
    df1 = df1.replace('\d+', ' number ', regex=True) # Reemplazamos los números
    df1 = df1.replace('[,.;@#?!&$:_]+', '', regex=True) # Eliminamos los símbolos
    return list(df1)[0]

def MNB_PROB(mensaje):
    mensaje = convertir_string_clasificador(mensaje)
    nuevo_dic = freq_diccionario(mensaje) 
    probs= [0,0]
    for clase in range(0,2):
        probs[clase] = 0
        for idxd in range (0,len(nuevo_dic)):
            if clase == 0:
                pdp=Clasificador.PROBABILIDAD_PALABRAS[Clasificador.PROBABILIDAD_PALABRAS.Palabras==nuevo_dic[idxd][0]].Probabilidad_Spam.item()
            if clase == 1:
                pdp=Clasificador.PROBABILIDAD_PALABRAS[Clasificador.PROBABILIDAD_PALABRAS.Palabras==nuevo_dic[idxd][0]].Probabilidad_Ham.item() 
            power = np.log(1+ int(nuevo_dic[idxd][1])) 
            probs[clase]+=power*np.log(pdp)
        if clase == 0:
            pdc = Clasificador.PI_SPAM
        if clase == 1:
            pdc = Clasificador.PI_HAM
        probs[clase] +=  np.log(pdc)
    prob_posi = [0, 0]
    prob_posi[0] = -1/probs[0]
    prob_posi[1] = -1/probs[1]
    total_posi = prob_posi[0] + prob_posi[1]
    return [prob_posi[0]/total_posi, prob_posi[1]/total_posi]
