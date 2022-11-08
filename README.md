<div align="center">
  
[![Github Actions](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml/badge.svg)](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml)

</div>

# Create An Object Detection Demo 

using AWS Rekognition + FastAPI + AWS App Runner

## Before you start

Make sure you have the quota to deploy your inference endpoint in a region where App Runner is available. In the demo I'm using an `ml.m5.large` instance.

## Docker Instructions


```sh
docker build --tag visiondemo-rekognition .
```
```sh
docker run -p 127.0.0.1:8080:8080 -v $HOME/.aws/:/root/.aws:ro -e \
    AWS_PROFILE=default visiondemo-rekognition
```



## Push to ECR


<img width="1548" alt="Screenshot 2022-11-08 at 09 56 41" src="https://user-images.githubusercontent.com/3386410/200521120-bbf41786-0dc3-46e8-8e33-6fe065375754.png">




## App Runner Permissions


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



## (Optional) Run without Docker


```sh
make install
python main.py
```

## (Optional) Automated Testing with Github Actions

If you are interested in automated testing, check out the workflow in `.github/workflows/`. You need to add AWS credentials to your repo to set this up. You can read more about it [here](https://github.com/aws-actions/configure-aws-credentials) and [here](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services). However, this is optional and not required for the demo to work.


## Learning Material

* [Deep Learning For Computer Vision](https://web.eecs.umich.edu/~justincj/teaching/eecs498/WI2022/) very similar to CS231n; pytorch assignments in Google Colab
* [Building Cloud Computing Solutions at Scale](https://www.coursera.org/specializations/building-cloud-computing-solutions-at-scale) inspiration for this repo
* [AWS Technical Essentials](https://www.coursera.org/learn/aws-cloud-technical-essentials)
* [Introduction to Machine Learning in Production](https://www.coursera.org/learn/introduction-to-machine-learning-in-production)
