
<img src="assets/ppgec.png" alt="drawing" width="200"/>

## Identificação
**Professor**: Diego Pinheiro, PhD

**Master's Student**: Pedro Natanael

**Course**: Network Science

**Task**: Final Project

# Analysis of Political Alliances and Community Detection in the Brazilian Senate Voting Network

## Abstract

The Brazilian Senate plays a pivotal role in shaping the nation’s legislative framework. Understanding the underlying dynamics of voting behavior and political alliances within the Senate is crucial for comprehending the broader political landscape. This research aims to analyze the voting patterns in the Brazilian Senate through advanced network analysis techniques, focusing on the detection of political communities and the examination of alliance patterns among political parties. By applying methods such as the Leiden algorithm for community detection and machine learning models for predictive analysis, this study seeks to simulate various political scenarios and anticipate shifts in alliances based on historical voting data.

### Background
The Brazilian Senate plays a crucial role in policy formulation and law approval. The analysis of voting networks can reveal hidden patterns of political alliances and influence blocks that may not be immediately apparent in a superficial analysis. Previous studies have explored the application of complex network analysis to understand voting behavior and political polarization in legislative bodies.

One relevant study is "Voting Behavior, Coalitions and Government Strength through a Complex Network Analysis" by Carlo Dal Maso et al., which examines the community structure in parliaments, focusing on the Italian Chamber of Deputies. This study introduces methods to measure party polarization, coalition cohesiveness, and government stability, providing a framework applicable to other legislative bodies, including the Brazilian Senate.

Another significant work is "An Approach for Probabilistic Modeling and Reasoning of Voting Networks", which discusses the use of probabilistic models to understand and predict voting behaviors in legislative networks. This research is particularly relevant for understanding the underlying dynamics of voting patterns and the formation of alliances.

Lastly, the study "Using Artificial Intelligence to Predict Legislative Votes in the United States Congress" demonstrates the potential of AI and machine learning in predicting legislative outcomes. Although focused on the U.S. Congress, the methodologies discussed offer valuable insights for similar applications in the Brazilian legislative context.

By building on these studies, the current research aims to detect and analyze the political communities formed through voting in the Brazilian Senate, with a focus on identifying patterns of alliances between political parties in significant votes. Additionally, it seeks to predict how these alliances may change under different political scenarios using simulation techniques and dynamic network analysis.

### Objectives

The primary objective of this research is to explore the formation and evolution of political alliances within the Brazilian Senate by applying advanced network analysis techniques. Specifically, this study aims to:

1. **Detect Political Communities**: Identify and analyze communities within the voting network of the Brazilian Senate, focusing on the dynamics of these communities over time.
   
2. **Understand Alliance Patterns**: Examine the patterns of alliances between political parties during key legislative votes, and determine how these alliances are influenced by political contexts such as government changes, crises, and electoral periods.
   
3. **Predict Future Alliances**: Utilize machine learning and probabilistic models to forecast the likelihood of future alliances and voting outcomes based on historical voting data and simulated political scenarios.
   
4. **Simulate Political Scenarios**: Implement dynamic network analysis to simulate various political scenarios (e.g., changes in government coalitions, political crises) and predict their impact on the stability and formation of political alliances.
   
5. **Evaluate Algorithmic Improvements**: Assess the effectiveness of different community detection algorithms, such as the Leiden algorithm, by testing variations and comparing their performance using metrics like modularity, NMI, and ARI.

### Methods

To achieve these objectives, the research employs a comprehensive methodology that integrates network science, machine learning, and political analysis. The key steps in the methodology are as follows:

1. **Data Collection**:
   - **Voting Data**: Extract voting records from the Brazilian Senate, focusing on key legislative periods and significant votes. Data is obtained from reliable sources such as "Base dos Dados."
   - **Political Context Data**: Gather information on political contexts, including government compositions, electoral cycles, and significant political events.

2. **Community Detection**:
   - **Algorithm Selection**: Apply the Leiden algorithm to detect communities within the voting network. The algorithm is chosen for its ability to uncover well-connected communities and is tested with different parameters to optimize detection.
   - **Algorithm Evaluation**: Compare the performance of the Leiden algorithm with other community detection methods (e.g., Louvain) using metrics such as modularity, NMI (Normalized Mutual Information), and ARI (Adjusted Rand Index).
   - **Temporal Analysis**: Conduct a temporal analysis to observe how communities evolve over time, particularly in response to political events.

3. **Alliance Analysis**:
   - **Network Construction**: Build a network where nodes represent political parties and edges represent alliances or voting similarities. Utilize metrics like Jaccard similarity to quantify the strength of alliances.
   - **Ideological Correlation**: Analyze the correlation between party ideologies and the formation of alliances using network metrics and statistical methods.
   - **Scenario Simulation**: Simulate various political scenarios (e.g., changes in government, crises) using dynamic network analysis to predict shifts in alliances and community structures.

4. **Machine Learning Models**:
   - **Model Training**: Train machine learning models, such as logistic regression and random forest, to predict the outcomes of future legislative votes based on historical data. The models will incorporate features such as party affiliations, historical voting behavior, and political context.
   - **Feature Engineering**: Develop and refine features based on the political context, party characteristics, and detected community structures.
   - **Model Evaluation**: Evaluate model performance using cross-validation and metrics such as accuracy, precision, recall, and F1-score.

5. **Simulation and Prediction**:
   - **Dynamic Network Simulation**: Implement simulations to model how changes in political scenarios (e.g., new coalitions, electoral periods) might affect future voting patterns and alliance formations.
   - **Predictive Analysis**: Use the trained models and simulated data to forecast potential changes in alliances and voting outcomes, providing insights into future legislative dynamics.

This comprehensive approach combines the strengths of network science, machine learning, and political analysis to provide a deep understanding of the Brazilian Senate's voting dynamics and offer predictive insights into future political alliances.

### Results
Summarize the main findings, including statistical significance, if applicable. Highlight any critical data points and trends observed.

### Conclusions
State the conclusions drawn from the results, emphasizing how they address the research problem. Discuss any implications for future research or practical applications.

### Keywords
Voting Networks, Community Detection, Political Alliances, Brazilian Senate, Dynamic Networks, Scenario Simulation

---

## Acknowledgments
Thanks to Professor Diego Pinheiro, PhD, for his support and guidance throughout the development of this project. Thanks also to "Base dos Dados" for providing the essential data for this analysis.

## References
1. Dal Maso, C., Pompa, G., Puliga, M., Riotta, G., & Chessa, A. (2014). Voting Behavior, Coalitions and Government Strength through a Complex Network Analysis. *PLOS ONE, 9*(12), e116046. https://doi.org/10.1371/journal.pone.0116046

2. Cardoso, D. O., Lima, W. P. C., Silva, G. G. V. L., & Assis, L. S. (2023). An Approach for Probabilistic Modeling and Reasoning of Voting Networks. *In: Proceedings of the 22nd International Conference on Computational Science (ICCS 2023),* Springer, Cham, pp. 74-89. https://doi.org/10.1007/978-3-031-36024-4_7

3. Bari, A., Brower, W., & Davidson, C. (2021). Using Artificial Intelligence to Predict Legislative Votes in the United States Congress. *2021 IEEE the 6th International Conference on Big Data Analytics (ICBDA)*, 56-60. https://doi.org/10.1109/ICBDA51983.2021.9403106
