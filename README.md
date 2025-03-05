

# Analysis of Political Alliances and Community Detection in the Brazilian Congress Voting Network

## Abstract

This study explores the use of network theory to analyze voting patterns in the Brazilian Congress from 2003 to 2023, applying advanced techniques such as the Leiden algorithm for community detection. By focusing on polarized propositions and iterative edge pruning, the research aims to enhance the clarity and modularity of detected political communities. Results reveal distinct ideological divides, shifts in party alignment, and the role of centrist parties as swing actors over time. The study contributes to both political science and Information Systems by demonstrating how network analysis can be applied to complex political systems.

### Background
The analysis of voting patterns using network theory has become increasingly prevalent in legislative studies, as it provides insights into hidden alliances and ideological shifts within political systems. Understanding these alliances is particularly relevant in democratic systems, where the evolution of political blocs can influence legislative outcomes and party behavior​.

Previous studies have applied network analysis to voting data, constructing political networks where nodes represent parliamentarians and edges reflect voting similarities. For example, Cherepnalkoski et al. (2016) combined roll-call votes and social media data to analyze cohesion and coalition formation in the European Parliament, revealing ideological alignments and shifts​. Similarly, Dal Maso et al. (2014) explored voting behavior in Italy, demonstrating how complex network analysis can identify party cohesion and detect ideological shifts​. In Brazil, Medeiros Brito et al. (2020) proposed a network-based approach for analyzing the Chamber of Deputies' voting data, identifying coalition patterns and party isolation before significant political events​.

While these studies provide valuable insights, they often include non-polarized propositions, which weakens the detection of clear ideological divides. Such limitations result in networks cluttered with weak connections that obscure meaningful political alliances, ultimately reducing modularity scores and hindering accurate community detection. Additionally, most methods do not incorporate edge pruning techniques to remove irrelevant edges, further diluting the clarity of detected communities​.

To address these challenges, this study focuses on improving community detection within the Brazilian Congress’ voting network. By applying the Leiden algorithm, a method known for its efficiency and accuracy in detecting cohesive communities and incorporating techniques like edge pruning and polarized proposition filtering, the research aims to enhance modularity and offer a clearer analysis of political dynamics. This approach aligns with Levorato and Frota’s (2017) findings, which highlighted the importance of community detection for understanding political behavior and party discipline within legislative bodies. Furthermore, the study builds on Ferreira et al. (2018), who demonstrated that focusing on polarized votes could improve the visibility of ideological divides in voting networks.

By refining the network structure through advanced techniques, this research aims to uncover the evolution of political alliances in Brazil, offering a more precise understanding of party behavior, loyalty, and shifts in ideological positions over time​.

### Objectives

**General Objective:** To analyze political alliances and detect communities within the Brazilian Congress voting network using advanced network analysis techniques.
**Specific Objectives:**
- Apply the Leiden algorithm to identify ideological divides.
- Improve community detection by filtering polarized propositions and applying edge pruning techniques.
- Track the temporal evolution of political communities and analyze shifts in alliances.
- Assess the role of centrist parties as swing actors within the voting network.

**Research Question:** How can advanced network analysis techniques improve the detection and understanding of political alliances in the Brazilian Congress?

### Methods

The methodology is structured into several key steps that involve data acquisition, processing, analysis of voting patterns, and visualization of political party positions over time. The steps are designed to optimize the detection of political communities and answer the core research questions regarding political alignment, loyalty, and the impact of government changes on alliances.

**Research Design**

Quantitative and descriptive approach focused on analyzing voting patterns in the Brazilian Congress.
The study aims to identify political alliances and ideological shifts using network analysis.

**Data Collection**

Data sourced from public voting records of the Brazilian Chamber of Deputies, covering the period from 2003 to 2023.
Voting data includes votes labeled as "Yes," "No," or "Abstain," mapped to numerical values (1, -1, and 0, respectively).
Preprocessing includes filtering for polarized propositions to enhance the clarity of ideological divisions.

**Graph Generation Process**

Construction of an adjacency matrix representing voting similarity between deputies.
Similarity calculated using a dot product of voting vectors, with normalization applied to ensure comparability across graphs.
NetworkX library used to create the graph, with nodes representing deputies and edges representing voting similarity.

**Community Detection**

Application of the Leiden Algorithm for detecting communities within the voting network.
The algorithm starts by considering each node as its own community, iteratively moving nodes to maximize network modularity.
Community structure is refined until no further gains in modularity can be achieved.

**Advanced Network Analysis Techniques**

Polarized Proposition Filtering: Propositions are progressively filtered based on the percentage of "Yes" votes, narrowing down the range to find the highest modularity.
Edge Pruning: Weaker edges are incrementally removed in 2% steps to refine the network structure. The pruning process continues until an optimal modularity is reached.
Maintaining Connectivity: To prevent nodes from becoming disconnected, at least one edge per node is retained.

**Ensuring Consistency of Communities Over Time**

A reference year is selected to establish consistent labeling of communities throughout the timeline.
Community labels are adjusted based on the highest overlap in party composition, allowing meaningful temporal comparisons.
Smaller, less significant communities are excluded to focus on major political blocs.

**Evaluation Metrics**

**Modularity:** The primary metric used to evaluate the strength of community division within the network.

The Leiden algorithm iteratively optimizes modularity, ensuring the detected communities accurately reflect the underlying voting patterns.

### Results
Summarize the main findings, including statistical significance, if applicable. Highlight any critical data points and trends observed.

### Conclusions
State the conclusions drawn from the results, emphasizing how they address the research problem. Discuss any implications for future research or practical applications.

### Keywords
Leiden Algorithm, Network Modularity, Political Polarization, Edge Pruning, Temporal Analysis.

---

## Acknowledgments
Thanks to Professor Diego Pinheiro, PhD, for his support and guidance throughout the development of this project. Thanks also to "Base dos Dados" for providing the essential data for this analysis.

## References
Cherepnalkoski, D., Karpf, A., Mozetič, I., & Grčar, M. (2016). Cohesion and coalition formation in the European Parliament: Roll-call votes and Twitter activities. PLoS ONE, 11(11), e0166586. https://doi.org/10.1371/journal.pone.0166586

Dal Maso, C., Pompa, G., Puliga, M., Riotta, G., & Chessa, A. (2014). Voting behavior, coalitions, and government strength through a complex network analysis. PLoS ONE, 9(12), e116046. https://doi.org/10.1371/journal.pone.0116046

Ferreira, C. H. G., de Sousa Matos, B., & Almeira, J. M. (2018). Analyzing dynamic ideological communities in congressional voting networks. In International Conference on Social Informatics (pp. 257–273). Springer. https://doi.org/10.1007/978-3-030-01129-1_16

Levorato, M., & Frota, Y. (2017). Brazilian Congress structural balance analysis. Journal of Interdisciplinary Methodologies and Issues in Science, 2, 1–18.

Medeiros Brito, A. C., Nascimento Silva, F., & Amancio, D. R. (2020). A complex network approach to political analysis: Application to the Brazilian Chamber of Deputies. PLoS ONE, 15(3), e0229928. https://doi.org/10.1371/journal.pone.0229928
