#! /usr/bin/racket
#lang racket
; This file is used to generate the mapping for elasticsearch
; It is written in Racket (a dialect of Scheme)
; It will not be necessary to run unless you want to change the elasticsearch mapping
; This may be necessary if you have fields you want to add, or need some other customization
; You may also edit the JSON mapping directly, or use whatever tool you want to edit the mapping with

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
