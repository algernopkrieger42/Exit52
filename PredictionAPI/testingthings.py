from datetime import datetime

import pandas as pd


def create_empty_and_save_df(file_name='empty_predictions.csv'):
    # Create an empty DataFrame with two columns: 'date' and 'prediction'
    df = pd.DataFrame(columns=['date', 'prediction'])

    # Save the DataFrame to a CSV file
    df.to_csv(file_name, index=False)
    print(f"Empty DataFrame saved to {file_name}")


def add_entry_to_csv(file_name, new_date, new_prediction):
    try:
        # Read the existing CSV into a DataFrame
        df = pd.read_csv(file_name)

        # Create a new DataFrame with the new entry
        new_row = pd.DataFrame({'date': [new_date], 'prediction': [new_prediction]})

        # Concatenate the new row with the existing DataFrame
        df = pd.concat([df, new_row], ignore_index=True)

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_name, index=False)
        print(f"Added new entry and saved to {file_name}")
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please provide a valid CSV file.")
    except Exception as e:
        print(f"An error occurred: {e}")




create_empty_and_save_df("Predictions24:25")


