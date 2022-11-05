<div align="center">
  
[![Github Actions](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml/badge.svg)](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml)

</div>

# Create An Object Detection Demo 

using AWS Rekognition + FastAPI + AWS App Runner
Make sure you have the quota to deploy endpoint in the appropriate region.

## Docker Instructions

```sh
docker build --tag visiondemo .
docker run -p 127.0.0.1:8080:8080 visiondemo
```


## Push to ECR


<img alt="ECR push commands" width="525" src="https://user-images.githubusercontent.com/3386410/196132461-7cd7c53e-cd52-401e-972c-68fbec15937c.png">

## Permissions


```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "tasks.apprunner.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

```

<img width="525" alt="Screenshot 2022-11-05 at 08 50 13" src="https://user-images.githubusercontent.com/3386410/200109578-1fd2c503-df76-4032-9372-31b608ddbb8f.png">



## Run without docker


```sh
make install
python main.py
```


## Learning Material

* [Deep Learning For Computer Vision](https://web.eecs.umich.edu/~justincj/teaching/eecs498/WI2022/) very similar to CS231n; pytorch assignments in Google Colab
* [Building Cloud Computing Solutions at Scale](https://www.coursera.org/specializations/building-cloud-computing-solutions-at-scale)
* [AWS Technical Essentials](https://www.coursera.org/learn/aws-cloud-technical-essentials)
* [Introduction to Machine Learning in Production](https://www.coursera.org/learn/introduction-to-machine-learning-in-production)
