import pandas as pd

def load_data():
    """Load the CSV data into DataFrames."""
    proposition_microdados = pd.read_csv('..\data\processed\proposicao_microdados.csv')
    proposition_tema = pd.read_csv('..\data\processed\proposicao_tema.csv')
    voting_object = pd.read_csv('..\data\processed/votacao_objeto.csv')
    voting_parliamentar = pd.read_csv('..\data\processed/votacao_parlamentar.csv')
    voting = pd.read_csv('..\data\processed/votacao.csv')
    
    return proposition_microdados, proposition_tema, voting_object, voting_parliamentar, voting

def rename_columns(proposition_microdados, voting_object):
    """Rename columns for consistency."""
    proposition_microdados.rename(columns={'data': 'proposition_date', 'ano': 'proposition_year'}, inplace=True)
    voting_object.rename(columns={'data': 'voting_date'}, inplace=True)

def join_tables(proposition_microdados, proposition_tema, voting_object, voting):
    """Join the tables based on the provided keys."""
    voting_analysis = proposition_microdados[['id_proposicao', 'proposition_year', 'proposition_date', 'sigla', 'tipo']]
    voting_analysis = voting_analysis.merge(proposition_tema[['id_proposicao', 'tema']], on='id_proposicao', how='left')
    voting_analysis = voting_analysis.merge(voting_object[['id_proposicao', 'id_votacao', 'voting_date']], on='id_proposicao', how='left')
    voting_analysis = voting_analysis.merge(voting[['id_votacao', 'sigla_orgao', 'aprovacao', 'voto_sim', 'voto_nao', 'voto_outro']], on='id_votacao', how='left')
    
    return voting_analysis

def process_voting_data(voting_analysis):
    """Process the voting data by converting and filtering."""
    # Convert 'voting_date' to datetime
    voting_analysis['voting_date'] = pd.to_datetime(voting_analysis['voting_date'], errors='coerce')
    
    # Create 'voting_year' extracting the year
    voting_analysis['voting_year'] = voting_analysis['voting_date'].dt.year
    
    # Remove nulls and convert 'voting_year' to int
    voting_analysis['voting_year'] = voting_analysis['voting_year'].fillna(0).astype(int)
    
    # Calculate total votes
    voting_analysis['total_votes'] = voting_analysis['voto_sim'] + voting_analysis['voto_nao'] + voting_analysis['voto_outro']
    
    # Filter votes with more than 200 total votes
    voting_analysis = voting_analysis[voting_analysis['total_votes'] > 200]
    
    # Filter for 'PLEN' or 'PLENARIO' in 'sigla_orgao'
    voting_analysis = voting_analysis[voting_analysis['sigla_orgao'].isin(['PLEN', 'PLENARIO'])]
    
    return voting_analysis

def evaluate_approval(row):
    """Replace NaN values in 'approval' column based on 'voto_sim' and 'voto_nao' comparison."""
    if pd.isna(row['aprovacao']):  # If 'approval' is NaN
        if row['voto_nao'] > row['voto_sim']:
            return 0  # Rejected
        else:
            return 1  # Approved
    else:
        return row['aprovacao']  # Keep the existing value if not NaN

def apply_evaluation(voting_analysis):
    """Apply the approval evaluation function and calculate vote percentages."""
    # Apply the function to replace NaN values in the 'approval' column
    voting_analysis['aprovacao'] = voting_analysis.apply(evaluate_approval, axis=1)

    # Calculate total votes
    total_votes = voting_analysis['voto_sim'] + voting_analysis['voto_nao'] + voting_analysis['voto_outro']

    # Calculate the percentage of 'voto_sim'
    voting_analysis['yes_vote_percentage'] = voting_analysis['voto_sim'] / total_votes

    return voting_analysis

def filter_polarized_votes(voting_analysis):
    """Filter polarized votes where the 'yes' vote percentage is between 40% and 60%."""
    polarized_votes = voting_analysis[(voting_analysis['yes_vote_percentage'] >= 0.4) & 
                                      (voting_analysis['yes_vote_percentage'] <= 0.6)]
    return polarized_votes

def export_to_csv(data, filename):
    """Export the DataFrame to a CSV file."""
    data.to_csv(filename, index=False)
    print(f"File '{filename}' successfully exported!")

def main():
    """Main function to run the analysis."""
    # Load data
    proposition_microdados, proposition_tema, voting_object, voting_parliamentar, voting = load_data()
    
    # Rename columns
    rename_columns(proposition_microdados, voting_object)
    
    # Join tables
    voting_analysis = join_tables(proposition_microdados, proposition_tema, voting_object, voting)
    
    # Process and filter data
    voting_analysis = process_voting_data(voting_analysis)
    
    # Apply approval evaluation and calculate percentages
    voting_analysis = apply_evaluation(voting_analysis)
    
    # Filter polarized votes
    polarized_votes = filter_polarized_votes(voting_analysis)
    
    # Export filtered data to CSV
    export_to_csv(polarized_votes, '../data/polarized_votes.csv')

if __name__ == "__main__":
    main()
