(ns scrapecontracts.scraper.fetch
  (:require [net.cgrand.enlive-html :as html]
            [cemerick.url :refer [url]]))

(defn- get-page-at-address [address]
  (html/html-resource (java.net.URL. address)))

(defn- make-full-url
  "if href is properly formed url, return url object.  if not, treat it as relative pathname and combine with source url, return that url object."
  [source-address href]
  (try (url href)
       (catch java.net.MalformedURLException e
         (url source-address href))))

(defn- parse-href [source-address href]
  (let [href-url (make-full-url source-address href)
        source-url (url source-address)
        source-host (:host source-url)
        href-host (:host href-url)]
    {:address (str href-url) :new-domain? (not= source-host href-host)}))

(defn- make-link-map [source-address link-node]
  (let [href (:href (:attrs link-node))
        {:keys [address new-domain?]} (parse-href source-address href)
        linktext (first (:content link-node))]
    {:address address :linktext linktext :source-url source-address :new-domain? new-domain?}))

(defn- extract-links [webpage]
  (html/select webpage [:a]))

(defn fetch [address]
  (let [webpage (get-page-at-address address)
        links (mapv (partial make-link-map address) (extract-links webpage))]
    {:webpage webpage :links links}))

