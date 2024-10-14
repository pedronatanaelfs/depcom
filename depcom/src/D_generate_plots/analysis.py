import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def load_detailed_results(detailed_results_path):
    """
    Carrega os resultados detalhados de um arquivo CSV.

    Args:
        detailed_results_path (str): Caminho para o arquivo 'detailed_results.csv'.

    Returns:
        pd.DataFrame: DataFrame contendo os resultados detalhados.
    """
    if not os.path.exists(detailed_results_path):
        raise FileNotFoundError(f"O arquivo {detailed_results_path} não foi encontrado.")
    
    try:
        df = pd.read_csv(detailed_results_path)
        print(f"Arquivo {detailed_results_path} carregado com sucesso.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo {detailed_results_path}: {e}")
        return None

def select_optimal_modularity(df_detailed):
    """
    Para cada ano e faixa de polarização, seleciona a modularidade máxima
    entre as entradas com o menor número de comunidades detectadas.

    Args:
        df_detailed (pd.DataFrame): DataFrame contendo os resultados detalhados.

    Returns:
        pd.DataFrame: DataFrame com a modularidade otimizada para cada ano e faixa de polarização.
    """
    # Verificar se o DataFrame está vazio
    if df_detailed.empty:
        print("O DataFrame está vazio. Não é possível realizar a seleção.")
        return None

    # Inicializar uma lista para armazenar os resultados otimizados
    optimized_results = []

    # Obter todos os anos e faixas de polarização únicas
    anos = df_detailed['Year'].unique()
    faixas_polarizacao = df_detailed['Polarization Range'].unique()

    for ano in anos:
        for faixa in faixas_polarizacao:
            # Filtrar os dados para o ano e faixa de polarização atual
            df_subset = df_detailed[(df_detailed['Year'] == ano) & 
                                     (df_detailed['Polarization Range'] == faixa)]
            
            if df_subset.empty:
                continue

            # Encontrar o menor número de comunidades detectadas
            min_comunidades = df_subset['Number of Communities'].min()

            # Filtrar as entradas que possuem o menor número de comunidades
            df_min_comunidades = df_subset[df_subset['Number of Communities'] == min_comunidades]

            # Selecionar a entrada com a maior modularidade entre as filtradas
            max_modularidade = df_min_comunidades['Modularity'].max()
            df_otimo = df_min_comunidades[df_min_comunidades['Modularity'] == max_modularidade].iloc[0]

            # Adicionar os resultados otimizados à lista
            optimized_results.append({
                'Year': ano,
                'Polarization Range': faixa,
                'Optimal Pruning Percentage (%)': df_otimo['Pruning Percentage (%)'],
                'Number of Communities': df_otimo['Number of Communities'],
                'Modularity': df_otimo['Modularity']
            })

    # Converter a lista de resultados otimizados em um DataFrame
    df_optimized = pd.DataFrame(optimized_results)
    return df_optimized

def plot_modularity_vs_polarization(df_optimized, output_path=None):
    """
    Gera um gráfico que mostra como a modularidade otimizada varia de acordo com a faixa de seleção
    de proposições polarizadas para cada ano.

    Args:
        df_optimized (pd.DataFrame): DataFrame contendo os resultados otimizados.
        output_path (str, optional): Caminho para salvar o gráfico. Se None, o gráfico será exibido.
    """
    # Verificar se o DataFrame está vazio
    if df_optimized.empty:
        print("O DataFrame está vazio. Não é possível gerar o gráfico.")
        return
    
    # Ordenar as faixas de polarização
    polarizacao_order = [f"{i}-{100-i}" for i in range(0, 50, 10)]
    df_optimized['Polarization Range'] = pd.Categorical(df_optimized['Polarization Range'], 
                                                       categories=polarizacao_order,
                                                       ordered=True)
    df_optimized = df_optimized.sort_values(['Polarization Range', 'Year'])
    
    # Configurar o estilo dos gráficos
    sns.set(style="whitegrid")
    
    plt.figure(figsize=(16, 10))  # Aumentar o tamanho para acomodar mais legendas
    
    # Plotar para cada ano
    sns.lineplot(
        data=df_optimized,
        x='Polarization Range',
        y='Modularity',
        hue='Year',
        marker='o',
        palette='tab20',  # Usar uma paleta com muitas cores
        linewidth=2.5
    )
    
    plt.title('Variação da Modularidade com a Faixa de Polarização das Proposições por Ano', fontsize=18)
    plt.xlabel('Faixa de Polarização das Proposições (%)', fontsize=16)
    plt.ylabel('Modularidade Otimizada', fontsize=16)
    
    # Ajustar a legenda para acomodar todos os anos
    plt.legend(title='Ano', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    
    plt.tight_layout()
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path, dpi=300)
        print(f"Gráfico salvo em {output_path}")
    else:
        plt.show()

def generate_all_plots(detailed_results_path, plots_output_dir):
    """
    Função principal para gerar todos os gráficos desejados.

    Args:
        detailed_results_path (str): Caminho para o arquivo 'detailed_results.csv'.
        plots_output_dir (str): Diretório onde os gráficos serão salvos.
    """
    # Carregar os dados detalhados
    df_detailed = load_detailed_results(detailed_results_path)
    
    # Verificar se os dados foram carregados corretamente
    if df_detailed is None:
        print("Falha ao carregar os dados detalhados. Encerrando a geração de gráficos.")
        return
    
    # Criar a coluna 'Polarization Range' se ainda não existir
    if 'Polarization Range' not in df_detailed.columns:
        df_detailed['Polarization Range'] = df_detailed['Polarization Lower Bound (%)'].astype(str) + "-" + df_detailed['Polarization Upper Bound (%)'].astype(str)
    
    # Selecionar a modularidade otimizada para cada ano e faixa de polarização
    df_optimized = select_optimal_modularity(df_detailed)
    
    if df_optimized is None or df_optimized.empty:
        print("Nenhum dado otimizado disponível para gerar o gráfico.")
        return
    
    # Criar o diretório de saída se não existir
    os.makedirs(plots_output_dir, exist_ok=True)
    
    # Gerar o gráfico de Modularidade vs Faixa de Polarização
    plot_path = os.path.join(plots_output_dir, "modularity_vs_polarization.png")
    plot_modularity_vs_polarization(df_optimized, output_path=plot_path)
    
    print("Gráficos foram gerados e salvos com sucesso.")