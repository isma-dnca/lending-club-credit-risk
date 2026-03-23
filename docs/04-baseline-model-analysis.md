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