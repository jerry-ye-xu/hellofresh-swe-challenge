import os
from time import sleep

print(os.environ['POSTGRES_DATABASE'])
print(os.environ['POSTGRES_USER'])
print(os.environ['POSTGRES_PASSWORD'])
print(os.environ['POSTGRES_HOST'])
print(os.environ['POSTGRES_PORT'])

while True:
    sleep(3)
    print("running...")