#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from datetime import datetime
from uccx_dbquery import dbquery

results = dbquery('select * from RtICDStatistics')
Text = str(datetime.now()) + '\n\n'
for i in results:
    # Active agents = workingagents + talkingagents + reservedagents + availableagents
    Active = i[3] + i[4] + i[5] + i[6]
    Text += '{} - Active={}\n'.format(str(i[0]), str(Active))
    Text += '{} - loggedinagents={}\n'.format(str(i[0]), str(i[2]))
    Text += '{} - availableagents={}\n'.format(str(i[0]), str(i[6]))
    Text += '{} - unavailableagents={}\n'.format(str(i[0]), str(i[7]))
    Text += '{} - totalcalls={}\n'.format(str(i[0]), str(i[8]))
    Text += '{} - callswaiting={}\n'.format(str(i[0]), str(i[9]))
    Text += '{} - callshandled={}\n'.format(str(i[0]), str(i[10]))
    Text += '{} - callsabandoned={}\n'.format(str(i[0]), str(i[11]))

path = os.path.dirname(os.path.abspath( __file__ ))
File = open(os.path.join(path, '_uccx_overall.txt'), 'w+')
File.write(Text)
File.close()
print(Text)