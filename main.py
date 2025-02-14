from flask import Flask, request, jsonify
import asyncio
import json

app = Flask(__name__)

from functions import FUNCTION_MAP
from llm_utils import query_llm

@app.route('/run', methods=['POST'])
async def run_task():
    task = request.args.get('task')
    if not task:
        return jsonify({"error": "No task provided"}), 400
    try:
        llm_response = query_llm(task)
        tool_calls = llm_response.get("tool_calls", [])
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])

            print(f"Executing function: {function_name} with arguments: {arguments}")

            if function_name not in FUNCTION_MAP:
                return jsonify({"error": f"Unsupported function: {function_name}"}), 400
            function = FUNCTION_MAP[function_name]
            if asyncio.iscoroutinefunction(function):
                await function(**arguments)
            else:
                function(**arguments)
        return jsonify({"message": "Task executed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file():
    path = request.args.get('path')
    if not path or not path.startswith("/data"):
        return jsonify({"error": "Invalid file path"}), 400
    try:
        with open(path, 'r') as f:
            content = f.read()
        return content, 200
    except FileNotFoundError:
        return "", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)