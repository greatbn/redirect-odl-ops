from __future__ import absolute_import, unicode_literals
from celery import Celery
import config


dvnh_worker = Celery('worker',
                     broker=config.BROKER_URI,
                     backend=config.BACKEND_URI,
                     include=['worker.handler'])



dvnh_worker.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    dvnh_worker.start()
