(ns scrapecontracts.scraper.core
  (:require [clojure.core.async :refer [>!! <!! chan buffer close! thread timeout]]
            [scrapecontracts.scraper.fetch :refer [fetch]]))


(defn scrape [site-vec processor-func opts-map]
  (println "not implemented"))

