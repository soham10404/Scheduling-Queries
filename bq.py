from google.cloud import bigquery_datatransfer
import os
from google.cloud import bigquery_datatransfer_v1
import google.protobuf.json_format
from schemas import QuerySchema

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/vedant.rathi/Desktop/service_account.json"

transfer_client = bigquery_datatransfer.DataTransferServiceClient()

def BQScheduling(input_query: QuerySchema):
    project_id = "growwapi"
    dataset_id = str(input_query.dataset)

    disposition= "WRITE_APPEND"
    if input_query.write_preference=="Overwrite table":
        disposition="WRITE_TRUNCATE"
    
    t = str(input_query.startTime)
    t = t.replace(" ","T")
    t = t + 'Z'

    parent = transfer_client.common_project_path(project_id)

    transfer_config = google.protobuf.json_format.ParseDict(
    {
        "destination_dataset_id": dataset_id,
        "display_name": str(input_query.title),
        "data_source_id": "scheduled_query",
        "params": {
            "query":str(input_query.query),
            "destination_table_name_template":str(input_query.table_id),
            "write_disposition": disposition,
            "partitioning_field": str(input_query.partitioning_field),
        },
        "scheduleOptions": {
        "startTime": t,
        "endTime": None,
        },
        "schedule": "every 104 hours",
    },
    bigquery_datatransfer_v1.types.TransferConfig()._pb,
    )
    response = transfer_client.create_transfer_config(
        parent=parent,
        transfer_config=transfer_config,
        #service_account_name=service_account_name,
        #authorization_code=authorization_code,
    )
    print("Created scheduled query '{}'".format(response.name))


def BQGet():
    project_id = "growwapi"
    parent = transfer_client.common_project_path(project_id)

    configs = transfer_client.list_transfer_configs(parent=parent)
    print("Got the following configs:")
    for config in configs:
        print(f"\tID: {config.name}, Schedule: {config.schedule}")






