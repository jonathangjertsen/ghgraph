Downloads stats from Github API and make a graph of open/closed issues + n issues tagged 'bug'

Usage: create a file named `my_secret.py` in this folder with the following contents

```Python
PAT = "ghp_my_pat"
REPO = "my_org_or_user/my_repo_name"
```

To download stats:

```
python download.py
```

To graph them

```
python graph.py
```
