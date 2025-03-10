
terraform_code_prompt = """
    You are an expert cloud architect.  
    Generate a Terraform configuration for an AWS web application with:  
    - EC2 instances behind an Elastic Load Balancer  
    - An RDS PostgreSQL database  
    - An S3 bucket for static file storage  
    - A VPC with public and private subnets  

    Output the response in **Terraform format** without explanations.  
"""


node_connection_prompt = """
Generate a JSON structure for a cloud architecture where:
    - A Load Balancer distributes traffic to EC2 instances.
    - EC2 instances interact with an RDS database.
    - An S3 bucket is used for static storage.
    - The architecture is multi-cloud (AWS, GCP, Azure).

    The output should include:
    - Nodes (services)
    - Dependencies (which node connects to which)
    - The cloud provider for each node
    - Ensure services follow the **Well-Architected Framework** principles, such as:
        - High availability
        - Fault tolerance
        - Security best practices
        - Scalability
    - Ensure the architecture includes appropriate nodes and dependencies, aligning with the Well-Architected Framework principles.
    - Maintain the correct sequence of services from an architectural perspective.
    - The output must be a valid JSON object without any code blocks or formatting like "```json```"
    - Return only the raw JSON response without any explanations.

Example format:
Unique Terraform resource type: aws_<service_name>, gcp_<service_name>, azure_<service_name> should be used in following nodes type. for example, aws_instance, aws_lambda, aws_s3_bucket etc
{
  "nodes": [
    {
      "id": "Load Balancer",
      "type": "aws_<service_name>",
      "cloud": "AWS"
    },
    {
      "id": "EC2 Instance 1",
      "type": "aws_<service_name>",
      "cloud": "AWS"
    },
    more nodes...
  ],
  "dependencies": [
    {
      "source": "Load Balancer",
      "target": "EC2 Instance 1"
    },
    {
      "source": "Load Balancer",
      "target": "EC2 Instance 2"
    },
    more dependencies...
  ]
}
"""