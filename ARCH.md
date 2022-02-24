# Plan for Architecture of this client 

## Dataset loading 
1. Simplifiy or make dataset loading more consistent across the two versions of WMLA 
  - Need to look into how to enable access to creating PVC and pod resources 
  - Ideally if a pod is create no one would need to login to it to download data this would all be specified by a command in the pod 
  - Alternativelly a service could be run in the WMLA namespace that takes API requests to pull data into a pod and copy it into the required folder location? 
  - API would need to be authenticated with RBAC and so would the data access on the system? 

## Training 
AP
1. Focus on simplification of model training with one GPU and no elastic distibution 
    - Ideally all this could be submitted from within a python notebook or via python code 
    - The user would just need to point to code or a train function to sub this and the code on the backend would format it to comply to the REST API (including creating a main.py as required)
    
2. Focus on simplification of model training with multiple GPU and no elastic distribution 
    - Take single GPU code and add requirements to make it multi GPU complient for Pytorch and TF 
    - Leverage 1. for the remainder 
    
3. Focus on simplification of model training with multiple GPU and elastic distribution 
    - Take single GPU code and either automagically find the appropriate parts of the code to update or (and more likley) use annotations to the specific parts of the code that need to be wrapped in the "FabricModel"
    - Output a Elastic Distribution complient model
    - We will need checks to ensure that the model will not fail on run (confirm the number of optimisers for example)
