(ns scrapecontracts.scraper.soup
  (:import [org.jsoup Jsoup]))

(defn- get-page-at-address [address]
  (let [conn (Jsoup/connect address)]
    (.get conn)))
;; put error handling or ignoring in here.

(defn- extract-link-data [link]
  (let [linktext (.text link)
        address (.attr link "abs:href")]
    {:linktext linktext :address address}))

(defn- extract-links [soup]
  (let [links (.select soup "a")]
    (mapv extract-link-data links)))

(defn extract-all- [soup]
  (let [links (extract-links soup)
        text (.text soup)]
    {:soup soup :links links :text text}))

(defn fetch [address]
  (extract-all (get-page-at-address address)))

(defn parse [htmlstring]
  (extract-all (Jsoup/parse htmlstring)))
