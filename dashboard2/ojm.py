"""
The off-line job monitor does offline sampling. This script is run on a login node as::

    > cd data/jobmonitor
    > module purge
    > module load hopper/2016a
    > module load Python
    > python ojm.py
    
This will produce an overview of the activity of the script as will as an 
overview of ill-performing jobs.

If you want to run the offline job monitor continuously::

    > nohup ./start.sh &

"""
from cfg import Cfg
from progress import printProgress
Cfg.offline = True

import os,time,argparse

from showq      import Sampler
from titleline  import title_line

#===============================================================================
if __name__=="__main__":
    parser = argparse.ArgumentParser('ojm')
    parser.add_argument('--show_progress','-s',action='store_true')
    args = parser.parse_args()
    print('ojm.py: command line arguments:',args)
    
    sampler = Sampler()
    
    running_flag = 'ojm.running'
    with open(running_flag,'w') as f:
        f.write('running')
    assert os.path.exists('ojm.running')
    
    print('\n'+title_line(                               char='=',width=100))
    print(     title_line('off-line job monitor started',char='=',width=100))
    stopped = False
    while not stopped: 
        timestamp = sampler.sample(verbose=False,show_progress=args.show_progress)
        stopped = not os.path.exists('ojm.running')
        minutes_to_sleep = int(Cfg.sampling_interval/60)
        print()
        for m in range(minutes_to_sleep+1):
            if args.show_progress:
                printProgress( m, minutes_to_sleep, prefix = 'Sleeping: ', suffix='minutes', decimals=-1)
            time.sleep(60)
        print('\n')

    print('\n\n-- off-line job monitor stopped --')



