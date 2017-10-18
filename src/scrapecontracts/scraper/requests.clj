(ns scrapecontracts.scraper.requests
  (:require [org.httpkit.client :as http]
            [clojure.core.async :refer [go go-loop chan >! <!]]))

(def inchan (chan))

(defn- get [inchan address]
  (http/get address #(go (>! inchan %))))

(defn- chan->atom [inchan outatom]
  (go-loop []
    (swap! outatom conj (<! inchan))
    (recur)))
;; this is just a stub for looking at results, will be replaced with actual processor code.  Listen to channel and dump everything in it into an atom.

;; atom is meant to be an empty vector

(defn fetch-pages! [addresses outatom]
  (do
    (chan->atom inchan outatom)
    (dorun
     (map (partial get inchan) addresses))))
