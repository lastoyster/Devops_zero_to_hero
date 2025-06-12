# Dockerize ECS Fargate with Python Flask

This is a Simple Python Flask web application that returns an HTML message:  
It’s designed to run as a containerized app on **AWS ECS Fargate**, using **Terraform** for infrastructure provisioning.

## 🧱 Project Structure

├── app.py # Main Flask application
├── requirements.txt # Python dependencies
├── Dockerfile # Build instructions for Docker image
├── terraform/ # Terraform configuration files
│ ├── main.tf
│ ├── variables.tf
│ ├── outputs.tf
│ └── terraform.tfvars


## 🔧 Prerequisites

Make sure you have the following installed on your local machine:

- [Python 3.8+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- An [AWS Account](https://aws.amazon.com/free/) with an IAM user and sufficient permissions
---

## 🐍 Run Locally (Optional Test)

You can run the Flask app locally before containerizing it.

```bash
pip install -r requirements.txt
python app.py
Visit: http://localhost:80

🐳 Build and Push Docker Image to Amazon ECR
Authenticate to ECR

aws ecr get-login-password --region <your-region> \
| docker login --username AWS --password-stdin <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com

aws ecr create-repository --repository-name hello-fargate-app
Build and Tag Docker Image

bash
Copy
Edit
docker build -t hello-fargate-app .
docker tag hello-fargate-app:latest <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/hello-fargate-app:latest
Push to ECR

bash
Copy
Edit
docker push <aws_account_id>.dkr.ecr.<your-region>.amazonaws.com/hello-fargate-app:latest
🌍 Deploy with Terraform on ECS Fargate
Update Terraform Variables

In terraform/terraform.tfvars, add your values:

hcl
Copy
Edit
region    = "us-east-1"
app_name  = "hello-fargate"
ecr_image = "<your ECR image URL>"
Initialize and Apply Terraform

bash
Copy
Edit
cd terraform
terraform init
terraform plan
terraform apply
This will provision a new VPC, ECS Cluster, IAM roles, networking, and Fargate service.

🌐 Access Your App
If you enabled public IP or set up an Application Load Balancer, open the assigned public IP or DNS in your browser:

cd terraform
terraform destroy
📌 Troubleshooting
Make sure your IAM user has permissions for ECS, ECR, VPC, IAM, and EC2.
Verify your Docker image is pushed to the correct ECR region and URL.

Ensure port 80 is exposed in your Dockerfile and security group.

📄 License
MIT License

