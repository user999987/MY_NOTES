```python
x='1960-01-06'
datetime.strptime(x,'%Y-%m-%d').strftime('%m/%d/%Y')
```
strftime - Convert object to a string according to a given format <br>
strptime - Parse a string into a datetime object given a corresponding format