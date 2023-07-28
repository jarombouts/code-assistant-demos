import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_titanic_dataset(file_path):
    """
    Load the Titanic dataset from a CSV file into a Pandas DataFrame.

    Parameters:
        file_path (str): The path to the CSV file containing the dataset.

    Returns:
        pandas.DataFrame: The Titanic dataset as a DataFrame.
    """
    df = pd.read_csv(file_path)
    return df


def visualize_age_distribution(df):
    """
    Visualize the distribution of passenger ages in the Titanic dataset.

    Parameters:
        df (pandas.DataFrame): The Titanic dataset as a DataFrame.
    """
    plt.figure(figsize=(8, 6))
    sns.histplot(df["Age"], bins=20, kde=True)
    plt.xlabel("Age")
    plt.ylabel("Count")
    plt.title("Age Distribution of Passengers")
    plt.show()

def extract_ticket_prefix(df):
    df['Ticket Prefix'] = df['Ticket'].apply(lambda ticket: ticket.split()[0] if len(ticket.split()) > 1 else 'No Prefix')
    return df


def family_survival_info(df):
    df['Last Name'] = df['Name'].apply(lambda name: name.split(',')[0])
    df['Family Survival'] = 0.5

    for _, grp_df in df.groupby('Last Name'):
        if len(grp_df) > 1:
            family_ids = set(grp_df['Ticket'].values)
            if grp_df['Survived'].notnull().sum() > 0:
                for idx, passenger in grp_df.iterrows():
                    num_family_members = grp_df.loc[grp_df['Ticket'] == passenger['Ticket']].shape[0]
                    if num_family_members > 1:
                        df.loc[idx, 'Family Survival'] = 1.0 if grp_df['Survived'].max() == 1 else 0.0
    return df
