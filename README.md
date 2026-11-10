# Project 10: Queue and Waiting Time Simulator

**Team:** <names, roll numbers>  |  **Course:** DAA, RGUKT Ongole
**Live app:** https://queue-simulator-hpsyvtcpbhnx5z3mbermpj.streamlit.app
**Source code:** https://github.com/kusumavutla924/queue-simulator

Simulates first-come first-served service at 1..19 counters, shows start/finish/wait for each
customer, compares the chosen number of counters with one extra counter, shows a busy/idle
timeline for each counter (my extension), and exports results to CSV.

## Ways to run
**A. Online (Streamlit Community Cloud):** open the live link above, press *Simulate*.
Change the number of counters and press *Simulate* again to see new results.

**B. Local browser app (Python 3.10+ only, no packages):**

    py 10_queue_simulator/app.py          # Windows
    python3 10_queue_simulator/app.py     # macOS / Linux

Open http://127.0.0.1:8000 . Press Ctrl+C to stop. Use PORT=8001 if the port is busy.

**C. Local Streamlit version:**

    pip install streamlit
    streamlit run streamlit_app.py

## Use
1. Paste CSV with the exact header `name,arrival,service` (integer minutes from opening).
2. Enter number of counters (1-19) and press the Simulate button.
3. Read the three tables: results, comparison, and the counter timeline.
4. Export / download the results as `simulation.csv`.

## Run the tests
    python3 10_queue_simulator/test_app.py

## Files
- `common.py` : shared browser toolkit from the handout (CSS repaired, page building moved to `render_page`)
- `10_queue_simulator/app.py` : application logic (reference code + my extension)
- `10_queue_simulator/test_app.py` : 8 automated tests
- `streamlit_app.py` : Streamlit front end used for the online deployment
- `requirements.txt` : `streamlit` (needed only for options A and C)
- `REPORT.md` : report
