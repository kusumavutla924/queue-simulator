# Project 10: Queue and Waiting Time Simulator

**Team:** <names, roll numbers>  |  **Course:** DAA, RGUKT Ongole

Simulates first-come first-served service at 1..19 counters, shows start/finish/wait for each
customer, compares the chosen number of counters with one extra counter, shows a busy/idle
timeline for each counter (my extension), and exports results to `simulation.csv`.

## Requirements
Python 3.10+ only. No pip packages, no internet.

## Run
From this folder (`daa_project_assignment`):

    py 10_queue_simulator/app.py          # Windows
    python3 10_queue_simulator/app.py     # macOS / Linux

Open http://127.0.0.1:8000 . Press Ctrl+C to stop. Use `PORT=8001` if the port is busy.

## Use
1. Paste CSV with the exact header `name,arrival,service` (integer minutes from opening).
2. Enter number of counters (1-19) and press *Simulate and compare one extra counter*.
3. Read the three tables: results, comparison, and the counter timeline.
4. Press *Export simulation* to write `simulation.csv`.

## Run the tests
    python3 10_queue_simulator/test_app.py

## Files
- `common.py` : shared browser toolkit (unchanged reference code, only the CSS dashes repaired)
- `10_queue_simulator/app.py` : application (reference code + my extension)
- `10_queue_simulator/test_app.py` : 8 automated tests
- `REPORT.md` : report

## Deploy on Render
1. Push this folder's contents to a GitHub repository (`common.py`, `10_queue_simulator/`, `requirements.txt`, `render.yaml`, README, REPORT).
2. On render.com: New > Web Service > connect the GitHub repo.
3. Runtime: Python 3. Build command: `echo ok`. Start command: `python 10_queue_simulator/app.py`. Instance type: Free.
4. Deploy. Render gives a link like https://queue-simulator-xxxx.onrender.com .
Note: the free plan sleeps after inactivity (first load can take ~1 minute) and data.json resets on redeploy/restart.
