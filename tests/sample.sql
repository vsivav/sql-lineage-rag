CREATE PROCEDURE dbo.usp_GetCustomers
AS
BEGIN

SELECT
    CustomerID,
    CustomerName
FROM dbo.Customers;

END
