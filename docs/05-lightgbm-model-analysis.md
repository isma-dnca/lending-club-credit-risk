# LightGBM — Threshold Analysis

## Why LightGBM

The previous results with Logistic Regression left two possible directions:

- **Path 1:** Keep adjusting thresholds and class weights  
  --> small incremental improvements, limited impact.

- **Path 2:** Move to a more powerful model better suited for tabular data  
  --> more impactful, more realistic for this kind of problem.

Path 2 is the more effective approach, so I moved to **LightGBM**.

---

## Quick Recap — What is LightGBM

LightGBM is a gradient boosting model based on decision trees.

Key points:
- builds trees sequentially, each one correcting the errors of the previous
- handles non-linear relationships naturally
- performs well on large tabular datasets
- faster and more memory efficient than most alternatives

Unlike Logistic Regression, it does not assume that classes are linearly separable.

---

## Key Result — AUC Improvement

The most important number here is AUC-ROC:

- Logistic Regression --> **0.59**
- LightGBM --> **0.67**

This is a real improvement. It means LightGBM is genuinely better at 
separating risky from safe clients, independently of any threshold choice.
Not perfect, but no longer borderline useless.

---

## Threshold Comparison

Several thresholds were tested to understand how the model behaves 
under different decision policies.

Important to keep in mind:
- the model itself does not change between thresholds
- only the decision boundary changes
- AUC-ROC stays at 0.67 across all thresholds for this reason

---

### Threshold = 0.2 — Aggressive Detection

At t = 0.2, we are telling the model to flag a client as risky 
even if it is only 20% sure.

As a result we get:
- **Recall = 0.63** --> the model catches 63% of truly risky clients
- **Precision = 0.29** --> out of everyone it flags as risky, only 29% actually are

The model casts a wide net. It would rather over-warn than miss someone risky.
More real defaulters caught, but also more false alarms.

This threshold makes sense when missing a risky client is more costly 
than investigating a few false alarms.

---

### Threshold = 0.3 — Moderate Detection

At t = 0.3, the model requires slightly more confidence before flagging a client.

As a result we get:
- **Recall = 0.28** --> the model catches 28% of truly risky clients
- **Precision = 0.37** --> out of everyone it flags as risky, 37% actually are

The net gets narrower. Fewer false alarms, but more real defaulters slip through.
Recall drops significantly compared to t = 0.2.

This threshold works only if missing some risky clients is acceptable.

---

### Threshold = 0.4 — Conservative Detection

At t = 0.4, the model becomes very selective about who it flags.

As a result we get:
- **Recall = 0.08** --> the model catches only 8% of truly risky clients
- **Precision = 0.44** --> out of everyone it flags as risky, 44% actually are

Precision improves slightly, but recall collapses. The model is now 
missing 92% of real defaulters. For a credit risk use case, this is 
not an acceptable trade-off.

---

### Threshold = 0.5 — Near-Blind Detection

At t = 0.5, the default classification boundary, the model requires 
50% confidence before flagging anyone.

As a result we get:
- **Recall = 0.01** --> the model catches only 1% of truly risky clients
- **Precision = 0.46** --> out of the very few it flags, 46% actually are risky

The model almost always predicts safe. The few flags it raises tend to 
be correct, but it misses 99% of real defaulters. Precision here is 
meaningless when recall is this low.

---

### Threshold = 0.6 — Detection Breakdown

At t = 0.6, the model flags only 7 clients in the entire test set.

As a result we get:
- **Recall = 0.00** --> out of 7949 real defaulters, only 2 are caught
- **Precision = 0.29** --> of those 7 flags, only 2 are correct

At this point the model is not functioning as a detection system anymore.
It predicts safe for essentially everyone.

---

### Threshold = 0.7 — No Detection

At t = 0.7, the model flags nobody.

As a result we get:
- **Recall = 0.00** --> 0 risky clients detected
- **Precision = 0.00** --> nothing to measure

The confusion matrix confirms it: all 7949 risky clients are missed.
The model predicts safe for every single person in the test set.

---

### Threshold = 0.8 — No Detection (same as 0.7)

At t = 0.8, the results are identical to t = 0.7.

- **Recall = 0.00**
- **Precision = 0.00**

The model never reaches 80% confidence on any client, so no one gets flagged.
Same confusion matrix, same outcome.

---

## General Observation — Threshold Effect

Lower thresholds increase recall but reduce precision.  
Higher thresholds increase precision but recall collapses.

In credit risk, this trade-off matters: missing a real defaulter 
is typically more costly than investigating a false alarm.
Based on these results, t = 0.2 remains the most usable threshold.

---

## Final Conclusion

LightGBM meaningfully improves the model's ability to separate 
risky from safe clients compared to Logistic Regression (AUC 0.59 --> 0.67).

However, threshold selection still has a large impact on behavior:
- lower thresholds (e.g. 0.2) are better for detecting defaults
- higher thresholds reduce false positives but miss most risky cases

Two things this experiment confirms:

1. Improving the model is more impactful than only tuning thresholds
2. Threshold controls behavior, not model quality

Next steps should focus on:
- feature engineering
- better handling of class imbalance
- exploring more advanced model configurations