from app.models import LineageResult, PipelineLineage,LineageStage,SystemType

lineage_by_snowflake_object: dict[str, LineageResult] = {
    "MOBILE_ORDERS": LineageResult(
        snowflake_object="MOBILE_ORDERS",
        pipelines=[
            PipelineLineage(
                pipeline_id="mobile-orders-pipeline",
                stages=[LineageStage(system_type=SystemType.KAFKA,resource_id="na-orders", description="topic of all NA orders"),
                        LineageStage(system_type=SystemType.EKS, resource_id="mobile-orders-consumer", description="app that collects mobile orders"),
                        LineageStage(system_type=SystemType.MONGODB, resource_id="orders.mobile_orders",description="collection that contains mobile orders"),
                        LineageStage(system_type=SystemType.AWS_BATCH, resource_id="mobile-orders-export",description="export mongo collection to s3"),
                        LineageStage(system_type=SystemType.S3, resource_id="s3://analytics-landing/mobile-orders/",description="s3 file that has mobile orders"),
                        LineageStage(system_type=SystemType.AIRFLOW, resource_id="mobile-orders-to-snowflake",description="DAG that loads s3 file to SF table"),
                        LineageStage(system_type=SystemType.SNOWFLAKE, resource_id="MOBILE_ORDERS",description="sf table")
                        ],
            )
        ],
    )
}
