import pandas as pd
import matplotlib.pyplot as plt

def plot_community_graphs(csv_file):
    """
    Reads the CSV file containing deputy numbers per party, year, and community,
    and generates PNG graphs for each community showing the number of deputies
    over the years for the top 5 parties.

    Parameters:
    csv_file (str): Path to the CSV file.
    """
    # Read the data into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Transform the DataFrame from wide to long format
    df_long = pd.melt(df, id_vars=['party'], var_name='year_community', value_name='num_deputies')
    
    # Split the 'year_community' column into separate 'year' and 'community' columns
    df_long[['year', 'community']] = df_long['year_community'].str.split('_', expand=True)
    
    # Convert data types
    df_long['year'] = df_long['year'].astype(int)
    df_long['community'] = df_long['community'].astype(int)
    df_long['num_deputies'] = df_long['num_deputies'].astype(float)
    
    # Loop through each community to generate the graphs
    for community in [0, 1, 2]:
        # Filter data for the current community
        df_comm = df_long[df_long['community'] == community]
        
        # Calculate the total number of deputies per party in this community
        total_deputies_per_party = df_comm.groupby('party')['num_deputies'].sum()
        
        # Identify the top 5 parties based on the total number of deputies
        top5_parties = total_deputies_per_party.nlargest(5).index.tolist()
        
        # Filter the DataFrame to include only the top 5 parties
        df_top5 = df_comm[df_comm['party'].isin(top5_parties)]
        
        # Pivot the DataFrame to have years as the index and parties as columns
        df_pivot = df_top5.pivot(index='year', columns='party', values='num_deputies')
        
        # Plot the data
        plt.figure(figsize=(10, 6))
        df_pivot.plot(kind='line', marker='o')
        plt.title(f'Number of deputies belonging to community {community}')
        plt.xlabel('Years')
        plt.ylabel('Number of deputies')
        plt.legend(title='Party')
        plt.tight_layout()
        
        # Save the plot as a PNG file
        plt.savefig(f'community_{community}_top5_parties.png')
        plt.close()
