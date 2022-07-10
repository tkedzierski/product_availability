import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


def job_one_hour():
    filename = 'products_check.py'
    while True:
        p = subprocess.Popen('python '+filename, shell=True).wait(160)

        if p != 0:
            continue
        else:
            break


scheduler = BlockingScheduler()
scheduler.add_job(job_one_hour, 'interval', minutes=60)
scheduler.start()
