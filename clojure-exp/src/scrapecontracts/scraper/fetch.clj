(ns scrapecontracts.scraper.fetch
  (:require [net.cgrand.enlive-html :as html]
            [clojure.string :refer [trim replace]]
            [cemerick.url :refer [url]]))

(defn- get-page-at-address [address]
  (html/html-resource (java.net.URL. address)))

(defn- space-out-punctuation [text] (replace text #"([.?!\",:;“”\)\(\[\]\{\}])" "$1 "))

(defn- space-out-caps-diff [text] (replace text #"([a-z])([A-Z])" "$1 $2"))

(defn- space-out-letter-digit [text] (replace text #"(\d)([a-zA-Z])" "$1 $2"))

(defn- spacing-heuristic
  "raw text extraction does a bad job with documents where there's no space between, e.g., paragraphs, table rows, etc.  Non-lazy approach would, I suppose, be to recursively walk the entire tree and concatenate all the text nodes with spaces.  But that would be a lot of work.  For now, here's a lazy heuristic that just replaces sentence/clause termination punctuation with punctuation + space to capture most of the problems.  Also assume capitalized character following lowercase character are at start of word, and letter following digit ditto."
  [text]
  (-> text
      space-out-punctuation
      space-out-caps-diff
      space-out-letter-digit))

(defn- de-whitespace [text]
  (trim (replace text #"\s+" " ")))

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

(defn extract-text [webpage]
  (-> webpage
      (html/select [:body])
      (html/transform [:img] nil)
      (html/transform [:script] nil)
      (html/transform [:style] nil)
      html/texts
      first
      spacing-heuristic
      de-whitespace))

(defn fetch [address]
  (let [webpage (get-page-at-address address)
        links (mapv (partial make-link-map address) (extract-links webpage))
        text (extract-text webpage)]
    {:webpage webpage :links links :text text}))

