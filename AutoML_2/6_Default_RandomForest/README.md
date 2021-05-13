# Summary of 6_Default_RandomForest

[<< Go back](../README.md)


## Random Forest
- **n_jobs**: -1
- **criterion**: gini
- **max_features**: 0.9
- **min_samples_split**: 30
- **max_depth**: 4
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

22.9 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.469211 | nan         |
| auc       | 0.816445 | nan         |
| f1        | 0.718447 |   0.415342  |
| accuracy  | 0.791045 |   0.516632  |
| precision | 1        |   0.966687  |
| recall    | 1        |   0.0763445 |
| mcc       | 0.569635 |   0.585268  |


## Confusion matrix (at threshold=0.516632)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                      76 |                       5 |
| Labeled as positive |                      23 |                      30 |

## Learning curves
![Learning curves](learning_curves.png)

## SHAP Importance
![SHAP Importance](shap_importance.png)

## SHAP Dependence plots

### Dependence (Fold 1)
![SHAP Dependence from Fold 1](learner_fold_0_shap_dependence.png)

## SHAP Decision plots


[<< Go back](../README.md)
