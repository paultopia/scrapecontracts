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


(defn make-http-channel [addresses]
  (let [inchan (chan 1 parse-transducer)]
    (dorun
     (map (partial get inchan) addresses))
    inchan))

(defn watch-http-channel [http-channel, callback]
  (go-loop []
    (callback (<! http-channel))
    (recur)))

;; example:
;; (def hchan (make-http-channel ["http://paul-gowder.com" "http://rulelaw.net"]))
;; (def outatom (atom []))
;; (watch-http-channel hchan #(swap! outatom conj %))
;; (count @outatom) => 2

(defn fetch [addresses callback]
  (let [inchan (make-http-channel addresses)]
    (watch-http-channel inchan callback)))

;; example:
;; (def outatom (atom []))
;; (fetch ["http://paul-gowder.com" "http://rulelaw.net"] #(swap! outatom conj %))
