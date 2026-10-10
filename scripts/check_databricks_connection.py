from databricks.connect import DatabricksSession

spark = (
    DatabricksSession.builder
    .profile("dev")
    .serverless()
    .getOrCreate()
)

df = spark.range(5)

df.show()