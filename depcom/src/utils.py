def determine_optimal_pruning(results):
    """
    Determines the optimal pruning percentage based on the criteria:
    - Minimum number of communities detected greater than one
    - Maximum modularity value

    Args:
        results (list): List of dictionaries containing pruning analysis results.

    Returns:
        float: The optimal pruning percentage.
    """
    # Filter results where number of communities > 1
    valid_results = [res for res in results if res['num_communities'] > 1]

    if not valid_results:
        print("No valid pruning percentage found where number of communities > 1.")
        return None

    # Find the minimum number of communities greater than one
    min_num_communities = min(res['num_communities'] for res in valid_results)

    # Filter results with the minimum number of communities
    min_community_results = [res for res in valid_results if res['num_communities'] == min_num_communities]

    # Find the maximum modularity among these results
    max_modularity = max(res['modularity'] for res in min_community_results)

    # Select the result with maximum modularity
    optimal_results = [res for res in min_community_results if res['modularity'] == max_modularity]

    # If multiple results have the same modularity, pick the one with the lowest pruning percentage
    optimal_result = min(optimal_results, key=lambda x: x['pruning_percentage'])

    optimal_pruning_percentage = optimal_result['pruning_percentage']
    print(f"Optimal pruning percentage determined: {optimal_pruning_percentage}%")
    return optimal_pruning_percentage
