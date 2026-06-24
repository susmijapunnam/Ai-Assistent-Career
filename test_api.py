from job_api import fetch_jobs


if __name__ == '__main__':
    try:
        jobs = fetch_jobs("Python Developer")
        print(jobs)
    except Exception as e:
        print("Could not fetch live jobs:", e)
        print("Make sure RAPIDAPI_KEY is set in the environment.")
