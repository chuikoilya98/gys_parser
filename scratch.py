from crontab import CronTab

cron = CronTab(user="root")

my_cron = CronTab(user=True)

job = cron.new(command='python3 /root/gys_parser/worker.py')

job.minute.every(1)

cron.write()
