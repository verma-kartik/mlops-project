# Dphi-MLOps-Assignment
 
 ## Project Title: Implementing Kubeflow with Evidently.ai for Model Monitoring
 
Project Tasks:

| Task | Status |
| ------- | ------ |
| 1. Install and configure Kubeflow on a Kubernetes cluster | Completed ✔️ |
| 2. Install and configure Evidently.ai on the same cluster | Completed ✔️ |
| 3. Write a Python script to train a model on a dataset | Completed ✔️ |
| 4. Use Kubeflow to create a pipeline to train & track model with Evidently.ai | Completed ✔️ |

## MLOps pipeline

### Architecture

<img src="images/architecture.png" width="100%"/>


### Deployment

The MLOps pipeline can be easily deployed via the following steps:

1. Clone the `dphi-mlops-assignment` repository locally:

    ```bash
    $ git clone https://github.com/verma-kartik/dphi-mlops-assignment.git
    ```
    
2. Goto folder `download_data`, build and push the docker image to your own registry. Repeat the step for folder `extremegboost`

    ```bash
    $ docker build -t <username>/<nameOfDockerImage> .
    $ docker push <username>/<nameOfDockerImage>
    ```

