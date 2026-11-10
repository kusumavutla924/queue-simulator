"""Streamlit front end for Project 10 (Queue and Waiting Time Simulator).
It reuses parse_people, simulate and build_timeline from 10_queue_simulator/app.py."""
import csv
import io
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent / '10_queue_simulator'))
import app as queue_app

st.set_page_config(page_title='Queue Simulator', layout='wide')
st.title('Queue and Waiting Time Simulator')
st.caption('DAA Project 10 | RGUKT Ongole. Times are integer minutes from opening. '
           'First-come first-served; equal arrivals keep input order; the lowest counter number wins ties.')

csv_text = st.text_area('Customer data as CSV (header must be name,arrival,service)',
                        queue_app.SAMPLE, height=170)
counters = st.number_input('Number of counters', min_value=1, max_value=19, value=1, step=1)

if st.button('Simulate and compare one extra counter'):
    try:
        n = int(counters)
        people = queue_app.parse_people(csv_text)
        rows, average, maximum = queue_app.simulate(people, n)
        _, average2, maximum2 = queue_app.simulate(people, n + 1)
        st.session_state['result'] = {
            'rows': rows,
            'summary': [[n, f'{average:.2f}', maximum], [n + 1, f'{average2:.2f}', maximum2]],
            'timeline': queue_app.build_timeline(rows, n),
        }
    except ValueError as error:
        st.session_state.pop('result', None)
        st.error('Please check your input: ' + str(error))

result = st.session_state.get('result')
if result:
    st.subheader('Selected counter configuration')
    st.dataframe(pd.DataFrame(result['rows'], columns=['Person', 'Arrival', 'Service', 'Counter',
                                                       'Start', 'Finish', 'Wait']), hide_index=True)
    st.subheader('Configuration comparison')
    st.dataframe(pd.DataFrame(result['summary'], columns=['Counters', 'Average wait in minutes',
                                                          'Longest wait in minutes']), hide_index=True)
    st.subheader('Counter timeline (busy and idle periods)')
    st.dataframe(pd.DataFrame(result['timeline'], columns=['Counter', 'State', 'From', 'To', 'Person',
                                                           'Counter utilization']), hide_index=True)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['person', 'arrival', 'service', 'counter', 'start', 'finish', 'wait'])
    writer.writerows(result['rows'])
    st.download_button('Download simulation.csv', buffer.getvalue(), 'simulation.csv', 'text/csv')
