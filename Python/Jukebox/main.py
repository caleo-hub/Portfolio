import pandas as pd
from jukeboxClasses import *


df = pd.read_csv('defaultLibrary.csv')
albuns = []
albuns = set(df['Artist'])
print(albuns)


