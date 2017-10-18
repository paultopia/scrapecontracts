(defproject scrapecontracts "0.1.0-SNAPSHOT"
  :description "core.async/enlive based scraper for my own research"
  :url "https://github.com/paultopia/scrapecontracts"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.9.0-alpha16"]
                 [com.cemerick/url "0.1.1"]
                 [enlive "1.1.6"]
                 [org.jsoup/jsoup "1.10.3"]
                 [org.clojure/core.async "0.3.443"]]
  :main ^:skip-aot scrapecontracts.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
