#lang racket

(require json)

(define (root name type)
  `(,name type))

(define ((prop
          type
          [index "analyzed"])
          name)
  (define prop-hash (make-hash))
  (hash-set! prop-hash (string->symbol name)
               `#hash(
                      (type . ,type)
                      (index . ,index)))
    prop-hash)

(define ((dict name) ps)
  (let ([prop-vals (make-hash)]
        [props-hsh (make-hash)])
    (for ([p ps])
      (hash-set! prop-vals
                 (car p)
                 (cdr p)))
    (hash-set! props-hsh name prop-vals)
    props-hsh))

(define (props ps)
  (define props-hash (make-hash))
  (for ([p ps])
    (match p
      [(hash-table (k v))
       (hash-set! props-hash k v)]))
  `#hash((properties . ,props-hash)))

(define str (prop "string"))

(define num (prop "integer"))

(define date (prop "date"))

(define bool (prop "boolean" "not_analyzed"))

(define (dictprop name d)
  (define dict (make-hash))
  (hash-set! dict name d)
  dict)

(define (estruct name pairs)
  (define estr (make-hash))
  (hash-set! estr
             (string->symbol name)
         (props pairs))
  estr)

(define (make-mapping
         type
         decl)
  (define mapping (make-hash))
  (hash-set! mapping
             (string->symbol type)
             (props decl))
  (jsexpr->string mapping))

(provide
 (all-defined-out))
