import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mssql.server import get_connection, is_read_only_query, execute_sql_raw, list_tables_raw, get_table_data_raw, describe_table_raw

class TestDatabaseConnection:
    def test_connection(self):
        """Test database connection"""
        conn = get_connection()
        assert conn is not None
        conn.close()

class TestQueryValidation:
    def test_valid_queries(self):
        """Test valid read-only queries"""
        valid_queries = [
            "SELECT * FROM users",
            "WITH cte AS (SELECT 1) SELECT * FROM cte",
            "DECLARE @x INT SELECT @x",
            "select count(*) from table1"
        ]
        for query in valid_queries:
            assert is_read_only_query(query) == True

    def test_invalid_queries(self):
        """Test invalid/dangerous queries"""
        invalid_queries = [
            "INSERT INTO users VALUES (1)",
            "UPDATE users SET name = 'test'",
            "DELETE FROM users",
            "DROP TABLE users",
            "CREATE TABLE test (id INT)",
            "ALTER TABLE users ADD col VARCHAR(10)",
            "TRUNCATE TABLE users",
            "EXEC sp_help",
            "SELECT * FROM users; DROP TABLE users",
            "GRANT SELECT ON users TO public"
        ]
        for query in invalid_queries:
            assert is_read_only_query(query) == False

class TestSQLExecution:
    def test_execute_valid_sql(self):
        """Test executing valid SQL"""
        result = execute_sql_raw("SELECT COUNT(*) as count FROM SalesLT.Customer")
        assert "count" in result
        assert "Error" not in result
        lines = result.strip().split('\n')
        assert len(lines) == 2  # Header + 1 data row

    def test_execute_invalid_sql(self):
        """Test rejecting invalid SQL"""
        result = execute_sql_raw("DELETE FROM SalesLT.Customer")
        assert result == "Error: Only SELECT queries are allowed"

    def test_execute_sql_error(self):
        """Test SQL execution error handling"""
        result = execute_sql_raw("SELECT * FROM NonExistentTable")
        assert "Error:" in result

class TestResources:
    def test_list_tables(self):
        """Test listing all tables"""
        result = list_tables_raw()
        assert "SalesLT.Customer" in result
        assert "SalesLT.Product" in result
        assert "dbo.BuildVersion" in result

    def test_get_table_data(self):
        """Test getting table data"""
        result = get_table_data_raw("SalesLT.ProductCategory")
        assert "ProductCategoryID" in result
        assert "Name" in result
        lines = result.strip().split('\n')
        assert len(lines) > 1  # Should have header + data

    def test_get_table_data_invalid(self):
        """Test invalid table name handling"""
        result = get_table_data_raw("'; DROP TABLE users; --")
        assert "Error:" in result

class TestDescribeTable:
    def test_describe_valid_table(self):
        """Test describing a valid table"""
        result = describe_table_raw("SalesLT.Customer")
        assert "COLUMN_NAME,DATA_TYPE" in result
        assert "CustomerID" in result
        assert "Error" not in result
        
    def test_describe_table_without_schema(self):
        """Test describing table without schema prefix"""
        result = describe_table_raw("Customer")
        assert "COLUMN_NAME,DATA_TYPE" in result
        assert "CustomerID" in result
        assert "Error" not in result
        
    def test_describe_nonexistent_table(self):
        """Test describing non-existent table"""
        result = describe_table_raw("NonExistentTable")
        assert "Error: Table 'NonExistentTable' not found" in result
        
    def test_describe_invalid_table_name(self):
        """Test describing with invalid table name"""
        result = describe_table_raw("'; DROP TABLE users; --")
        assert "Error: Invalid table name format" in result