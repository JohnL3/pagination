# Pagination with flask and mongo

### About

I never used pagination in any project that I have done. So decided I would try out using pagination in a 
flask test project where I was trying out things in flask that I had not covered or covered in depth before.  

I had intended to look up how to do it and add it to project .... but then realizing unlike with
Flask-SQLAlchemy pagination is not built in with py-mongo so it was either follow a tutorial by somebody who created it themself or create one myself .... so went with the latter and created my own function for pagination.  

I initially created a working version ... but decided there were a few things I did not like so created a version 2
... and then decided to post it seperately from the test project I am working on.  

#### Items in files

- repository comes with the pagination.py file ... this contains the code for the pagination
- templates folder ( these are not required ... but can be used saving you having to create ones from scratch )
  - Within the templates folder there is a partails folder containg small html sections that can be included in your html page
  - The most important one being the paginate.html
- Videos.html ... this can be renamed and reused for your main page that you want your pagination on 
  - you would just add the pagination.html to your main page using the include statement as shown in file
- A filter html section 
  - As I added the ability to also  filter within the pagination function ... 
  - if you dont require you database to be filtered you can leave out the filter.html
  - if you would like to also be able to filter database you will more than likely also have to make some changes to the pagination function ... but I beleive this can easily be done without to much difficulty



#### How to use it.

First you need to put the pagination.py file somewhere ... I used a module which I named helper_functions ... in which i place a blank \_\_init\_\_.py file.
And I put the pagination.py file in this module.  
You would then import the paginate function from this location into your app.py file along with your other imports.    
you would then use the function in a route that you wanted the data sent to frontend paginated ... as shown below ... passing in the 
revelant parameters.  
The paginate function takes 7 parameters  
- mongo connection
- collection_name: name of the database collection
- Items_per_page: (default is set to 3)
- pages_before_after: (default is set to 1)
- my_filter: a dictionary with the filter you want to use ... gets passed into database query
- sort_direction: tells funtcion to sort database results by DESCENDING or ASCENDING
- dont_filter: set to True if your not filtering

The function returns  
```python
return {"results": results, "lis": lis, "nex": nex, "previous": previous, "dont_filter": dont_filter, 'pages': True}
```

- results: Items returned from database
- lis: list of page numbers for pagination in the following form it can also contain page: None to indicate pages before and after as shown next.
  - [{"page": None},{"page": 3}, {"page": 4, "highlight": True}, {"page": 5}, {"page": None},{"page": 6}]
  - highlight: True ... I used this to indicate with css which page i was on 
- nex: the next page for data .. which goes at end of page numbers
- previous: the previous page for data that goes before page numbers
- pages: used to let frontend know it they were items in database to display
- dont_filter: a variable used to tell function if a filter is being used

```python
from <...> import paginate

@app.route('videos')
def videos():
    # usage if no filter is being used on page
    context = paginate(mongo, "videos", 2, 2, 'DESC')
    return render_template('videos.html', context=context)


@app.route('videos')
def videos():
    # usage if filter is being used on page
    filtered = filtering(mongo, request, 'videos', 2, 1, 'ASC')
    
    if filtered[1]:
        return render_template('videos.html',  v=True, context=filtered[0], **filtered[2])
    else:
        return render_template("videos.html", v=True, context=filtered[0])
```
This is how things would look in browser .... 
![A test image](images/browser.jpg)

This is how the pagination would look  
![A test image](images/pagination.jpg)

```python
from <...> import paginate

@app.route('videos')
def videos():
    '''
    When filtering you need to create the query and pass it into function
    You need to pass down a string in the render_template to add the filter as arguments to the pages href
    below is one way to do it ... 
    '''
    filter_and = dict(request.args.to_dict())
    try:
        del filter_and['page']
    except:
        pass
    
    if len(filter_and) > 0:
        my_filter = {'$and':[filter_and]}
        qry_str = ''

        try:
            filter_in = request.args.getlist('tags_in')
            del filter_and['tags_in']
            for itm in filter_in:
                qry_str+= '&tags_in=' + itm

            my_filter['$and'].append({'tags': {'$in': filter_in}})
        except:
            pass

        for k,v in filter_and.items():
            qry_str+= '&' + k + '=' + v
        
        filter_with = {'qry_str': qry_str}

        context = paginate(mongo, "videos", 2, 2, my_filter,'ASC', False)
        return render_template('videos.html', context=context, **filter_with)
    else:
        # usage if no filter is being applied
        context = paginate(mongo, "videos", 2, 2, 'DESC', False)
    return render_template('videos.html', context=context)
```