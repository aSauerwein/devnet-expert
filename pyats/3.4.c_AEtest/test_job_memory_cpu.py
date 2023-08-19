#usage: pyats run job test_job_memory_cpu.py  --testbed testbed-cat8kv.yaml 

from pyats.easypy import run

def main():

    run('./memory_cpu_aetest.py')
