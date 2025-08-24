def load_data(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

def save_data(data, file_path):
    import pandas as pd
    data.to_csv(file_path, index=False)

def preprocess_data(data):
    # Example preprocessing: fill missing values
    return data.fillna(method='ffill')

def visualize_data(data, column):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 5))
    plt.plot(data[column])
    plt.title(f'Visualization of {column}')
    plt.xlabel('Index')
    plt.ylabel(column)
    plt.show()