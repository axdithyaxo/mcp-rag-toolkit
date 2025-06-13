from mcp_rag_toolkit.query_executor import run_sql_query
from mcp_rag_toolkit.sql_generator import generate_sql

# Direct SQL query
query = "SELECT name, role FROM employee_directory WHERE department = 'HR';"
result_df = run_sql_query(query)
print("🔹 Direct SQL Query Result:")
print(result_df.to_markdown())

# Natural language to SQL
nl_question = "Get name and role from employee_directory where department is HR"
generated_sql = generate_sql(nl_question)
print("\n🔹 Generated SQL from NL:")
print(generated_sql)

# Run the generated SQL
if generated_sql.strip():
    result_df = run_sql_query(generated_sql)
    print("\n🔹 Result of Generated SQL:")
    print(result_df.to_markdown())
else:
    print("\n⚠️ No SQL query was generated.")