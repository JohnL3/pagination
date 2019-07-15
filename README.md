# Pagination with flask and mongo

### About

I never used pagination in any project that I have done. So decided I would try out using pagination in a 
flask test project where I was trying out things in flask that I had not covered or covered in depth before.  

I had intended to look up how to do it and add it to project .... but then realizing unlike with
Flask-SQLAlchemy pagination is not built in with py-mongo so it was either follow a tutorial by somebody who created it themself or create one myself .... so went with the latter and created my own function for pagination. 


#### How to use it.

```python
from <...> import pagination

@app.route('videos')
def videos():

    context = pagination(mongo, "videos", 2, 2)
    return render_template('videos.html', context=context)
```