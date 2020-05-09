from flask import request
from bson.objectid import ObjectId
from flask_pymongo import pymongo


def filtering(mongo, req, route,  per_page = 2, pages_before_after = 1, sort_direction='ASC'):
    """
    This function is used If filter section is on the page as well as pagination 
    """
    filter_and = dict(req.args.to_dict())

    try:
        del filter_and['page']
    except:
        pass

    if len(filter_and) > 0:
        my_filter = {'$and':[filter_and]}
        qry_str = ''

        try:
            filter_in = request.args.getlist('filter_with')
            filter_in[0] = filter_in[0].lower()
            del filter_and['filter_with']
            for itm in filter_in:
                qry_str+= f'&filter_with={itm.lower()}'
            my_filter['$and'].append({'tags': {'$in': filter_in}})
        except:
            pass

        for k,v in filter_and.items():
            qry_str += f'&{k}={v.lower()}'

        filter_with = {'qry_str': qry_str}
        context = paginate(mongo, route, per_page, pages_before_after, my_filter, sort_direction, False)
        return (context, True, filter_with)
    else:
        context = paginate(mongo, route, per_page, pages_before_after, {}, sort_direction)
        return (context, False)

def paginate(mongo, collection_name, items_per_page = 3, pages_before_after = 1, my_filter={}, sort_direction = 'DESC', dont_filter=True):
    """
    This function is used to create the pagination 
    """
    
    sort_direction = pymongo.DESCENDING if sort_direction == 'DESC' else pymongo.ASCENDING
    dec = '$lte' if sort_direction == pymongo.DESCENDING else '$gte'
    total_items = 0
    all_items = []

    if request.args:
        try:
            mid_page = int(request.args.get('page'))
        except:
            mid_page = 1
    else:
        mid_page = 1
    
    if dont_filter:
        all_items = list(mongo.db[collection_name].find().sort('_id', sort_direction))
    else:
        all_items = list(mongo.db[collection_name].find(my_filter).sort('_id', sort_direction))
    
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

        if dont_filter:
            results = mongo.db[collection_name].find({"_id":{dec: ObjectId(first)}}).sort('_id', sort_direction).limit(items_per_page)
        else:
            my_filter['$and'][0]['_id']={dec: ObjectId(first)}
            print('my_filter fun', my_filter)
            results = mongo.db[collection_name].find(my_filter).sort('_id', sort_direction).limit(items_per_page) 

        lis = get_pages(mid_page, total_pages, pages_before_after)
       
        return {"results": results, "lis": lis, "nex": nex, "previous": previous, "dont_filter": dont_filter, 'pages': True}
    
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
