(ns scrapecontracts.scraper.core
  (:require [clojure.core.async :refer [>!! <!! chan buffer close! thread timeout]]
            [net.cgrand.enlive-html :as html]))

(defn scrape [site-vec processor-func opts-map]
  (println "not implemented"))

