starting as micro-library.  goal api: 

(scrape site-vec processor-func address-func opts-map)

site-vec: vector of urls to start at

processor-func: function to handle each scraped page

address-func: function to call on url in scrape queue, returns url to scrape or nil to do nothing 

opts-map with following keys: 

option | default | description
--- | --- | ---
`:domain-depth` | 1 | depth to scrape each domain. 0 is just first page, 1 is follow links from first page, 2 is follow links from first page and each page thereafter, etc.
`:travel-depth` | 1 | number of domains to traverse. 0 is do not leave original domain, 1 is go one domain, 2 is go two domains, etc.
`:http-threads` | 2 | number of threads to spin up for http requests
`:processing-threads` | 2 | number of threads to spin up for handling 
`:stop-atom` | nil | symbol for atom to check on every scrape; if `true`, continue, if `false` then terminate execution. (e.g. change in callback function when enough pages are gathered)

once this is done, factor out into micro library and then can trivially build contract scraper out of it.

need to switch to jsoup; enlive isn't up to the job---no good get text, zero documentation, no updates in two years.

also need to do request error handling---think jsoup can just be made to swallow those, but then what does it return?

-- 

scrape contracts using core.async --- basic api will be designed to factor out into library later, pass in a filter (boolean-returning) function for pages to be matched against and a callback function for what to do with matches that parses, shoves into database, etc.  Also takes a maxpages-from-domain parameter to avoid slamming people.  

filter function will apply a fitted ML model to identify things that are contracts.  callback function will probably just append to a text file in my case, or maybe (if I feel ambitious) dump to a database.  though I don't really need database guarantees, so honestly the filesystem should be fine.

No code written yet, trying to design before writing.  But here's some...

Pseudocode: 

A.  Main function from commandline takes origin page, calls scrape-initiate function.  (Can also take a json with a list of origin pages)

B.  scrape-initiate function takes filter function and callback function and depth parameter (when this is a library these will be usercode supplied).  Then deposits origin url on decision queue as map {:inlinktext nil :url url}.  This sets off the chain.  (If passed a list, just puts each origin url on decision queue)

DECIDER FUNCTION (takes map with :inlink and :url ): 

1.  Watch decision queue. When something shows up:

2.  Check if url is in visited urls set.  If it is, terminate execution on the spot.
    
3.  Else, add url to visited urls set. (This is a potential problem, needs to avoid race condition with multiple decision functions having the same url.  I think using a transaction will solve it though---if I read the visited urls set and write to it in the same transaction then the [isolation of refs](https://clojure.org/reference/refs) should guarantee that no other thread can add between read and write.)

4.  Parse out domain name from url with helper function. 

5.  Check if domain name of url is in DOMAIN NAME MAP (atom).

6.  If domain is in map, increment value of domain in that map. 

7.  Else, add domain to map with value of 1.  (This doesn't need to be atomic, worst case scenario is I get one extra page, this is permissible error.)

8.  If number of domain in DOMAIN NAME MAP >= maxpages-from-domain, terminate execution.

9.  Else, deposit input map on fetch queue.
    
FETCH FUNCTION

1.  Watch fetch queue.  When something shows up there: 

2.  Make HTTP request for page.

3.  Deposit input map with (assoc input-map pagecontent) on parse queue

E.  PARSE FUNCTION

1.  Watch parse queue.  When something shows up there:

2.  extract all links from page and add each to decision queue in the form of {:inlinktext text-of-link :url url-of-link}

2.  pass input map to filter function.

3.  if filter function returns true, pass input map to callback function.  else terminate execution.
    
    
GLOBAL STATE:

1.  domain name map (map, atom)

2.  visited urls (set, in ref)

3.  fetch queue (core.async channel)

4.  parse queue (core.async channel)

5.  decision queue (core.async channel)
