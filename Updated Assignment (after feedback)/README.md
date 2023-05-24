### Architecture

<img src="images/new-architecture.png" width="100%"/>

Changes in the current architecture from the previous architecture:

1.	Use of microk8s (on a single 8 cores 32 GB 150GB instance) instead of GKE for installing Kubeflow.
2.	Use of Charmed Kubeflow instead of google marketplace provided Kubeflow pipelines.
3.	Running the pipelines from the cluster directly instead of structuring the components as separate docker images and uploading them to docker hub.
4.	Evidently dashboard reports can now be seen directly in the Kubeflow visualization tabs instead of storing them into google bucket storage.
