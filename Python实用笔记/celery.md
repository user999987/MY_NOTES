### Client side
pip install celery \
application code 
```python
# app.py
from celery import Celery

app = Celery('tasks', broker='redis://<broker_ip>')

result = app.send_task('tasks.add', args=(4, 4))
print(result.get())

```

### Worker
pip install celery \

```python
# worker.py
from celery import Celery

app = Celery('tasks', broker='redis://<broker_ip>')

@app.task
def add(x, y):
    return x + y
```
```bash
celery -A worker worker --loglevel=info
```
Ensure that the celery command is executed in the same directory where the worker.py file is located.

In this setup, the implementation of the add task is defined only on the worker machine. The application code on Machine A sends a task to the Redis broker, specifying the task name as 'tasks.add' (where 'tasks' is the Celery app name and 'add' is the task name). The Celery worker running on Machine B listens to the broker for new tasks and executes them. The result is then retrieved by the application code on Machine A using the result.get() method.