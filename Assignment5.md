+-------------------------+
|       User/System       |
| (inputs transaction)    |
+-----------+-------------+
            |
            v
+-------------------------+
|     Airtable Database   |
| (stores transaction)    |
+-----------+-------------+
            |
            v
+-------------------------+
|   AI Agent / Rule Engine|
| - Check thresholds      |
| - Frequency rules       |
| - Blacklist matching    |
+-----------+-------------+
            |
            v
+-------------------------+
|  Decision: High Risk?   |
+-----------+-------------+
    |                     |
    | Yes                 | No
    v                     v
+----------------+     +-------------------------+
| Zapier/Make.com|     | Airtable stores record |
| - Email alert  |     | as normal              |
| - Slack post    |     +-------------------------+
| - Notion page  |
+----------------+
