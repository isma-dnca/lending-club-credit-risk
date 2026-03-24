# Base Line Model Analysis - Logistic Regression

## Understand the behavior of a baseline Logistic Regression model in an imbalanced credit risk sample.

-------------

## Dataset Characteristics 
- Binary Classification
    - 0 : non-default
    - 1 : default
- Imbalanced distribution 
    - Almost 80% non-default
    - Almost 20% default
  
---------------

## Experiment 1 : Default Logistic Regression

### Results :
- Accuracy: 0.8013
- ROC-AUC: 0.5446
- Recall (class 1): 0.00
  
### Interpretation :
The model predicted almost all samples as non-default
So we can say that :
- High accuracy is misleading
- The model ignores the minority class
- No defaults are detected
And that this model is npt useful in practice

## Experiment 2 : Blanced Logistic Regression

### Configuration :
```python
LogisticRegression(
    solver="saga",
    max_iter=1000,
    class_weight="balanced"
)
```

### Results :
- Accuracy: 0.5434
- ROC-AUC: 0.5911
- Recall (class 1): 0.61
- Precesion (class 1): 024%
  
### Interpretation :
The model now predicting a significant samples of defaults. But as precision is 24%, it introduces many false positives. Overall accuracy drops from 80% to 54% but usefulness improves
So we can say that :
- High accuracy is misleading
- The model ignores the minority class
- No defaults are detected
And that this model is npt useful in practice

## Conclusion & feedback 
## Key Learning

From this experiment, I realized something very important about working with real data.

First, accuracy can be very misleading when the dataset is imbalanced. In my case, most people are non-default, so the model can get around 80% accuracy just by predicting everyone as safe, which is clearly useless.

Second, recall is very important for this problem. The goal is to detect defaults, so missing them (false negatives) is a big issue. A model that doesn’t catch any default is not useful, even if its accuracy looks good.

Third, there is a trade-off between precision and recall. When I forced the model to pay attention to defaults using `class_weight="balanced"`, the recall improved a lot, but precision became low, meaning many predicted defaults were actually wrong.

Finally, I understood that baseline models can be deceptive. At first glance, the results can look good, but if I don’t analyze the metrics properly, I can completely misunderstand what the model is doing.


## Experiment 3 : Threshold Tuning (=0.3)

### Results 
```bash
Confusion Matrix:
[[  394 31657]
 [   48  7901]]

Evaluation Metrics:
Accuracy: 0.2074
AUC-ROC: 0.5911

Classification Report:
              precision    recall  f1-score   support

           0       0.89      0.01      0.02     32051
           1       0.20      0.99      0.33      7949

    accuracy                           0.21     40000
   macro avg       0.55      0.50      0.18     40000
weighted avg       0.75      0.21      0.09     40000

```
### Interpretation:

Lowering the THRESHOLD from default =0.5 to =0.3 made the model much more aggressive.
    The model now detects almost all defaults (recall for class 1 = 0.99 || 99% which is very high recall)
    But it also wrongly flags a very large number of safe clients as suspicious and defaulters.

In practice, the model predicts `default` for almost everyone. This reduces missed defaults (FN=48).
    But it also creates a huge number of false alarms (FP=31657 which is extremely high)

### Key finding from previous results 

This experiments shows that the decision threshold directly controls the trade-off between :
  - catching more defaults (recall)
  &
  -avoiding false alarms

In other words, when I lower the threshold, the model catches more defaults, which is good. But it also makes more mistakes on safe clients, which is bad and even a diaster for the business objective. 
