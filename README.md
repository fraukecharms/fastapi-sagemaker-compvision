<div align="center">
  
[![Github Actions](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml/badge.svg)](https://github.com/fraukecharms/fastapi-sagemaker-compvision/actions/workflows/main.yml)
![Badge](https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiQk1EZHMrdDJlR1l1VFdWeWpIbjduaDNrQnRlZ29KckJLcG9BWmlMSGhEOGRWNm43UTRFb2U2b2RzdGNtcXJ6amcrQ1J5V2d1SVljS3I4VFFuRUdnOVpJPSIsIml2UGFyYW1ldGVyU3BlYyI6Iks5UUU1Z1ljRXdoWDNwTk0iLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=main)
</div>

# Create an Object Detection Demo 

You can use this repo to quickly create a live public(!) demo website for object detection. The prediction requests are sent to your own Sagemaker endpoint. If you are looking for a solution that sends requests to AWS' built-in Rekognition service instead, check out [this repo](https://github.com/fraukecharms/fastapi-rekognition-compvision).

## Before You Start

Make sure that you do all your work in a region where App Runner is available (e.g. `eu-west-1` if you are based in Europe) and that you have the quota to deploy your inference endpoint in that region. In the demo I'm using an `ml.m5.large` instance.

## Walk-Through Screen Recording
[Here](https://www.youtube.com/watch?v=y6bNoQvozu8) is an example of setting up a Cloud9 environment for your repo. Once that is up and running, feel free to follow along here:

[![Sagemaker Object Detection Demo (via FastAPI & AWS App Runner)](https://user-images.githubusercontent.com/3386410/215270756-f4515685-6b0e-4a9c-831c-3b8aeade51f7.png)](https://www.youtube.com/watch?v=3gYK3uCbd7g)



## Docker Instructions


```sh
docker build --tag visiondemo-sagemaker .
```
```sh
docker run -p 127.0.0.1:8080:8080 -v $HOME/.aws/:/root/.aws:ro -e \
    AWS_PROFILE=default visiondemo-sagemaker
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


If you are interested in automated testing, check out the `main.yml` file in `.github/workflows/`. You can set this up by configuring OpenID Connect in AWS and creating an IAM role for your repo. You can read more about it [here](https://github.com/aws-actions/configure-aws-credentials) and [here](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services). However, this is optional and not required for the demo to work.

## Learning Material

* [Deep Learning For Computer Vision](https://web.eecs.umich.edu/~justincj/teaching/eecs498/WI2022/) very similar to CS231n; pytorch assignments in Google Colab
* [Building Cloud Computing Solutions at Scale](https://www.coursera.org/specializations/building-cloud-computing-solutions-at-scale) inspiration for this repo
* [AWS Technical Essentials](https://www.coursera.org/learn/aws-cloud-technical-essentials)
* [Introduction to Machine Learning in Production](https://www.coursera.org/learn/introduction-to-machine-learning-in-production)
