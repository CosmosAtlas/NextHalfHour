"""
Main File for nhh (Next Half Hour)
"""

import PySimpleGUI as sg
from datetime import datetime, timedelta

def cnhh(now):
    h, m = now.hour, now.minute
    nhh = now
    nhh = nhh + timedelta(minutes=25)
    nhh = nhh.replace(second=0, microsecond=0)
    if (nhh.minute < 30):
        nhh = nhh.replace(minute = 30)
    else:
        nhh = nhh + timedelta(minutes=30)
        nhh = nhh.replace(minute=0)
    return nhh

layout = [
    [sg.Text('Next Half Hour', size=(20, 2), justification='left')],
    [sg.Text('', size=(10,2), font=('Helvetica', 20), justification='center', key='__CURTIME__'), sg.Text('next:', size=(10,2), justification='left'), sg.Text('', size=(10, 2), font=('Helvetica', 20), justification='center', key='__OUTPUT__')],
    [sg.Text('',size=(10,2), justification='right', key='startTime'), sg.ProgressBar(1000, orientation='h', key='progbar'), sg.Text('', size=(10,2), justification='left', key='endTime')],
    [sg.T(' ' * 5), sg.Button('Start', focus=True), sg.Cancel(),sg.Quit()]
]

window = sg.Window('Next Half Hour', layout)

monotasking, i = False, 0
diffTime = timedelta(seconds=0)
elapsedTime = timedelta(seconds=0)
startTime = datetime.now()
now = datetime.now()
nhh = cnhh(now)
timeT = now + timedelta(seconds=2)

while True:
    event, values = window.Read(timeout=1000)
    if event is None or event == 'Quit':
        break
    if event == 'Cancel':
        monotasking = False
        window.Element('progbar').UpdateBar(0)

    now = datetime.now()
    if event == 'Start':
        if not monotasking:
            monotasking = True
            window.Element('__CURTIME__').Update('FOCUS!')
            startTime = now
            diffTime = nhh - now

    if monotasking:
        if now > nhh:
            monotasking = False
            window.BringToFront()
            sg.Popup('Monotasking Section Complete!')
        elapsedTime = now - startTime
        window.Element('progbar').UpdateBar(1000 * elapsedTime/diffTime)
    else:
        window.Element('__CURTIME__').Update('{:02d}:{:02d}'.format(now.hour, now.minute))
        nhh = cnhh(now)
        startTime = now
        window.Element('__OUTPUT__').Update('{:02d}:{:02d}'.format(nhh.hour, nhh.minute))
    window.Element('startTime').Update('{:02d}:{:02d}'.format(startTime.hour, startTime.minute))
    window.Element('endTime').Update('{:02d}:{:02d}'.format(nhh.hour, nhh.minute))
