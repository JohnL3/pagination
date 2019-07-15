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
  - you would just add the pagination.html to your main page useing the include statement as shown in file
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
The paginate function takes 4 parameters  
- mongo connection
- collection_name: name of the database collection
- Items_per_page: (default is set to 3)
- pages_before_after: (default is set to 1)

The function returns  
```python
return {"results": results, "lis": lis, "nex": nex, "previous": previous, "filter_with": filter_with, 'pages': True}
```

- results: Items returned from database
- lis: list of page numbers for pagination in the following form it can also contain page: None to indicate pages before and after as shown next.
  - [{"page": None},{"page": 3}, {"page": 4, "highlight": True}, {"page": 5}, {"page": None},{"page": 6}]
  - highlight: True ... I used this to indicate with css which page i was on 
- nex: the next page for data .. which goes at end of page numbers
- previous: the previous page for data that goes before page numbers
- filter_with: used if filtering database
- pages: used to let frontend know it they were items in database to display  and also in conjunction with filter_with to let frontend know if there was filter results

```python
from <...> import paginate

@app.route('videos')
def videos():

    context = paginate(mongo, "videos", 2, 2)
    return render_template('videos.html', context=context)
```
This is how things would look in browser .... 
![A test image](images/browser.jpg)

This is how the pagination would look  
![A test image](images/pagination.jpg)