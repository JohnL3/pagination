from flask import request
from bson.objectid import ObjectId

def paginate(mongo, collection_name, items_per_page = 3, pages_before_after = 1, sort_direction = 'DESC'):
    """
    This function is used to create the pagination 
    """
    sort_direction = pymongo.DESCENDING if sort_direction == 'DESC' else pymongo.ASCENDING
    dec = '$lte' if sort_direction == pymongo.DESCENDING else '$gte'
    filter_by = []
    total_items = 0
    all_items = []

    if request.args:
        try:
            mid_page = int(request.args.get('page'))
        except:
            mid_page = 1
        filter_with = request.args.get('filter_with')
    else:
        mid_page = 1
        filter_with = ''
    
    if not filter_with:
        all_items = list(mongo.db[collection_name].find().sort('_id', sort_direction))
    else:
        filter_by.append(filter_with)
        all_items = list(mongo.db[collection_name].find({'$and':[{'tags': {'$in':filter_by }}]}).sort('_id', sort_direction))
    
    total_items = len(all_items)

    if total_items > 0:
        
        total_pages = how_many_pages(total_items, items_per_page)
        mid_page = validate_mid_page(mid_page, total_pages)
        
        index_start_page = start_page_index(mid_page, items_per_page, total_items)

        nex = mid_page + 1 if mid_page + 1 < total_pages else total_pages
        previous = mid_page - 1 if mid_page - 1 > 0 else 1
        
        try:
            first = all_items[index_start_page]['_id']
        except:
            index_start_page = 0
            first = all_items[index_start_page]['_id']

        if not filter_with:
            results = mongo.db[collection_name].find({"_id":{ dec: ObjectId(first)}}).sort('_id', sort_direction).limit(items_per_page)
        else:
            results = mongo.db[collection_name].find({'$and':[{"_id":{ dec: ObjectId(first)}},{'tags': {'$in':filter_by }}]}).sort('_id', sort_direction).limit(items_per_page) 

        lis = get_pages(mid_page, total_pages, pages_before_after)

        return {"results": results, "lis": lis, "nex": nex, "previous": previous, "filter_with": filter_with, 'pages': True}
    
    return {'pages': False}

def how_many_pages(total_items, items_per_page):
    '''
    Return an int for how many pages will be needed
    '''

    total_pages = int(total_items/items_per_page)\
    if total_items % items_per_page == 0\
    else int(total_items/items_per_page) + 1
    
    return total_pages

def start_page_index(mid_page, items_per_page, total_items):
    '''
    Returns the index for the start page of list containing page numbers
    '''
    start = (mid_page -1) * items_per_page if not (mid_page -1) * items_per_page > total_items else 0
    
    return start

def get_pages(mid_page, total_pages, pages_before_after):
    '''
    Returns a list of dicts with page numbers for pagination
    In the form similar to:
    [{"page": None },{"page": 1, "highlight": True}, {"page": 2}, {"page": 3},{"page": None },{"page": 6 }]
    '''

    l_off = mid_page - pages_before_after if mid_page - pages_before_after > 0 else 1
    r_off = mid_page + pages_before_after + 1 if mid_page + pages_before_after <= total_pages else total_pages +1
    
    lis = [{'page': page} if not page == mid_page else {'page': page,'highlight': True} for page in range(l_off, r_off)]

    if not lis[0]['page'] == 1:
            lis.insert(0, {'page': None})  
    if  not lis[-1]['page'] == total_pages:
        lis.append({'page': None})
        lis.append({'page': total_pages})

    return lis

def validate_mid_page(mid_page, total_pages):
    '''
    This function checks to see if mid_page is within the range of pages available
    returns it if it is else sets it to 1 or value of last page depending on the value of mid_page
    '''
    if mid_page <= total_pages and mid_page >= 1:
        return mid_page
    else:
        mid_page = total_pages if mid_page > total_pages else 1
        return mid_page
