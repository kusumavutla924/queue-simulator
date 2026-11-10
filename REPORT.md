# Report: Queue and Waiting Time Simulator

**Team members:** <fill in>   **Project:** 10 (Queue and Waiting Time Simulator)

## 1. Problem
A service office wants to know how long customers wait with one or several counters, and whether
adding one more counter helps. The app simulates the queue and reports waits and counter usage.

## 2. Features and input rules
- Input CSV header exactly `name,arrival,service`; times are integer minutes from opening.
- Names must be unique, arrival >= 0, service > 0. Counters: 1 to 19 (so one extra can be compared).
- Customers are served in arrival order (stable sort keeps input order for equal arrivals).
- Service is non-preemptive; if several counters can start a customer at the same time the lowest counter number is chosen.
- Outputs: per-customer table, average and longest wait, comparison with one extra counter,
  busy/idle timeline (extension), CSV export.
- *(Insert screenshot of the working app here.)*

## 3. Main functions and saved data
- `parse_people(text)` : validates CSV, returns `[name, arrival, service]` sorted by arrival.
- `simulate(people, counters)` : keeps `available[i]` = time counter i becomes free. For each customer it
  picks the counter minimising `(max(arrival, available[i]), i)`, then `start = max(arrival, available)`,
  `finish = start + service`, `wait = start - arrival`. Returns rows, average wait, longest wait.
- `build_timeline(rows, counters)` **(my extension)** : for each counter, walks its customers in start order;
  a gap between the previous finish and the next start is an *Idle* period, otherwise *Busy*. Time runs from 0 to
  the finish of the last customer overall, and utilization = busy minutes / that horizon.
- `view()` / `handle()` : build the page and process the `simulate` and `export` actions.
- `data.json` stores the CSV text, result rows, comparison and timeline; `simulation.csv` is the export.

## 4. Worked example
Input: A(0,4) B(1,3) C(2,2) D(3,1).
One counter: waits 0,3,5,6 -> average 3.50, longest 6.
Two counters: A and B start immediately, C starts at 4 (wait 2), D starts at 4 (wait 1) -> average 0.75, longest 2.
Timeline with two counters: counter 2 is Idle 0-1, Busy 1-4 (B), Busy 4-5 (D), Idle 5-6.

## 5. Tests (run with `python3 10_queue_simulator/test_app.py`)
| # | Input / action | Expected | Actual |
|---|---|---|---|
| 1 | Default data, 1 counter | waits 0,3,5,6; avg 3.5; max 6 | Pass |
| 2 | Default data, 2 counters | waits 0,0,2,1; avg 0.75; max 2 | Pass |
| 3 | Arrivals 0,10,20 each service 2, 1 counter | all waits 0 | Pass |
| 4 | Zed and Amy both arrive at 0 | Zed served first | Pass |
| 5 | Zero service, negative arrival, duplicate name, bad header, missing column | ValueError each time | Pass |
| 6 | 0 and 21 counters | ValueError | Pass |
| 7 | Timeline, default data, 2 counters | counter 2 Idle 0-1, Busy B 1-4, Idle 5-6; counter 1 never idle | Pass |
| 8 | Timeline, 1 counter | utilization 100% | Pass |
A live HTTP form submission was also checked: the page showed average wait 3.50 and the timeline.

## 6. Extension, limitations, reference code and AI assistance
- **Extension:** busy/idle timeline and utilization per counter (extension task 1 of Project 10).
- **Limitations:** integer minutes only; identical counters; no priorities; timeline ends at the last finish time;
  single local user.
- **Reference code:** `common.py` and the base of `app.py` come from the DAA project assignment handout.
  I only repaired CSS property names that were broken by PDF line wrapping (`border-radius`, `min-height`, `pre-wrap`).
- **AI assistance:** Claude (Anthropic) helped write the extension, the tests, the README and this report.
  <Edit this section to state honestly what you did yourself.>
