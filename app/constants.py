insert_resutl_query = ""

get_results_query = """
SELECT results.*
FROM results
INNER JOIN users ON results.username = users.username
WHERE users.username = 'to_be_replaced';
"""