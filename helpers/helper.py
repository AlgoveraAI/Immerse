from io import StringIO
import pandas as pd

def read_file(b):

    s=str(b,'utf-8')

    data = StringIO(s) 

    df=pd.read_csv(data)
    
    return df