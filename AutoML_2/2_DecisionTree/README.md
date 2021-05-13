# Summary of 2_DecisionTree

[<< Go back](../README.md)


## Decision Tree
- **n_jobs**: -1
- **criterion**: gini
- **max_depth**: 3
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

27.7 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.488282 | nan         |
| auc       | 0.813301 | nan         |
| f1        | 0.693878 |   0.444488  |
| accuracy  | 0.791045 |   0.523059  |
| precision | 1        |   0.971429  |
| recall    | 1        |   0.0929348 |
| mcc       | 0.569635 |   0.523059  |


## Confusion matrix (at threshold=0.523059)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                      78 |                       3 |
| Labeled as positive |                      25 |                      28 |

## Learning curves
![Learning curves](learning_curves.png)

## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence (Fold 1)
![SHAP Dependence from Fold 1](learner_fold_0_shap_dependence.png)

## SHAP Decision plots


[<< Go back](../README.md)
