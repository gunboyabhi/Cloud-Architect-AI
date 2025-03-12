import json
import hcl2
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError

# AWS
from diagrams import Diagram, Cluster
from diagrams.aws.compute import AppRunner, ElasticBeanstalk, EC2, Lambda, Outposts, ECS, EKS, EB, Batch, EC2ElasticIpAddress, EC2AutoScaling, ECR, Lightsail
from diagrams.aws.network import ELB, VPC, APIGateway, PublicSubnet, CloudFront, ElasticLoadBalancing
from diagrams.aws.storage import S3, EFS
from diagrams.aws.database import RDS, KeyspacesManagedApacheCassandraService, Neptune, Dynamodb, Redshift, Elasticache, Aurora, DatabaseMigrationService, DocumentDB
from diagrams.aws.security import IAM, KMS, WAF
from diagrams.aws.ml import Sagemaker
from diagrams.aws.analytics import EMR, Glue, LakeFormation, Quicksight, Kinesis, Athena, Cloudsearch, AmazonOpensearchService
from diagrams.aws.integration import SQS, SNS, Eventbridge, StepFunctions, MQ
from diagrams.aws.devtools import Codepipeline, Codebuild, Codecommit, Codedeploy, Codestar
from diagrams.aws.iot import IotCore, InternetOfThings
from diagrams.aws.management import AmazonManagedWorkflowsApacheAirflow, Cloudwatch, Cloudtrail, Cloudformation
from diagrams.aws.general import InternetGateway
from diagrams.aws.blockchain import ManagedBlockchain, QuantumLedgerDatabaseQldb
from diagrams.aws.business import Workmail
from diagrams.aws.cost import CostAndUsageReport
from diagrams.aws.engagement import Connect, Pinpoint, SES
from diagrams.aws.game import Gamelift

# GCP
from diagrams.gcp.compute import GCE, GKE, KubernetesEngine, Run, AppEngine, Functions
from diagrams.gcp.database import SQL, Spanner, Bigtable, Firestore, Memorystore
from diagrams.gcp.ml import AIPlatform
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.devtools import Build
from diagrams.gcp.storage import GCS, Filestore
from diagrams.gcp.network import CDN, LoadBalancing, VirtualPrivateCloud
from diagrams.gcp.security import Iam as GCP_IAM, SecurityCommandCenter
from diagrams.gcp.operations import Monitoring, Logging

# Azure
from diagrams.azure.compute import VM, ContainerInstances, FunctionApps, AKS
from diagrams.azure.storage import BlobStorage
from diagrams.azure.database import SQLDatabases, CosmosDb, DataLake
from diagrams.azure.ml import MachineLearningServiceWorkspaces
from diagrams.azure.analytics import SynapseAnalytics, EventHubs
from diagrams.azure.devops import Pipelines, Repos
from diagrams.azure.network import LoadBalancers, VirtualNetworks
from diagrams.azure.security import SecurityCenter, KeyVaults


load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
BUCKET_NAME = os.environ.get("GROQ_API_KEY")
S3_REGION = os.environ.get("GROQ_API_KEY")

# # Initialize Boto3 S3 Client
# s3_client = boto3.client(
#     "s3",
#     aws_access_key_id=AWS_ACCESS_KEY,
#     aws_secret_access_key=AWS_SECRET_KEY,
#     region_name=S3_REGION
# )

SERVICE_MAP = {
    # AWS Services
    "aws_instance": EC2,
    "aws_lambda": Lambda,
    "aws_ecs_cluster": ECS,
    "aws_ecs_container": ECS,
    "aws_eks_cluster": EKS,
    "aws_batch_compute_environment": Batch,
    "aws_elb": ELB,
    "aws_vpc": VPC,
    "aws_api_gateway": APIGateway,
    "aws_s3_bucket": S3,
    "aws_efs_file_system": EFS,
    "aws_db_instance": RDS,
    "aws_rds": RDS,
    "aws_dynamodb_table": Dynamodb,
    "aws_redshift_cluster": Redshift,
    "aws_iam_role": IAM,
    "aws_kms_key": KMS,
    "aws_waf": WAF,
    "aws_sagemaker_notebook_instance": Sagemaker,
    "aws_kinesis_stream": Kinesis,
    "aws_athena_database": Athena,
    "aws_sqs_queue": SQS,
    "aws_sns_topic": SNS,
    "aws_eventbridge_rule": Eventbridge,
    "aws_codepipeline": Codepipeline,
    "aws_codebuild_project": Codebuild,
    "aws_codecommit_repository": Codecommit,
    "aws_codedeploy_deployment_group": Codedeploy,
    "aws_codestarconnections_connection": Codestar,
    # "aws_codestarnotifications_notification_rule": CodestarNotifications,
    "aws_iot_core": IotCore,
    "aws_cloudwatch_log_group": Cloudwatch,
    "aws_cloudtrail": Cloudtrail,
    "aws_eip": EC2ElasticIpAddress,
    "aws_subnet": PublicSubnet,
    "aws_cloudfront_distribution": CloudFront,
    "aws_cloudsearch_domain": Cloudsearch,
    "aws_elasticache_cluster": Elasticache,
    "aws_opensearch_domain": AmazonOpensearchService,
    "aws_internet_gateway": InternetGateway,
    "aws_sfn_state_machine": StepFunctions,
    "aws_iot_thing": InternetOfThings,
    "aws_cloudformation_stack": Cloudformation,
    "aws_autoscaling_group": EC2AutoScaling,
    "aws_ecr_repository": ECR,
    "aws_elastic_beanstalk_application": EB,
    "aws_lightsail_instance": Lightsail,
    "aws_emr_cluster": EMR,
    "aws_glue_catalog_database": Glue,
    "aws_lakeformation_data_lake_settings": LakeFormation,
    "aws_quicksight_user": Quicksight, 
    "aws_managedblockchain_network": ManagedBlockchain,
    "aws_qldb_ledger": QuantumLedgerDatabaseQldb,
    "aws_workmail_organization": Workmail,
    "aws_apprunner_service": AppRunner,
    "aws_elastic_beanstalk_environment": ElasticBeanstalk,
    "aws_outposts_outpost": Outposts,
    "aws_cur_report_definition": CostAndUsageReport,
    "aws_rds_cluster": Aurora,
    "aws_dms_replication_instance": DatabaseMigrationService,
    "aws_docdb_cluster": DocumentDB,
    "aws_keyspaces_table": KeyspacesManagedApacheCassandraService,
    "aws_neptune_cluster": Neptune,
    "aws_connect_instance": Connect,
    "aws_pinpoint_app": Pinpoint,
    "aws_ses_email_identity": SES,
    "aws_gamelift_build": Gamelift,
    # "aws_appflow_flow": Appflow,
    "aws_mwaa_environment": AmazonManagedWorkflowsApacheAirflow,
    "aws_mq_broker": MQ,
    # "aws_athena_workgroup": Athena,

    # GCP Services
    "google_compute_instance": GCE,
    "google_compute_instance_group_manager": GCE,
    "google_kubernetes_engine_cluster": KubernetesEngine,
    "google_cloud_run_service": Run,
    "google_app_engine_application": AppEngine,
    "google_sql_database_instance": SQL,
    "google_spanner_instance": Spanner,
    "google_bigtable_instance": Bigtable,
    "google_firestore_database": Firestore,
    "google_ai_platform_model": AIPlatform,
    "google_bigquery_dataset": BigQuery,
    "google_dataflow_job": Dataflow,
    "google_pubsub_topic": PubSub,
    "google_cloud_build_trigger": Build,
    "google_cloud_function": Functions,
    "google_storage_bucket": GCS,
    "google_filestore_instance": Filestore,
    "google_compute_network": VirtualPrivateCloud,
    "google_compute_firewall": SecurityCommandCenter,
    "google_compute_forwarding_rule": LoadBalancing, 
    "google_compute_backend_bucket": CDN,
    "google_monitoring_alert_policy": Monitoring,
    "google_logging_sink": Logging,
    "google_monitoring_notification_channel": Monitoring,
    "google_logging_project_sink": Logging,
    "google_redis_instance": Memorystore,
    "google_iam_policy": GCP_IAM,
    "google_container_cluster": GKE,


    # Azure Services
    "azurerm_virtual_machine": VM,
    "azurerm_container_instance": ContainerInstances,
    "azurerm_function_app": FunctionApps,
    "azurerm_kubernetes_cluster": AKS,
    "azurerm_storage_account": BlobStorage,
    "azurerm_data_lake_store": DataLake,
    "azurerm_sql_database": SQLDatabases,
    "azurerm_cosmosdb_account": CosmosDb,
    "azurerm_machine_learning_workspace": MachineLearningServiceWorkspaces,
    "azurerm_synapse_workspace": SynapseAnalytics,
    "azurerm_eventhub": EventHubs,
    "azurerm_devops_pipeline": Pipelines,
    "azurerm_devops_repo": Repos,
    "azurerm_lb": LoadBalancers,
    "azurerm_virtual_network": VirtualNetworks,
    "azurerm_security_center": SecurityCenter,
    "azurerm_key_vault": KeyVaults,
}


def upload_to_s3(file_path, s3_key):
    """Uploads a file to S3 and returns its URL."""
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, s3_key, ExtraArgs={"ACL": "public-read"})
        return f"https://{BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{s3_key}"
    except NoCredentialsError:
        print("AWS Credentials not found")
        return None
    

def generate_architecture_diagram(data, filename="AI_generated_cloud_architecture"):
    try:
      if not data:
        return
      local_filename = f"{filename}.svg"
      with Diagram("AI Generated Cloud Architecture", outformat="svg", show=False, filename=filename):
          nodes = {}
          breakpoint()
          # Define cloud clusters
          cloud_clusters = {
              "AWS": Cluster("AWS Cloud"),
              "GCP": Cluster("GCP Cloud"),
              "Azure": Cluster("Azure Cloud")
          }
          # Create cloud clusters and nodes
          for node in data["nodes"]:
              if node['cloud'] == 'AWS':
                service_icon = SERVICE_MAP.get(node["type"], EC2)  # Default to EC2 if unknown
              elif node['cloud'] == 'GCP':
                service_icon = SERVICE_MAP.get(node["type"], GCE)  # Default to GCE if unknown
              else:
                 service_icon = SERVICE_MAP.get(node["type"], VM)  # Default to VM if unknown
              with cloud_clusters.get(node["cloud"], Diagram()):
                nodes[node["id"]] = service_icon(node["id"])

          # Create connections based on dependencies
          for dep in data["dependencies"]:
              nodes[dep["source"]] >> nodes[dep["target"]]
      
      # # Upload to S3
      # s3_key = f"architecture/{local_filename}"  # Store in a specific folder in S3
      # s3_url = upload_to_s3(local_filename, s3_key)
      s3_url = ''

      # Cleanup local file
      # os.remove(local_filename)

      return s3_url if s3_url else None
    except Exception as e:
       print(e)
       return None

# generate_architecture_diagram(data)
