
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
    - type should unique terraform resource type example, aws_instance, aws_s3_bucket
    - Ensure services follow the **Well-Architected Framework** principles, such as:
        - High availability
        - Fault tolerance
        - Security best practices
        - Scalability
    - Ensure the architecture includes appropriate nodes and dependencies, aligning with the Well-Architected Framework principles.
    - Maintain the correct sequence of services from an architectural perspective.

Additionally, provide a second list in the JSON that contains the corresponding **Terraform Infrastructure as Code (IaC)** for the architecture. The Terraform code should:
    - Use the correct provider (`aws_`, `gcp_`, `azure_`) for each service.
    - Define resources, variables, and dependencies appropriately.
    - Follow Terraform best practices for modularity and reusability.

The final JSON structure should have:
1. **Nodes and dependencies** (as described above).
2. **Terraform IaC list** where each entry maps to the nodes in the architecture.
3. **Ensure the output is a valid JSON object without code blocks (e.g., ` ```json `).

### **IMPORTANT INSTRUCTIONS**:
- **Return ONLY raw JSON output.**  
- **Do NOT include any explanations, descriptions, or introductory text.**  
- **Ensure the output is a valid JSON object without code blocks (e.g., ` ```json `).**  

Example format:
{
  "architecture": {
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
  },
  "terraform": [
    {
      "resource": "aws_lb",
      "config": "resource \"aws_lb\" \"example\" { ... }"
    },
    {
      "resource": "aws_instance",
      "config": "resource \"aws_instance\" \"example\" { ... }"
    },
    more Terraform resources...
  ]
}
"""

