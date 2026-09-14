import pyarrow as pa


VENDOR_SCHEMA = pa.schema([
    pa.field("vendor_id", pa.string()),
    pa.field("name", pa.string()),
    pa.field("email", pa.string()),
    pa.field("phone", pa.string()),
    pa.field("city", pa.string()),
    pa.field("postcode", pa.string()),
    pa.field("address", pa.string()),
])


CUSTOMER_SCHEMA = pa.schema([
    pa.field("customer_id", pa.string()),
    pa.field("first_name", pa.string()),
    pa.field("last_name", pa.string()),
    pa.field("email", pa.string()),
    pa.field("phone", pa.string()),
    pa.field("city", pa.string()),
    pa.field("postcode", pa.string()),
    pa.field("address", pa.string()),
    pa.field("payment_card", pa.string()),
])


STORE_SCHEMA = pa.schema([
    pa.field("store_id", pa.string()),
    pa.field("name", pa.string()),
    pa.field("size", pa.string()),
    pa.field("city", pa.string()),
    pa.field("postcode", pa.string()),
    pa.field("address", pa.string()),
])


PRODUCT_SCHEMA = pa.schema([
    pa.field("product_id", pa.string()),
    pa.field("vendor_id", pa.string()),
    pa.field("category", pa.string()),
    pa.field("name", pa.string()),
    pa.field("brand", pa.string()),
    pa.field("unit_cost", pa.decimal128(10, 2)),
    pa.field("unit_price", pa.decimal128(10, 2)),
])


ORDER_SCHEMA = pa.schema([
    pa.field("order_id", pa.string()),
    pa.field("customer_id", pa.string()),
    pa.field("store_id", pa.string()),
    pa.field("order_timestamp", pa.timestamp("us")),
    pa.field("status", pa.string()),
])


ORDER_LINE_SCHEMA = pa.schema([
    pa.field("order_line_id", pa.string()),
    pa.field("order_id", pa.string()),
    pa.field("product_id", pa.string()),
    pa.field("quantity", pa.int64()),
    pa.field("unit_price", pa.decimal128(10, 2)),
])