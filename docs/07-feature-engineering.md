# Feature Engineering for `issue_d`

The original `issue_d` column is a high-cardinality categorical features.

After transforming it into :
    - issue_year
    - issue_month
  
The original one is removed. The impact of this is :
    - Number of features reduces significantly after encoding from 220 to 82 
    - Slight improvement in AUC-ROC from 0.6706 to 0.6725

Conclusion:
This transformation reduced noise and improved model structure, even if the performance gain is modest.

