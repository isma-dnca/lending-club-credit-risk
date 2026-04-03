# Feature Engineering
 
## Feature Engineering for `issue_d`
 
The original `issue_d` column is a high-cardinality categorical feature.
 
After transforming it into:
- issue_year
- issue_month

  
The original one is removed. The impact of this is:
- Number of features reduces significantly after encoding from 220 to 82
- Slight improvement in AUC-ROC from 0.6706 to 0.6725

Verdict 1:
This transformation reduced noise and improved model structure, even if the performance gain is modest.

---
 
## Feature Engineering for `emp_length`
 
The original `emp_length` column is a messy string category.
 
After transforming it into:
- emp_length_num as clean numerical signal
 
The original one is removed. The impact of this is:
- Number of features reduces slightly after encoding from 82 to 74
- AUC-ROC went slightly down from 0.6725 to 0.6714
 
No meaningful change and the behavior is still the same at threshold = 0.2 and at threshold = 0.5 the model is still blind to defaults.
 
Verdict 2:
No new signal added at this point. No improvement in the model's ability to separate classes.
 
---
 
## Conclusion
 
From verdict 1 & 2 we can conclude that the model already extracted most of what those features could give. After feature engineering on `issue_d` and `emp_length`, the impact was minimal.
 
So after attempting this signal we need NEW signal — not just cleaner versions of the same weak signal that we just proved here.
 
The next steps will focus on feature engineering of HIGH IMPACT COLUMNS — the features that actually matter and have a strong effect in credit risk.