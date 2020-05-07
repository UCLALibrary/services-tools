from locust import HttpLocust, TaskSet, task, between
import random
import re

f = open("50-60MB_url_lossy")
#f = open("110-130MB_url_lossy")
#f = open("50-60MB_url_lossless")
# = open("110-130MB_url_lossless")
iiif_urls = []

for x in f:
  iiif_urls.append(x.strip())

class MyTaskSet(TaskSet):
    @task
    def iiif_endpoint4(self):
        self.client.get(random.choice(iiif_urls) + "?cache=false")

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    wait_time = between(5, 15)
