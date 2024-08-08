import pandas as pd

csv_file = 'selected_few_shot_pipeline/results/test.csv'  

data = pd.read_csv(csv_file)

coders = ['ty_binary_label', 'will_binary_label', 'llm_label'] 


def calculate_cohen_kappa(coders_data, coder1, coder2):
    labels1 = coders_data[coder1]
    labels2 = coders_data[coder2]
    n = len(labels1)

    # Calculate observed agreement
    observed_agreement = sum(1 for a, b in zip(labels1, labels2) if a == b) / n

    # Calculate expected agreement
    categories = sorted(set(labels1) | set(labels2))
    expected_agreement = 0
    for category in categories:
        p1 = sum(1 for a in labels1 if a == category) / n
        p2 = sum(1 for b in labels2 if b == category) / n
        expected_agreement += p1 * p2

    kappa = (observed_agreement - expected_agreement) / (1 - expected_agreement)
    return kappa

def calculate_reliability(coders_data, coder_to_remove):
    remaining_coders = [coder for coder in coders_data.columns if coder != coder_to_remove]
    kappa_scores = []
    for i in range(len(remaining_coders)):
        for j in range(i + 1, len(remaining_coders)):
            kappa = calculate_cohen_kappa(coders_data, remaining_coders[i], remaining_coders[j])
            kappa_scores.append(kappa)
    return kappa_scores

for coder in coders:
    print(f"\nRemoving {coder}:")
    kappa_scores = calculate_reliability(data[coders], coder)
    average_kappa = sum(kappa_scores) / len(kappa_scores)
    print(f"Cohen's Kappa Scores: {kappa_scores}")
    print(f"Average Cohen's Kappa: {average_kappa}")