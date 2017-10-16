(ns scrapecontracts.scraper.fetch
  (:require [net.cgrand.enlive-html :as html]))

(defn- get-page-at-address [address]
  (html/html-resource (java.net.URL. address)))

(defn- make-link-map [source-address link-node]
  (let [address (:href (:attrs link-node))
        linktext (first (:content link-node))]
    {:address address :linktext linktext :source-url source-address}))

(defn- extract-links [webpage]
  (html/select webpage [:a]))

(defn fetch [address]
  (let [webpage (get-page-at-address address)
        links (mapv (partial make-link-map address) (extract-links webpage))]
    {:webpage webpage :links links}))

;; problem: this doesn't handle relative urls or anchors properly at all.  anchors should be stripped, relative urls should be made absolute.
