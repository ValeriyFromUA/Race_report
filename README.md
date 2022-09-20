<h2>This program is designed to output the Monaco Race report.</h2>

<h4>Main used libraries in requirements.txt</h4>
***

* <h2>Importantly:</h2>

  **Also need to install
  "Task-5-Report-Monaco 2.0" from test.pypi.org**

```pip install -i https://test.pypi.org/simple/ Task-5-Report-Monaco```

**https://test.pypi.org/project/Task-5-Report-Monaco/**


***
About:

build_report(path) returns a list of two reports:

* [0] - list of strings, example:

```['Sebastian Vettel | FERRARI | 0:01:04.415000', 'Valtteri Bottas | MERCEDES | 0:01:12.434000']```

* [1] - list of dicts, example:

```[{'abbr': 'SVF', 'name': 'Sebastian Vettel', 'team': 'FERRARI', 'lap_time': '0:01:04.415000'},{'abbr': 'VBM', 'name': 'Valtteri Bottas', 'team': 'MERCEDES', 'lap_time': '0:01:12.434000'}]```

* in both cases data sorted by lap_time

***

* get_abbr_and_time_data(path, start_or_end_file) return dict, key is abbr, value is time, example:

```{'SVF': '12:02:58.917', 'NHR': '12:02:49.914', 'FAM': '12:13:04.512'}```