#! /usr/bin/racket
#lang racket
(require "schemadsl.rkt")

(displayln
  (make-mapping
    "course"
    `(,(estruct "sections"
      `(,(str "title")
      ,(str "time")
      ,(str "loc")
      ,(str "prof")
      ,(str "sem")
      ,(str "day")))

      ,(estruct "textbooks"
        `(,(str "title")
          ,(str "author")
          ,(str "price"))))))
