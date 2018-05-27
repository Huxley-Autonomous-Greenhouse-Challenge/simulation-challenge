import pandas as pd
import os

cropOutput_filePath = os.path.join(os.getcwd(), 'cropModelOutput.csv')
climate_filePath = os.path.join(os.getcwd(), 'climateModelOutput.csv')
crop_data = pd.read_csv(cropOutput_filePath)
climate_data = pd.read_csv(climate_filePath)

print(crop_data)
print(climate_data)
