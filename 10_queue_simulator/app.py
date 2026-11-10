"""First-come first-served simulation using earliest available counter.

Extension: busy/idle timeline for every counter (see build_timeline).
"""
import sys
import csv
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import Store, form, heading, note, table, run

SAMPLE = 'name,arrival,service\nA,0,4\nB,1,3\nC,2,2\nD,3,1'
store = Store(Path(__file__).with_name('data.json'),
              {'csv': SAMPLE, 'rows': [], 'summary': [], 'timeline': []})


def parse_people(text):
    reader = csv.DictReader(io.StringIO(text.strip()))
    if reader.fieldnames != ['name', 'arrival', 'service']:
        raise ValueError('Header must be exactly name,arrival,service')
    people, seen = [], set()
    for row in reader:
        if None in row or any(row[k] is None for k in reader.fieldnames):
            raise ValueError('Every row must have exactly three values.')
        name = row['name'].strip()
        arrival, service = int(row['arrival']), int(row['service'])
        if not name or name in seen or arrival < 0 or service <= 0:
            raise ValueError('Use unique names, nonnegative arrival and positive service times.')
        people.append([name, arrival, service])
        seen.add(name)
    if not people:
        raise ValueError('Add at least one customer.')
    return sorted(people, key=lambda p: p[1])


def simulate(people, counters):
    if not 1 <= counters <= 20:
        raise ValueError('Use 1 to 20 counters.')
    available, rows = [0] * counters, []
    for name, arrival, service in sorted(people, key=lambda p: p[1]):
        # Earliest possible start wins; ties go to the lowest counter number.
        counter = min(range(counters), key=lambda i: (max(arrival, available[i]), i))
        start = max(arrival, available[counter])
        finish = start + service
        available[counter] = finish
        rows.append([name, arrival, service, counter + 1, start, finish, start - arrival])
    average = sum(row[-1] for row in rows) / len(rows)
    maximum = max(row[-1] for row in rows)
    return rows, average, maximum


def build_timeline(rows, counters):
    """EXTENSION: list Busy and Idle periods for each counter.

    Time runs from 0 to the finish time of the last customer overall.
    Returns rows [counter, 'Busy'/'Idle', from, to, person, utilization%].
    """
    horizon = max(r[5] for r in rows)
    result = []
    for c in range(1, counters + 1):
        mine = sorted((r for r in rows if r[3] == c), key=lambda r: r[4])
        cursor, busy_total, periods = 0, 0, []
        for name, _, _, _, start, finish, _ in mine:
            if start > cursor:
                periods.append([c, 'Idle', cursor, start, '-'])
            periods.append([c, 'Busy', start, finish, name])
            busy_total += finish - start
            cursor = finish
        if cursor < horizon:
            periods.append([c, 'Idle', cursor, horizon, '-'])
        percent = f'{100 * busy_total / horizon:.0f}%'
        result.extend(p + [percent] for p in periods)
    return result


def view():
    out = note('All times are minutes from opening. Equal arrivals retain input order. '
               'Service is not interrupted.')
    out += form('simulate', [('csv', 'Customer data as CSV', 'textarea', store.data['csv']),
                             ('counters', 'Number of counters', 'number', '1')],
                'Simulate and compare one extra counter')
    out += heading('Selected counter configuration')
    out += table(['Person', 'Arrival', 'Service', 'Counter', 'Start', 'Finish', 'Wait'],
                 store.data['rows'])
    out += heading('Configuration comparison')
    out += table(['Counters', 'Average wait in minutes', 'Longest wait in minutes'],
                 store.data['summary'])
    out += heading('Counter timeline (busy and idle periods)')
    out += table(['Counter', 'State', 'From', 'To', 'Person', 'Counter utilization'],
                 store.data.get('timeline', []))
    out += form('export', [], 'Export simulation')
    return out


def handle(data):
    if data['action'] == 'simulate':
        people = parse_people(data['csv'])
        counters = int(data['counters'])
        if not 1 <= counters <= 19:
            raise ValueError('Use 1 to 19 counters so one extra can be compared.')
        rows, average, maximum = simulate(people, counters)
        _, other_average, other_maximum = simulate(people, counters + 1)
        store.data = {'csv': data['csv'], 'rows': rows,
                      'summary': [[counters, f'{average:.2f}', maximum],
                                  [counters + 1, f'{other_average:.2f}', other_maximum]],
                      'timeline': build_timeline(rows, counters)}
        store.save()
    elif data['action'] == 'export':
        if not store.data['rows']:
            raise ValueError('Run a simulation first.')
        with Path(__file__).with_name('simulation.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.writer(stream)
            writer.writerow(['person', 'arrival', 'service', 'counter', 'start', 'finish', 'wait'])
            writer.writerows(store.data['rows'])
        return note('Exported simulation.csv into this project folder.')
    else:
        raise ValueError('Unknown action.')


if __name__ == '__main__':
    run('Queue and Waiting Time Simulator', view, handle)
