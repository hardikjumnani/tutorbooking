# Terraform — AWS VPC + EKS for TutorSlot

This provisions the cloud infrastructure the app runs on:

- a **VPC** with 2 public and 2 private subnets across two availability zones
- a single **NAT gateway** (lets private nodes reach the internet, cheaply)
- an **EKS** (managed Kubernetes) cluster with a worker node group (2x `t3.medium`)

AWS credentials are supplied through the environment (`aws configure`, or the
`AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` variables). **Never commit them.**

## Commands

```bash
terraform init          # download the AWS provider and the VPC/EKS modules
terraform fmt -recursive
terraform validate
terraform plan          # preview what will be created (needs AWS credentials)
terraform apply         # create the infrastructure (~15-20 minutes)

# point kubectl at the new cluster:
aws eks update-kubeconfig --region ap-south-1 --name tutorslot-eks

terraform destroy       # tear everything down when finished
```

> **Cost warning:** EKS and the NAT gateway are **not** free tier. Run
> `terraform destroy` as soon as you finish the demo to avoid charges.
