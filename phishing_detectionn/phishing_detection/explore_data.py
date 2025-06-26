import pandas as pd

data = pd.read_csv('phishing_dataset.csv')

print("Dimensions du dataset :", data.shape)
print("\nColonnes :\n", data.columns)
print("\nAperçu des données :\n", data.head())
print("\nRépartition des classes :\n", data['Result'].value_counts())

