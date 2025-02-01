import os
import numpy as np
import pandas as pd
class GreyModel:
    def __init__(self):
        self.a = None
        self.b = None
        self.x0 = None  
        self.x1 = None  
    def fit(self, data):
        self.x0 = data
        self.x1 = np.cumsum(data)
        B = np.array([-0.5*(self.x1[i-1] + self.x1[i]) for i in range(1, len(self.x1))])
        B = np.column_stack((B, np.ones(len(B))))
        Y = self.x0[1:]
        params = np.linalg.inv(B.T @ B) @ B.T @ Y
        self.a, self.b = params
        
    def predict(self, n):
        x1_pred = [self.x1[0]]
        for k in range(1, len(self.x0) + n):
            x1_k = (self.x0[0] - self.b/self.a) * np.exp(-self.a*(k)) + self.b/self.a
            x1_pred.append(x1_k)
        x0_pred = np.diff(x1_pred)
        return x0_pred[-n:]  

def process_files():
    input_folder = "rawData"
    output_folder = "2011-2021"
    os.makedirs(output_folder, exist_ok=True)
    file_names = [
        "10-14_years.csv", "15-19_years.csv", "20-24_years.csv",
        "25-29_years.csv", "30-34_years.csv", "35-39_years.csv",
        "40-44_years.csv", "45-49_years.csv", "5-9_years.csv",
        "50-54_years.csv", "55-59_years.csv", "60-64_years.csv",
        "65-69_years.csv", "70-74_years.csv", "75-79_years.csv",
        "80-84_years.csv", "85-89_years.csv", "90-94_years.csv",
        "95plus_years.csv", "less_5_years.csv"
    ]
    
    for file_name in file_names:
        df = pd.read_csv(os.path.join(input_folder, file_name))
        values = df['value'].values 
        
        train_data = values[:31]  
        test_data = values[31:]  
        model = GreyModel()
        model.fit(train_data)
        predictions = model.predict(len(test_data))
        result_df = pd.DataFrame({
            'year': df['year'][31:],
            'true_value': test_data,
            'predicted_value': predictions
        })
        output_path = os.path.join(output_folder, f"result_{file_name}")
        result_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    process_files()