# Summary of 5_Default_NeuralNetwork

[<< Go back](../README.md)


## Neural Network
- **n_jobs**: -1
- **dense_1_size**: 32
- **dense_2_size**: 16
- **learning_rate**: 0.05
- **explain_level**: 2

## Validation
 - **validation_type**: split
 - **train_ratio**: 0.75
 - **shuffle**: True
 - **stratify**: True

## Optimized metric
logloss

## Training time

16.3 seconds

## Metric details
|           |    score |    threshold |
|:----------|---------:|-------------:|
| logloss   | 0.5492   | nan          |
| auc       | 0.799208 | nan          |
| f1        | 0.702703 |   0.311927   |
| accuracy  | 0.768657 |   0.409188   |
| precision | 0.916667 |   0.857539   |
| recall    | 1        |   0.00569454 |
| mcc       | 0.509776 |   0.409188   |


## Confusion matrix (at threshold=0.409188)
|                     |   Predicted as negative |   Predicted as positive |
|:--------------------|------------------------:|------------------------:|
| Labeled as negative |                      68 |                      13 |
| Labeled as positive |                      18 |                      35 |

## Learning curves
![Learning curves](learning_curves.png)

[<< Go back](../README.md)
