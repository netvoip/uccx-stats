#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from uccx_dbquery import dbquery

results = dbquery('select * from RtCSQsSummary')
Text = str(datetime.now()) + '\n\n'
for i in results:
    # Active agents = workingagents + talkingagents + reservedagents + availableagents
    Active = i[15] + i[16] + i[17] + i[2]
    # Ratio = callshandled / totalcalls
    if i[4]>0:
        Ratio = round(i[6]/i[4], 3)
    else:
        Ratio = 0
    Text += '{} - loggedinagents={}\n'.format(str(i[0]), str(i[1]))
    Text += '{} - availableagents={}\n'.format(str(i[0]), str(i[2]))
    Text += '{} - unavailableagents={}\n'.format(str(i[0]), str(i[3]))
    Text += '{} - talkingagents={}\n'.format(str(i[0]), str(i[16]))
    Text += '{} - Active={}\n'.format(str(i[0]), str(Active))
    Text += '{} - callswaiting={}\n'.format(str(i[0]), str(i[13]))
    Text += '{} - totalcalls={}\n'.format(str(i[0]), str(i[4]))
    Text += '{} - callshandled={}\n'.format(str(i[0]), str(i[6]))
    Text += '{} - callsabandonded={}\n'.format(str(i[0]), str(i[7]))
    Text += '{} - callsdequeued={}\n'.format(str(i[0]), str(i[8]))
    Text += '{} - CallRatio={}\n'.format(str(i[0]), str(Ratio))
    Text += '{} - avgtalkduration={}\n'.format(str(i[0]), str(round(i[9]/1000)))
    Text += '{} - avgwaitduration={}\n'.format(str(i[0]), str(round(i[10]/1000)))
    Text += '{} - longesttalkduration={}\n'.format(str(i[0]), str(round(i[11]/1000)))
    Text += '{} - longestwaitduration={}\n'.format(str(i[0]), str(round(i[12]/1000)))
    Text += '{} - oldestcontact={}\n'.format(str(i[0]), str(round(i[5]/1000)))

path = os.path.dirname(os.path.abspath( __file__ ))
File = open(os.path.join(path, '_uccx_csqstats.txt'), 'w+')
File.write(Text)
File.close()
print(Text)