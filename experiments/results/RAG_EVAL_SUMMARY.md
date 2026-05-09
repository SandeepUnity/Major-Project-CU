# RAG offline evaluation summary

| Artifact | Path |
|----------|------|
| Per-run CSV | `experiments/results/rag_eval_runs.csv` |
| Statistics JSON | `experiments/results/rag_eval_statistics.json` |
| Gold labels | `data/evaluation_gold.csv` |

## Conditions

- Compared **top_k = 3** vs **top_k = 5** on the same queries (paired design).

## Descriptive statistics

- Pairs **N** = 10
- Mean answer–reference embedding similarity (**top_k=3**): **0.9213**
- Mean answer–reference embedding similarity (**top_k=5**): **0.8975**
- Mean paired difference (**top_k_5 − top_k_3**): **-0.0238**

## Inference (paired)

- **Paired t-test** on similarities (top_k 5 vs 3): statistic = -1.3817, *p*-value = 0.200398
- **Wilcoxon signed-rank** on paired differences: statistic = 6.0000, *p*-value = 0.176296

## Chapter 7 reporting hints

- Embedding similarity proxies **semantic alignment** with the gold FAQ answer; cite limitations (no entailment judgment).
- For **true RAGAS** (faithfulness, etc.), replicate this batch under Linux/WSL2 with `pip install ragas` working, 
  then add a second exports file from `ragas.evaluate`.
- Increase **sample size** and add **multiple annotators** if you promise human-subjective evaluation.
