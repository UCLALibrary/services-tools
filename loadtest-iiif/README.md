# Locust load test script
This script imports URIs from a specified file and stores it into a list. Once the list is stored, simulated users will select a random URL from the list in the load test.

```
pip3 install locustio

# Modify runner.py to change input files
locust -f runner.py  --host https://test-iiif.library.ucla.edu
locust -f runner.py  --host https://stage-iiif.library.ucla.edu
```
