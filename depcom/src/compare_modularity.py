import pandas as pd
import matplotlib.pyplot as plt
import os

def compare_modularities(detailed_results_file, results_summary_file, output_dir='data/comparisons'):
    """
    Compara a modularidade entre a modularidade inicial (Polarization Lower Bound = 0, Upper Bound = 100, Pruning = 0)
    e a modularidade otimizada para cada ano. Gera um gráfico de barras e exporta os dados em uma tabela CSV,
    além de calcular a melhoria média entre as modularidades e a média da modularidade inicial.
    
    Args:
        detailed_results_file (str): Caminho para o arquivo 'detailed_results.csv'.
        results_summary_file (str): Caminho para o arquivo 'results_summary.csv'.
        output_dir (str, optional): Diretório para salvar o gráfico e a tabela gerada. Padrão é 'data/comparisons'.
    """
    # Verificar se os arquivos existem
    if not os.path.exists(detailed_results_file) or not os.path.exists(results_summary_file):
        print("Erro: Arquivos não encontrados. Verifique os caminhos fornecidos.")
        return

    # Ler os arquivos CSV
    detailed_df = pd.read_csv(detailed_results_file)
    summary_df = pd.read_csv(results_summary_file)

    # Filtrar o detailed_results para obter a modularidade inicial (Polarization Lower Bound = 0, Upper Bound = 100, Pruning = 0)
    detailed_filtered = detailed_df[
        (detailed_df['Polarization Lower Bound (%)'] == 0) &
        (detailed_df['Polarization Upper Bound (%)'] == 100) &
        (detailed_df['Pruning Percentage (%)'] == 0)
    ][['Year', 'Modularity']]

    # Renomear a coluna da modularidade para 'Initial Modularity'
    detailed_filtered = detailed_filtered.rename(columns={'Modularity': 'Initial Modularity'})

    # Selecionar as colunas necessárias do results_summary (Year e Modularity)
    summary_filtered = summary_df[['Year', 'Modularity']]
    summary_filtered = summary_filtered.rename(columns={'Modularity': 'Optimized Modularity'})

    # Juntar os dois DataFrames com base no ano
    comparison_df = pd.merge(detailed_filtered, summary_filtered, on='Year', how='inner')

    # Calcular a diferença de modularidade e a melhoria percentual
    comparison_df['Difference'] = comparison_df['Optimized Modularity'] - comparison_df['Initial Modularity']
    comparison_df['Improvement (%)'] = (comparison_df['Difference'] / comparison_df['Initial Modularity']) * 100

    # Exportar a tabela de comparação
    os.makedirs(output_dir, exist_ok=True)
    table_output_path = os.path.join(output_dir, 'modularity_comparison_table.csv')
    comparison_df.to_csv(table_output_path, index=False)
    print(f"Comparison table saved to {table_output_path}")

    # Calcular as médias
    avg_initial_modularity = comparison_df['Initial Modularity'].mean()
    avg_difference = comparison_df['Difference'].mean()
    avg_improvement_percent = comparison_df['Improvement (%)'].mean()

    print(f"Average Initial Modularity: {avg_initial_modularity:.4f}")
    print(f"Average Difference in Modularity: {avg_difference:.4f}")
    print(f"Average Improvement (%): {avg_improvement_percent:.2f}%")

    # Plotar o gráfico de barras comparativo
    plt.figure(figsize=(12, 6))

    years = comparison_df['Year']
    initial_modularities = comparison_df['Initial Modularity']
    optimized_modularities = comparison_df['Optimized Modularity']

    bar_width = 0.35
    index = range(len(years))

    # Barras para modularidade inicial
    plt.bar(index, initial_modularities, bar_width, label='Initial Modularity', color='blue')

    # Barras para modularidade otimizada
    plt.bar([i + bar_width for i in index], optimized_modularities, bar_width, label='Optimized Modularity', color='green')

    # Configurações do gráfico
    plt.xlabel('Year')
    plt.ylabel('Modularity')
    plt.title('Comparison of Initial vs Optimized Modularity by Year')
    plt.xticks([i + bar_width / 2 for i in index], years, rotation=45)
    plt.legend()

    # Salvar o gráfico
    graph_output_path = os.path.join(output_dir, 'modularity_comparison.png')
    plt.tight_layout()
    plt.savefig(graph_output_path, dpi=300)
    plt.close()

    print(f"Graph saved to {graph_output_path}")

# Exemplo de uso
detailed_results_file = 'data/detailed_results.csv'
results_summary_file = 'data/results_summary.csv'
compare_modularities(detailed_results_file, results_summary_file)
