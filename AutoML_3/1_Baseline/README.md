# Summary of 1_Baseline

[<< Go back](../README.md)


## Baseline Classifier (Baseline)
- **n_jobs**: -1
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

0.8 seconds

## Metric details
|           |    score |   threshold |
|:----------|---------:|------------:|
| logloss   | 0.674222 |      nan    |
| auc       | 0.5      |      nan    |
| f1        | 0.574468 |        0.36 |
| accuracy  | 0.402985 |        0.36 |
| precision | 0.402985 |        0.36 |
| recall    | 1        |        0.36 |
| mcc       | 0        |        0.36 |


## Confusion matrix (at threshold=0.36)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                       0 |                      80 |
| Labeled as positive |                       0 |                      54 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
