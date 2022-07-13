import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


def job_one_hour():
    filename = 'products_check.py'
    subprocess.Popen('python '+filename, shell=True).wait()


scheduler = BlockingScheduler()
scheduler.add_job(job_one_hour, 'cron', minutes="6-22")
scheduler.start()
