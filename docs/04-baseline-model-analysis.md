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


## Experiment 4 : Threshold Comparison (=0.3, =0.4, =0.5, =0.6, =0.7)

I tested several THRESHOLD to see how the model will behave.

### Results :
Here is the the output of all threshold from 0.3 to 0.7 :
```Bash
(lending-club-ml) PS C:\Users\Utilisateur\...\ML\lending-club-credit-risk> python -m src.main

 ---- THRESHOLD: 0.3 ----

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


 ---- THRESHOLD: 0.4 ----

Confusion Matrix:
[[ 2021 30030]
 [  289  7660]]

Evaluation Metrics:
Accuracy: 0.2420
AUC-ROC: 0.5911

Classification Report:
              precision    recall  f1-score   support

           0       0.87      0.06      0.12     32051
           1       0.20      0.96      0.34      7949

    accuracy                           0.24     40000
   macro avg       0.54      0.51      0.23     40000
weighted avg       0.74      0.24      0.16     40000


 ---- THRESHOLD: 0.5 ----

Confusion Matrix:
[[16890 15161]
 [ 3106  4843]]

Evaluation Metrics:
Accuracy: 0.5433
AUC-ROC: 0.5911

Classification Report:
              precision    recall  f1-score   support

           0       0.84      0.53      0.65     32051
           1       0.24      0.61      0.35      7949

    accuracy                           0.54     40000
   macro avg       0.54      0.57      0.50     40000
weighted avg       0.72      0.54      0.59     40000


 ---- THRESHOLD: 0.6 ----

Confusion Matrix:
[[31106   945]
 [ 7526   423]]

Evaluation Metrics:
Accuracy: 0.7882
AUC-ROC: 0.5911

Classification Report:
              precision    recall  f1-score   support

           0       0.81      0.97      0.88     32051
           1       0.31      0.05      0.09      7949

    accuracy                           0.79     40000
   macro avg       0.56      0.51      0.49     40000
weighted avg       0.71      0.79      0.72     40000


 ---- THRESHOLD: 0.7 ----

Confusion Matrix:
[[32051     0]
 [ 7948     1]]

Evaluation Metrics:
Accuracy: 0.8013
AUC-ROC: 0.5911

Classification Report:
              precision    recall  f1-score   support

           0       0.80      1.00      0.89     32051
           1       1.00      0.00      0.00      7949

    accuracy                           0.80     40000
   macro avg       0.90      0.50      0.44     40000
weighted avg       0.84      0.80      0.71     40000


Pipeline executed successfully.
LogisticRegression(class_weight='balanced', max_iter=1000, solver='saga')
```

### Interpretation :
#### Threshold = 0.3
So the model with t=0.3, it becomes LESS STRICT before identifying a client as defaulter.

    1. What does =0.3 mean  
    2. 
```mermaid
flowchart LR
    A[Client data] --> B[Trained ML model]
    B --> C[Probability of default (class 1)]
    C --> D{Threshold = 0.3}
    D -- ≥ 0.3 --> E[Class = DEFAULT]
    D -- < 0.3 --> F[Class = NON-DEFAULT]
```
That means our model will predict more defaults, catch more real defaulters, But it will also make more false alarms 

    1.  Confusion matrix :
The confusion matrix for the threshold = 0.3 is :
```bash
[[  394 31657]
 [   48  7901]]
```
So TN = 394 , TP = 7901 , FN = 48 , FP = 31657
    - 394 clients are safe AND the model said they are indeed safe : very small number comparing to the actual population 
    - 31657 clients are actually safe BUT the model said they are not. The model is accusing a large and huge number of GOOD client. The model here is too much *aggressive*.
    - 48 clients are actually not safe (default) and the model said they are safe. Very small number. So here the model misses almost no risky client. This is good one for threshold = 0.3
    - 7901 clients are actually risky (defaulted) and the model correctly predicted them as defaulter and risky. At this threshold the model is very good at catching risky clients (default). 

    1.  Model behavior at threshold = 0.3
    From the previous results of the confusion matrix we can conclude that :
        -   Predicted default (risky) = `FP + TP = 31657 + 7901 = 39558`
        -   Predicted Non-default (safe) = `TN + FN = 394 + 48 = 442`
    Out of 40k clients 39558 are predicted as default (risky) and only 442 clients are predicted non-default (safe).
    So at threshold = 0.3 the model consider almost everyone as risky (default).

    2.  Accuracy = 0.2074
    The correct ones from confusion matrix are `TP + TN = 394 + 7901 = 8295`out of `40k` clients.
    Very low accuracy and this because as we saw earlier that our model flags a lot safe clients.

    3. AUC-ROC = 0.5911
    As we know this metric measures how well the model separates risky people from safe people in general.
    W e know also that we interpret `0.5` as random, `0.6` as weak, but better that random a little bit, `0.7+` as decent and `0.8+` as strong.
    So in our case auc-roc = 0.59 : it tells us that the model still weak from separating risky from safe clients.

    4. Classification report :
        - class 0 (safe or non-default)
        ```bash
        precision = 0.89
        recall    = 0.01
        f1-score  = 0.02
        support   = 32051
        ```
        support = 32051 real safe clients in the test set. So the class 0 (non-default) is the majority class. 

        Recall for class 0 = 0.01 . Recall always ask *out of all real safe clients, how many did the model correctly identify as safe?* So our result here means that out of real safe clients (32051) it only identify 1% as safe!! that is a disaster my friend. the model never recognize safe clients or at least almost never.  

        Precision for class 0 = 0.89. Precession always asks *out of the people predicted as safe, how many were actually safe?* In our case here 89%. Very high. Obviously high because the model predicts (safe) for very few clients.

        F1 score class 0 =  0.02 : very low because recall metrics is also so low. it say that you model is just bad at class 0.


        - class 1 (risky or default)
        ```bash
        precision = 0.20
        recall = 0.99
        f1-score = 0.33
        support = 7949
        ```
        Support = 7949 : real risky clients (defaulters) in the test set

        recall for calls 1 = 0.99 : so the model at this threshold identifies 99% of real defaulters, almost every one. This one of the best and good strength for this threshold

        Precision for class 1 = 0.20 : so 80% of good clients are just flagged as risky. A weakness point of this threshold = 0.3.

        F1 score class 1 = 0.33 : despite very high recall, the low precision keeps the overall performance weak.

    8. Final conclusion for threshold = 0.3

        At threshold 0.3, the model becomes extremely aggressive.

        It catches almost all real defaults, which is why recall for class 1 reaches 0.99. This is the good side: the model misses very few risky clients.

        However, the cost is very high. The model wrongly flags a huge number of safe clients as defaulters, which causes false positives to explode. This is why accuracy falls to 0.21 and precision for class 1 stays low at 0.20.

        In simple words, the model now acts like almost everyone is risky. So even though it is very good at catching defaults, it is not practical because it rejects too many good clients.



