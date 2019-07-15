# Pagination with flask and mongo

#### How to use it.

```python
from <...> import pagination

@app.route('videos')
def videos():

    context = pagination(mongo, "videos", 2, 2)
    return render_template('videos.html', context=context)
```