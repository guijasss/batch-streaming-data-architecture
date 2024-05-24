USE demo;
EXEC sys.sp_cdc_enable_db;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'Customers',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'Geolocation',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'OrderItems',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'OrderPayments',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'OrderReviews',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'Orders',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'Products',
@role_name     = 'adm',
@supports_net_changes = 0;

EXEC sys.sp_cdc_enable_table
@source_schema = 'dbo',
@source_name   = 'Sellers',
@role_name     = 'adm',
@supports_net_changes = 0;