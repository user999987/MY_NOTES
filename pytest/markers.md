```python 
# 单独测试特定函数
pytest -v file::function
```
Page 30 Exception测试

Page 31 Marking test 
```
pytest -v -m get xxxx.py
pytest -v -m "get and somke" xxx.py
```

Page 46 
```python
@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
class TestAdd():
    def test_equivalent(self, task):
        ...
```
When you apply parametrize() to classes, the same test data will be sent to all the test methods in the class.

Page 65
```python
tasks_to_try = (Task('sleep',done=True),
Task('wake','brian')
)
# The request listed in the fixture parameter is another builtin fixture that represents the calling state of the fixture. It has a field param that is filled with one element from the list assigned to params in @pytest.fixture(params_to_try)
@pytest.fixture(params=tasks_to_try)
def a_task(request):
    return request.param
```

Page 74
```python
@pytest.fixture(scope='module')
def author_file_json(tmpdir_factory):
    # make a python dic
    python_author_data = {'x0':{'x00':'x000'}}
    # make a dir under tmpdir and json file under data dir
    file_ = tmpdir_factory.mktemp('data').join('author_file.json')
    with file.open('w') as f:
        json.dump(python_author_data, f)
    return file

def test_file_content(author_file_json):
    with author_file_json.open() as f:
        content = json.load(f)
    asssert content['x0']['x00'] = 'x000'
```