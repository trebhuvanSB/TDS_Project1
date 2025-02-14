import os
import base64
import glob
import io
import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import time
from PIL import Image

import httpx
import markdown2
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil import parser

from llm_utils import AIPROXY_TOKEN, AIPROXY_URL, ask_llm, generate_embeddings


def run_datagen(email: str, url: str):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("Failed to download datagen.py")
    
    with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tf:
        tf.write(r.content)
        temp_script = tf.name

    subprocess.run(["python", "-m", "uv", "run", temp_script, email], check=True)
    os.remove(temp_script)

def validate_data_path(*paths):
    for path in paths:
        if not path.startswith("/data"):
            raise ValueError(f"Path '{path}' must be within the /data directory")

def count_days(input_file: str, output_file: str, day_of_week: str):
    validate_data_path(input_file, output_file)
    day_of_week = day_of_week.lower()
    days_map = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    if day_of_week not in days_map:
        raise ValueError(f"Invalid day of the week: {day_of_week}")

    target_day = days_map[day_of_week]

    with open(input_file, "r") as f:
        dates = f.readlines()
    count = sum(1 for date in dates if parser.parse(date.strip()).weekday() == target_day)
    with open(output_file, "w") as f:
        f.write(str(count))

def format_markdown(input_file: str):
    validate_data_path(input_file)
    result = subprocess.run(
        ["npx", "prettier@3.4.2", "--write", '--stdin-filepath',input_file],
        capture_output=True,
        text=True,
        shell=True
    )
    if result.returncode != 0:
        print(f"Error running npx prettier: {result.stderr}")
        raise Exception(f"npx prettier failed with exit code {result.returncode}")
    print(f"npx prettier output: {result.stdout}")

def sort_contacts(input_file: str, output_file: str):
    validate_data_path(input_file, output_file)
    with open(input_file, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open(output_file, "w") as f:
        json.dump(sorted_contacts, f)

def write_recent_logs(log_dir: str, output_file: str):
    validate_data_path(log_dir, output_file)
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.endswith('.log')]
    log_files.sort(key=os.path.getmtime, reverse=True)
    recent_logs = log_files[:10]

    with open(output_file, "w") as out_f:
        for log_file in recent_logs:
            with open(log_file, "r") as in_f:
                first_line = in_f.readline().strip()
                out_f.write(first_line + "\n")

def create_markdown_index(docs_dir: str, index_file: str):
    validate_data_path(docs_dir, index_file)
    index = {}
    markdown_files = glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True)

    for md_file in markdown_files:
        with open(md_file, "r") as f:
            for line in f:
                if line.startswith("# "):
                    title = line[2:].strip()
                    filename = os.path.relpath(md_file, docs_dir).replace("\\", "/")
                    index[filename] = title
                    break

    sorted_index = {k: index[k] for k in sorted(index)}

    with open(index_file, "w") as f:
        json.dump(sorted_index, f, indent=4)

def extract_sender_email(input_file: str, output_file: str):
    validate_data_path(input_file, output_file)
    with open(input_file, 'r') as f:
        email_content = f.read()

    prompt = f"Extract the sender's email address from the following email content:\n{email_content}, do not include any other information."
    sender_email = ask_llm(prompt)

    with open(output_file, 'w') as f:
        f.write(sender_email)

def extract_credit_card_number(input_image: str, output_file: str):
    validate_data_path(input_image, output_file)
    try:
        img = Image.open(input_image)
        upscale_factor = 2
        new_size = (int(img.width * upscale_factor), int(img.height * upscale_factor))
        img = img.resize(new_size, Image.Resampling.LANCZOS)

        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error processing image: {e}")
        return

    prompt = "Please extract the largest number from the following image data. Do not include any other information or any other number."
    response = httpx.post(
        AIPROXY_URL+"/chat/completions",
        headers={
            "Authorization": f"Bearer {AIPROXY_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": [{"type": "text", "text": prompt}, {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}]}],
            "temperature": 1,
        },
    )
    card_number = response.json()["choices"][0]["message"]["content"].replace(" ", "")

    with open(output_file, 'w') as f:
        f.write(card_number)

async def find_most_similar_comments(input_file, output_file):
    validate_data_path(input_file, output_file)
    with open(input_file, 'r') as file:
        comments = file.readlines()

    comments = [comment.strip() for comment in comments]

    embeddings = await generate_embeddings(comments)

    similarity = np.dot(embeddings, embeddings.T)

    np.fill_diagonal(similarity, -np.inf)

    i, j = np.unravel_index(similarity.argmax(), similarity.shape)

    with open(output_file, 'w') as file:
        file.write(f"{comments[i]}\n")
        file.write(f"{comments[j]}\n")

def execute_sql_query(query: str, db_path: str, output_file: str, db_type: str = "sqlite"):
    validate_data_path(db_path, output_file)
    if not output_file.startswith("/data"):
        raise ValueError("Output file must be within the /data directory")

    if db_type == "sqlite":
        conn = sqlite3.connect(db_path)
    elif db_type == "duckdb":
        import duckdb
        conn = duckdb.connect(db_path)
    else:
        raise ValueError("Unsupported database type. Use 'sqlite' or 'duckdb'.")

    cursor = conn.cursor()

    cursor.execute(query)
    result = cursor.fetchall()

    with open(output_file, 'w') as f:
        for row in result:
            f.write(','.join(map(str, row)) + '\n')

def fetch_api_data(api_url: str, output_file: str):
    validate_data_path(output_file)
    response = httpx.get(api_url)
    response.raise_for_status()

    with open(output_file, 'w') as f:
        f.write(response.text)

def clone_and_commit(repo_url: str, commit_message: str, file_path: str, file_content: str):
    repo_dir = tempfile.mkdtemp()

    try:
        subprocess.run(["git", "clone", repo_url, repo_dir], check=True)

        os.chdir(repo_dir)

        with open(file_path, 'w') as f:
            f.write(file_content)

        subprocess.run(["git", "add", file_path], check=True)

        subprocess.run(["git", "commit", "-m", commit_message], check=True)

        subprocess.run(["git", "push"], check=True)
    finally:
        shutil.rmtree(repo_dir)

def scrape_website(url: str, selector: str, output_file: str):
    validate_data_path(output_file)

    time.sleep(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    
    elements = soup.select(selector)
    extracted_data = [elem.get_text(strip=True) for elem in elements]

    with open(output_file, 'w', encoding='utf-8') as f:
        for item in extracted_data:
            f.write(f"{item}\n")

def compress_image(input_file: str, output_file: str, quality: int = 85):
    validate_data_path(input_file, output_file)
    
    with Image.open(input_file) as img:
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.save(output_file, 'JPEG', quality=quality, optimize=True)

def resize_image(input_file: str, output_file: str, width: int = None, height: int = None):
    validate_data_path(input_file, output_file)
    
    if width is None and height is None:
        raise ValueError("Either width or height must be specified")
    
    with Image.open(input_file) as img:
        orig_width, orig_height = img.size
        if width is not None:
            ratio = width / orig_width
            new_height = int(orig_height * ratio)
            new_size = (width, new_height)
        else:
            ratio = height / orig_height
            new_width = int(orig_width * ratio)
            new_size = (new_width, height)
        
        img_resized = img.resize(new_size, Image.Resampling.LANCZOS)
        img_resized.save(output_file)

def convert_markdown_to_html(input_file: str, output_file: str):
    validate_data_path(input_file, output_file)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    html_content = markdown2.markdown(
        markdown_content,
        extras=[
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'task_list',
            'metadata',
            'footnotes',
            'strike',
            'spoiler'
        ]
    )
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Converted Markdown</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; line-height: 1.6; padding: 2em; max-width: 800px; margin: 0 auto; }}
            pre {{ background-color: #f6f8fa; padding: 1em; border-radius: 4px; overflow-x: auto; }}
            code {{ background-color: #f6f8fa; padding: 0.2em 0.4em; border-radius: 3px; }}
            img {{ max-width: 100%; }}
            table {{ border-collapse: collapse; width: 100%; margin: 1em 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f6f8fa; }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_template)

def filter_csv(input_file: str, output_file: str, filter_description: str):
    validate_data_path(input_file, output_file)

    df = pd.read_csv(input_file)
    
    column_info = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        sample = str(df[col].iloc[0]) if len(df) > 0 else "N/A"
        column_info.append(f"- {col} ({dtype}), example value: {sample}")
    
    prompt = f"""
Given this filter description: {filter_description}

The CSV file has the following columns:
{chr(10).join(column_info)}

Write a Python pandas filtering expression (just the condition) for this DataFrame.
Return only the filtering code, no explanation.
Example format: (df['column'] > 5) & (df['other'] == 'value')
"""
    filter_code = ask_llm(prompt).strip()

    filtered_df = df[eval(filter_code, {"df": df, "pd": pd})]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_df.to_dict(orient='records'), f, indent=2)

FUNCTION_MAP = {
    "count_days": count_days,
    "format_markdown": format_markdown,
    "sort_contacts": sort_contacts,
    "run_datagen": run_datagen,
    "write_recent_logs": write_recent_logs,
    "create_markdown_index": create_markdown_index,
    "extract_sender_email": extract_sender_email,
    "extract_credit_card_number": extract_credit_card_number,
    "find_most_similar_comments": find_most_similar_comments,
    "execute_sql_query": execute_sql_query,
    "fetch_api_data": fetch_api_data,
    "clone_and_commit": clone_and_commit,
    "scrape_website": scrape_website,
    "compress_image": compress_image,
    "resize_image": resize_image,
    "convert_markdown_to_html": convert_markdown_to_html,
    "filter_csv": filter_csv,
}
