(ns scrapecontracts.scraper.requests
  (:require [org.httpkit.client :as http]
            [clojure.core.async :refer [go go-loop chan >! <!]]
            [scrapecontracts.scraper.soup :refer [parse]]))

(def parse-transducer
  (comp
   (map :body)
   (map parse)))

(defn- get [inchan address]
  (http/get address #(go (>! inchan %))))
;; error handling needs to be somewhere either in get or in parse-transduer


(defn- make-http-channel [addresses]
  (let [inchan (chan 1 parse-transducer)]
    (dorun
     (map (partial get inchan) addresses))
    inchan))

(defn- watch-http-channel [http-channel, callback]
  (go-loop []
    (callback (<! http-channel))
    (recur)))


(defn fetch [addresses callback]
  (let [inchan (make-http-channel addresses)
        getter (partial get inchan)
        cb (partial callback getter)]
    (watch-http-channel inchan cb)
    getter))

;; example:
;; (def outatom (atom []))
;; (fetch ["http://paul-gowder.com" "http://rulelaw.net"] #(swap! outatom conj %2))
;; (count @outatom) => 2


;; callback function has special requirements: will take getter as its first argument and result of transducer on http-channel as second argument.  When not a crawler, the first argument won't be used and can be discarded (thus the example that just uses the second argument).  When it is a crawler, the callback can use the getter to queue up links found in the results for recursive scraping.  

;; For example, I think that (defn callback [getter item] (dorun (map getter (:links item)))) should work to just take every link from every page and fetch that too, and so forth, recursively...

;; this new thing noted in previous 2 comments is TOTALLY UNTESTED.  