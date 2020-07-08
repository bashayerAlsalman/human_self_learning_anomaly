# Human Activity Analysis: Iterative Weak/Self-Supervised Learning Frameworks for Detecting Abnormal Events

This repository contains the code for the IJCB'20 paper ["Human Activity Analysis: Iterative Weak/Self-Supervised Learning Frameworks for Detecting Abnormal Events"](http://socia-lab.di.ubi.pt/EventDetection)

<div align="center">
    <img src="fig/WSS_Schema.png", width=100%">
</div>

## Installation
```bash
pip install -r requirements.txt  # use flag --user if permission needed
```

##### Libraries version:
* Keras: 2.4.3
* TensorFlow: 2.2.0
* Scipy: 1.4.1
* Scikit-learn: 0.23.1
* NumPy: 1.19.0


## Dataset and Directories Structure

The [**UBI-Fights Dataset**](http://socia-lab.di.ubi.pt/EventDetection) provides a wide diversity in fighting scenarios with 1000 videos, where 784 are normal daily life situations and 216 contain a fighting event. This dataset is **fully-annotated** at the **frame-level**.<br>
Extract the [C3D](https://github.com/facebookarchive/C3D) features of your dataset.<br>
To train your model and employ self-supervision for each network, the following directory structure is created:

```
|-- annotation
|   |-- strong
|   |   |-- train.csv           // empty, to be filled by the WS Model and Bayesian Classifier
|   |   |-- test.csv
|   |   |-- val.csv
|   |   |-- unlabeled_set.csv
|   |   |-- test_notes.csv
|   |   `-- val_notes.csv
|   `-- weak
|       |-- train.csv           // Small percentage (i.e., 30%) of the original training set
|       |-- test.csv
|       |-- val.csv
|       |-- unlabeled_set.csv   // Remaining videos are unlabeled for self-supervision purposes
|       |-- test_notes.csv
|       `-- val_notes.csv
|-- models
|   |-- pattern_model
|   |   |-- 0                   // WSS framework iterations
|   |   |-- 1
|   |   |-- ...
|   |-- strong_model
|   |   |-- 0                   // WSS framework iterations
|   |   |-- 1
|   |   |-- ...
|   `-- weak_model
|       |-- 0                   // WSS framework iterations
|       |-- 1
|       |-- ...
`-- results         
    |-- pattern
    |   `-- VAL                 // Directory for validation stats
    |-- strong
    |   |-- FINAL               // Directory for test stats
    |   `-- VAL
    `-- weak
        |-- FINAL
        `-- VAL
    
```


## Quick Start
- **Training**: Start framework training.
```bash
python3 ws_ss.py --save_best_weak --save_best_strong    # Set flag settings accordingly to the ws_ss.py file
```

- **Restart from checkpoint**: To analyse the unlabeled scores, after a network executed over the unlabeled set, set the iteration and starting network.
```bash
python3 ws_ss.py --start_iteration 0 --weak_free_checkpoint --save_best_weak --save_best_strong    # Set flag settings accordingly to the ws_ss.py file
```

## Citation
Please cite this paper in your publications if it helps your research:

    @inproceedings{degardin2020human,
      author = {Degardin, Bruno and Proença, Hugo},
      title = {Human Activity Analysis: Iterative Weak/Self-Supervised Learning Frameworks for Detecting Abnormal Events},
      booktitle={IEEE International Joint Conference on Biometrics},
      year = {2020},
      organization={IEEE}
    }

    
