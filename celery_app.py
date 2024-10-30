from celery import Celery

app = Celery('dining_philosophers', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

import philosopher 
