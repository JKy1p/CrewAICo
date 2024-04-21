from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv

from crew import AccountResearchCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger
from langsmith import traceable
from utils.logging import debug_process_inputs
import traceback


load_dotenv()

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app, resources={r"/api/*": {"origins": "*"}})

@traceable(name="kick off crew", process_inputs=debug_process_inputs)    
def kickoff_crew(job_id, target_account: str, topics: list[str]):
    logger.info(f"Running kickoff_crew with job_id={job_id}, target_account={target_account}, topics={topics}")

    results = None
    try:
        account_research_crew = AccountResearchCrew(job_id)
        account_research_crew.setup_crew(
            target_account, topics)
        results = account_research_crew.kickoff()
        logger.info(f"Crew for job {job_id} is complete", results)

    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        logger.error(traceback.format_exc())
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))

@traceable(name="run crew", process_inputs=debug_process_inputs)    
@app.route('/api/crew', methods=['POST'])
def run_crew():
    logger.info("Received request to run crew")
    # Validation
    data = request.json
    if not data or 'target_account' not in data or 'topics' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    target_account = data['target_account']
    topics = data['topics']

    thread = Thread(target=kickoff_crew, args=(
        job_id, target_account, topics))
    thread.start()

    return jsonify({"job_id": job_id}), 202

@traceable(name="get status", process_inputs=debug_process_inputs)    
@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")

    # Initialize result_json as None to handle cases where job.result is None
    result_json = None
    # Only attempt to parse job.result if it's not None
    if job.result is not None:
        try:
            result_json = json.loads(job.result)
        except json.JSONDecodeError:
            # If parsing fails, set result_json to the original job.result string
            result_json = job.result

    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })

if __name__ == '__main__':
    app.run(debug=True, port=3001)
