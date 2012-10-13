from time import time

import psycopg2

from urlparse import urlparse, ParseResult

connection = psycopg2.connect("dbname=internet user=donatas")
cursor = connection.cursor()

def save():
    connection.commit()

def execute(query, args=None, ret=True):
    cursor.execute(query, args)
    if ret:
        return cursor.fetchone()

def createTable():
    query = '''
    -- Table: urls
    
    -- DROP TABLE urls;
    
    CREATE TABLE urls
    (
      id serial NOT NULL,
      path text,
      website_id integer,
      scanned timestamp without time zone,
      parent integer,
      CONSTRAINT urls_pkey PRIMARY KEY (id ),
      CONSTRAINT urls_website_url_key UNIQUE (website_id , path )
    )
    WITH (
      OIDS=FALSE
    );
    ALTER TABLE urls
      OWNER TO postgres;
    '''
    execute(query)
    save()

def cleanDatabase():
    execute('DELETE FROM websites;', ret=False)
    execute('DELETE FROM urls;', ret=False)
    save()

def getUrls():
    cursor.execute("SELECT * from urls;")
    return cursor.fetchone()

def cleanTable():
    pass

def _getPath(data):
    scheme, netloc, url, params, query, fragment = data
    if params:
        url = "%s;%s" % (url, params)
    if query:
        url = url + '?' + query
#    if fragment:
#        url = url + '#' + fragment
    return url

class URL():
    id = None
    string = None

def getWebsiteId(website):
    result = execute('SELECT id FROM websites WHERE name = %s;', (website,))
    if not result:
        result = execute('INSERT INTO websites(name) VALUES (%s) RETURNING id;', (website,))
        save()
    return result[0]

def addUrl(url, parent_id=0):
    parsed = urlparse(url)#TODO: clear segment
    path = _getPath(parsed)
    websiteId = getWebsiteId(parsed.netloc)
    result = execute("SELECT id FROM urls WHERE website_id = %s AND path = %s;", (websiteId, path))
    if result:
        return None
    result = execute("INSERT INTO urls (path, website_id, scanned, parent_id) VALUES (%s, %s, %s, %s) RETURNING id",
                            (path, websiteId, psycopg2.TimestampFromTicks(time()), parent_id))
    save()
    return (result[0], parsed.geturl())

def addManualUrl(url):
    return addUrl(url)
#    site = addUrl(url)
#    if id:
#        return (id, url)
#    return None

def getJob():
    url = addManualUrl('http://www.delfi.lt')
    if url:
        return [url]
    return None
#    return [addManualUrl('http://www.delfi.lt')]
