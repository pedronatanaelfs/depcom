
<img src="assets/ppgec.png" alt="drawing" width="200"/>

## Identificação
**Professor**: Diego Pinheiro, PhD

**Master's Student**: Pedro Natanael

**Course**: Network Science

**Task**: Final Project

# Analysis of Political Alliances and Community Detection in the Brazilian Congress Voting Network

## Abstract

Understanding how political alliances and voting patterns in the Brazilian Congress evolve over time is crucial for analyzing the ideological positioning of political parties, their loyalty to party lines, and the influence of the president's party on legislative behavior. This research seeks to address key questions about the political landscape in Brazil by examining the voting records of Congress using advanced network analysis techniques. The primary focus is on detecting communities within the voting network, analyzing the shifts in party alliances, and determining the extent to which ideological divides between the left, center, and right influence voting outcomes. Additionally, the project explores how different filtering methods and edge pruning techniques affect the quality of community detection.

### Background
The Brazilian Congress, as the legislative backbone of the country, influences key national policies. By analyzing voting networks, it is possible to observe deeper, often hidden, patterns of political alignment, party loyalty, and shifting ideological positions. Previous research has shown that network analysis can reveal these hidden patterns, but few studies have delved into long-term changes in the alignment of political parties within the Brazilian context.

One relevant work is "Voting Behavior, Coalitions and Government Strength through a Complex Network Analysis" by Carlo Dal Maso et al., which provides a method for detecting communities within legislative bodies based on voting patterns. Another significant study, "An Approach for Probabilistic Modeling and Reasoning of Voting Networks," applies probabilistic models to predict future voting behavior based on past patterns. These studies, combined with others that explore the role of AI in legislative prediction, lay the groundwork for a deeper analysis of the Brazilian Congress.

This research aims to explore how political alliances and party positions have shifted over time, particularly in response to changes in government leadership and broader political contexts. It also investigates methodological questions around how different filters and edge pruning strategies can optimize the detection of these communities.

### Objectives

The specific objectives of this research are as follows:

1. **Analyze Political Alignment Over Time:** Investigate the ideological shifts of political parties, especially those that claim to be centrist, and observe how their position has changed over the years relative to the left and right.

2. **Evaluate Political Influence:** Examine which political side (left or right) holds greater power in Congress and identify the parties whose deputies show the highest loyalty in voting.

3. **Impact of the President’s Party:** Assess whether the ruling party of the president influences the overall positioning of other parties in Congress during key legislative decisions.

4. **Optimize Community Detection:** Explore how filtering more polarized propositions affects the quality of community detection and assess which filtering methods are best suited for different political contexts.

5. **Improve Graph Pruning Methods:** Investigate how edge pruning influences the clarity and accuracy of detected political communities and how to automate the pruning process to optimize network analysis results.

### Methods

The methodology is structured into several key steps that involve data acquisition, processing, analysis of voting patterns, and visualization of political party positions over time. The steps are designed to optimize the detection of political communities and answer the core research questions regarding political alignment, loyalty, and the impact of government changes on alliances.

 Data Acquisition:

- The first step is to acquire voting data and political context information. The data includes voting records, deputies' details, and metadata on each proposition. This data is sourced primarily from Base dos Dados and other publicly available repositories.

2. Data Processing:

- After acquiring the raw data, it undergoes filtering and preprocessing to remove irrelevant or incomplete records. A critical part of this step involves filtering propositions to focus on the most polarized votes, which are more likely to reveal meaningful political divisions.

3. Prepare Voting Data:

- Remove duplicates from the dataset, ensuring each deputy is only listed once. This prepares the dataset for analysis of individual voting behavior and party alignment.

4. Optimize Polarization Interval and Perform Analysis:

- The critical analysis of this research involves optimizing the polarization interval of the voting data. This step identifies the propositions that exhibit the highest levels of polarization, which are essential for detecting distinct political communities and understanding party alignments.
  
- This function refines the dataset, focusing on votes where ideological divisions are most clear, which helps in detecting political communities and evaluating party loyalty and shifts over time.

5. Visualizing Political Alignment:

- After optimizing the polarization intervals, the next step involves visualizing how political parties have shifted over the years. Graphs will be plotted to show party alignment on a left-right spectrum, as well as how centrist parties have moved closer to the left or right over time.
  
- These visualizations will help answer questions such as "Which side of the political spectrum holds more influence?" and "How do parties that identify as centrist behave over time?"

6. Community Detection:

- The filtered voting data will be used to detect communities within the voting network. Community detection methods such as the Leiden algorithm will be applied to reveal clusters of political alliances.

- Parameters for the community detection algorithm will be tuned using metrics like modularity and NMI, ensuring that the results are both accurate and meaningful in the context of political behavior.

7. Answering Research Questions:

Throughout the analysis, specific steps will be taken to address the core questions:

- **Political Positioning:** Graphs of political alignment will show how parties have shifted over time, particularly focusing on centrist parties and their behavior.

- **Loyalty and Power:** Metrics will be calculated to determine which parties exhibit the highest loyalty and which side of the spectrum holds more power in Congress.

- **Influence of the President’s Party:** Temporal analysis will assess whether the party of the president affects the positioning and behavior of other parties.

- **Filtering and Pruning:** The research will also test how filtering polarized propositions and edge pruning can improve the detection of communities, optimizing both the accuracy and clarity of the detected political groups.

### Results
Summarize the main findings, including statistical significance, if applicable. Highlight any critical data points and trends observed.

### Conclusions
State the conclusions drawn from the results, emphasizing how they address the research problem. Discuss any implications for future research or practical applications.

### Keywords
Political Alliances, Community Detection, Brazilian Congress, Voting Networks, Party Loyalty, Dynamic Networks

---

## Acknowledgments
Thanks to Professor Diego Pinheiro, PhD, for his support and guidance throughout the development of this project. Thanks also to "Base dos Dados" for providing the essential data for this analysis.

## References
1. Dal Maso, C., Pompa, G., Puliga, M., Riotta, G., & Chessa, A. (2014). Voting Behavior, Coalitions and Government Strength through a Complex Network Analysis. *PLOS ONE, 9*(12), e116046. https://doi.org/10.1371/journal.pone.0116046

2. Cardoso, D. O., Lima, W. P. C., Silva, G. G. V. L., & Assis, L. S. (2023). An Approach for Probabilistic Modeling and Reasoning of Voting Networks. *In: Proceedings of the 22nd International Conference on Computational Science (ICCS 2023),* Springer, Cham, pp. 74-89. https://doi.org/10.1007/978-3-031-36024-4_7

3. Bari, A., Brower, W., & Davidson, C. (2021). Using Artificial Intelligence to Predict Legislative Votes in the United States Congress. *2021 IEEE the 6th International Conference on Big Data Analytics (ICBDA)*, 56-60. https://doi.org/10.1109/ICBDA51983.2021.9403106
