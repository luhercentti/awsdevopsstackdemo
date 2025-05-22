# Simple Python Flask App with AWS CI/CD Pipeline

This repository contains a simple Python Flask application deployed to AWS ECS Fargate using a CI/CD pipeline built with AWS CodePipeline, CodeBuild, and CodeDeploy.

AWS CodePipeline Workflow

Source Stage: AWS CodePipeline pulls code from your GitHub repository
Build Stage: CodeBuild uses your Python setup to test and build the app
Deploy Stage: CodeDeploy deploys the app to ECS


## Project Structure

```
.
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image configuration
├── buildspec.yml           # AWS CodeBuild configuration
├── appspec.yml             # AWS CodeDeploy configuration
└── README.md               # This file
```

## Prerequisites

1. An AWS account
2. AWS CLI configured with appropriate credentials
3. Terraform installed
4. A GitHub repository to host this code

## Deployment Steps

1. **Update GitHub Repository Information**:
   - In `main.tf`, update the `FullRepositoryId` parameter in the `aws_codepipeline` resource with your GitHub repository details.

2. **Initialize Terraform**:
   ```
   terraform init
   ```

3. **Review and Apply Terraform Configuration**:
   ```
   terraform plan
   terraform apply
   ```

4. **Complete GitHub Connection Setup**:
   - After applying the Terraform configuration, follow the instructions in the output to complete the GitHub connection setup in the AWS Console.

5. **Push Your Code to GitHub**:
   Make sure you have all the files in this repository pushed to your GitHub repository.

## How it Works

1. **CI/CD Pipeline**:
   - The pipeline is triggered when changes are pushed to the GitHub repository.
   - CodeBuild builds a Docker image based on the Dockerfile and pushes it to ECR.
   - CodeDeploy deploys the new image to the ECS Fargate service.

2. **Application**:
   - The simple Flask application exposes two endpoints:
     - `/`: Returns a JSON response with a greeting message
     - `/health`: Returns the health status

## Cleanup

To destroy all resources created by Terraform:
```
terraform destroy
```

## Note

This is a minimal example for demonstration purposes. For production use, you should consider adding:
- SSL/TLS
- Proper logging configuration
- Enhanced security measures
- More robust health checks
- Load balancer configuration



/////

terraform show -json tfplan.binary > tfplan.json
infracost breakdown --path=tfplan.json