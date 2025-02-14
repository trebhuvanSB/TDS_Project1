FUNCTION_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "count_days",
            "description": "Count the specified day of the week in a file containing dates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the input file containing dates."},
                    "output_file": {"type": "string", "description": "Path to the output file to write the result."},
                    "day_of_week": {"type": "string", "description": "The day of the week to count (e.g., 'monday', 'tuesday')."}
                },
                "required": ["input_file", "output_file", "day_of_week"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "format_markdown",
            "description": "Format a Markdown file using Prettier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the Markdown file to format."},
                },
                "required": ["input_file"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sort_contacts",
            "description": "Sort contacts in a JSON file by last name and first name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the input JSON file."},
                    "output_file": {"type": "string", "description": "Path to the output JSON file."},
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_datagen",
            "description": "Install uv (if required) and run datagen.py with the user's email and the given url or for inputting data to run other tasks",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "description": "The user's email address."},
                    "url": {"type": "string", "description": "The URL of the datagen.py file."},
                },
                "required": ["email", "url"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_recent_logs",
            "description": "Write the first line of the 10 most recent .log files in /data/logs/ to /data/logs-recent.txt, most recent first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log_dir": {"type": "string", "description": "Path to the directory containing log files."},
                    "output_file": {"type": "string", "description": "Path to the output file to write the result."},
                },
                "required": ["log_dir", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_markdown_index",
            "description": "Create an index of Markdown files with their titles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "docs_dir": {"type": "string", "description": "Path to the directory containing Markdown files."},
                    "index_file": {"type": "string", "description": "Path to the output index file."},
                },
                "required": ["docs_dir", "index_file"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    {
        "type": "function",
        "function": {
            "name": "extract_sender_email",
            "description": "Extract the sender's email address from an email message.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the input email file."},
                    "output_file": {"type": "string", "description": "Path to the output file to write the sender's email."},
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_credit_card_number",
            "description": "Use this for extracting credit card number.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_image": {"type": "string", "description": "Path to the input image file."},
                    "output_file": {"type": "string", "description": "Path to the output text file."},
                },
                "required": ["input_image", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_most_similar_comments",
            "description": "Use this to find similar comments.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {"type": "string", "description": "Path to the input file containing comments."},
                    "output_file": {"type": "string", "description": "Path to the output file to write the most similar pair of comments."},
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_markdown_to_html",
            "description": "Convert a Markdown file to styled HTML.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "Path to the input Markdown file."
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to save the output HTML file."
                    }
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_api_data",
            "description": "Fetch data from an API and save it to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "api_url": {"type": "string", "description": "The URL of the API to fetch data from."},
                    "output_file": {"type": "string", "description": "Path to the output file to save the data."},
                },
                "required": ["api_url", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clone_and_commit",
            "description": "Clone a git repository, make a commit, and push it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {"type": "string", "description": "The URL of the git repository to clone."},
                    "commit_message": {"type": "string", "description": "The commit message to use."},
                    "file_path": {"type": "string", "description": "The path of the file to add/modify in the repository."},
                    "file_content": {"type": "string", "description": "The content to write to the file."},
                },
                "required": ["repo_url", "commit_message", "file_path", "file_content"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_markdown_to_html",
            "description": "Convert a Markdown file to styled HTML.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "Path to the input Markdown file."
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to save the output HTML file."
                    }
                },
                "required": ["input_file", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "filter_csv",
            "description": "Filter a CSV file based on conditions and save as JSON.",
            "parameters": {
                "type": "object",
                "properties": {
                    "input_file": {
                        "type": "string",
                        "description": "Path to the input CSV file."
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to save the filtered JSON output."
                    },
                    "filter_description": {
                        "type": "string",
                        "description": "Description of how to filter the data (e.g., 'rows where price > 100 and category is Electronics')."
                    }
                },
                "required": ["input_file", "output_file", "filter_description"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_sql_query",
            "description": "Execute a SQL query on a database (sqlite or duckdb)",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to execute"
                    },
                    "db_path": {
                        "type": "string",
                        "description": "Path of the SQLite or DuckDB database file. (should be inside /data/)"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Path to save the output CSV file."
                    },
                    "db_type": {
                        "type": "string",
                        "description": "Type of database (sqlite or duckdb)"
                    },
                },
                "required": ["query", "db_path", "output_file", "db_type"],
                "additionalProperties": False,
            },
            "strict": True,   
        }
    },
        {
        "type": "function",
        "function": {
            "name": "scrape_website",
            "description": "Extract data from a website using CSS selectors.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string", 
                        "description": "The URL of the website to scrape."
                    },
                    "selector": {
                        "type": "string", 
                        "description": "CSS selector to extract specific elements (e.g., 'h1', '.class-name', '#id')."
                    },
                    "output_file": {
                        "type": "string", 
                        "description": "Path to the output file to save the extracted data."
                    }
                },
                "required": ["url", "selector", "output_file"],
                "additionalProperties": False,
            },
            "strict": True,
        }
    },
]
