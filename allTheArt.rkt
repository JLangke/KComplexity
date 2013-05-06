#lang racket

(require (planet dfriedman/miniKanren:1:1/minikanren))

(define succeed (== #t #t)) ; thanks Danny Yoo!
(define fail (== #t #f))

; != is the opposite of ==, very convenient to have
(define != 
  (λ (x y)
    (conda ; conda requires that exactly one goal succeed
     ((== x y) fail)
     (succeed))))


; Peano arithmetic adapted from "From Variadic Functions to Variadic Relations"
; http://scheme2006.cs.uchicago.edu/12-byrd.pdf
; Convert a normal integer into Peano's encoding
(define peano
  (λ (x)
    (cond
      ((= x 0) 'z)
      (else (list 's (peano (- x 1)))))))

; convenience definitions
(define zeroo (peano 0))
(define oneo (peano 1))

; defines what it means for two numbers to add up to a third
(define pluso
  (λ (n m sum)
    (conde
     ((== 'z n) (== m sum))
     ((fresh (x y)
             (== (list 's x) n)
             (== (list 's y) sum)
             (pluso x m y))))))

; Now we define what it means to be a well-typed simple program
; (no lambdas or function definitions (yet!))
(define programo
  (λ (p totype size)
    (conde
     ((== totype 'int)
      (conde 
       ((== p 0) (== size oneo))
       ((== p 1) (== size oneo))
       ((== p 'x) (== size oneo))
       ((== p 'y) (== size oneo))
       ((fresh (x y xs ys smallsize)
               (pluso oneo smallsize size)
               (pluso xs ys smallsize)
               (programo x 'int xs)
               (programo y 'int ys)
               (!= x 0) ; math with 0 is boring
               (!= y 0) ; math with 0 is boring
               (conde
                ((== p (list '+ x y)))
                ((== p (list '* x y)) 
                 (!= x 1) ; * programs should not multiply by 1
                 (!= y 1)))))))
     ((== totype 'bool)
      (conde
       ((== p #t) (== size oneo))
       ((== p #f) (== size oneo))
       ((fresh (x y xs ys smallsize)
               (pluso oneo smallsize size)
               (pluso xs ys smallsize)
               (programo x 'int xs)
               (programo y 'int ys)
               (!= x y) ; < programs should not compare the same thing, that's dumb
               (conde
                ((contains-variable x))
                ((contains-variable y))) ; one of the two sides should be non-const
               (== p (list '< x y))))
       ((fresh (x y xs ys smallsize)
               (pluso oneo smallsize size)
               (pluso xs ys smallsize)
               (programo x 'bool xs)
               (programo y 'bool ys)
               (!= x y) ; you shouldn't (and) or (or) the same things together
               (contains-variable x) ; make sure x isn't constant
               (contains-variable y) ; make sure y isn't constant
               (conde 
                ((== p (list 'and x y)))
                ((== p (list 'or x y))))))
       ((fresh (x xs f r)
               (pluso xs oneo size)
               (programo x 'bool xs)
               (== x (cons f r))
               (!= f 'not) ; eliminate (not (not ...)) because that's lame
               (contains-variable x) ; otherwise, it's always #t or #f
               (== p (list 'not x)))))))))


; A predicate to ensure that a program actually varies with either x or y
(define contains-variable
  (λ (p)
    (conda
     ((== p 'x))
     ((== p 'y))
     ((fresh (x y)
             (== p (cons x y))
             (conda
              ((contains-variable x))
              ((contains-variable y))))))))

; Sorts the list and removes any duplicates
(define uniq-programs
  (λ (l)
    (define uniq-helper
      (λ (prev l)
        (cond 
          ((null? l) (list prev))
          ((equal? prev (car l)) (uniq-helper prev (cdr l)))
          (else (cons prev (uniq-helper (car l) (cdr l)))))))
    (define sorted-list (sort l string<? #:key ~s #:cache-keys? #t))
    (cond 
      ((pair? l) (uniq-helper (car sorted-list) (cdr sorted-list)))
      (else l))))


(require 2htdp/image) ; this is the library for producing images
(define b0  (square 25 "solid" "gray")) ; defines a binary output of zero.
(define b1  (square 25 "solid" "black"))    ; defines a binary output of one.


; THIS IS WHERE WE DECIDE HOW BIG THE 2-D PATTERNS ARE
(define width 3)
(define height 3)


; Finds the bit-pattern for a given function on the specified grid
(define tf-fn-to-number
  (λ (f)
    (define g
      (λ (x y)
        (cond 
          ((f x y) 1)
          (else 0))))

    (define build-number
      (λ (x y c)
        (cond 
          ((and (< x width) (< y height)) (+ (arithmetic-shift (g x y) c) 
                                             (build-number (+ 1 x) y (+ 1 c))))
          ((< y height) (build-number 0 (+ 1 y) c))
          (else 0))))

    (build-number 0 0 0)))


; Takes in an integer and produces an image of its corresponding pattern
(define int-to-image
  (λ (i)
    (define image-for-bit
      (λ (bit)
        (cond 
          ((bitwise-bit-set? i bit) b1)
          (else b0))))
    (define build-row
      (λ (x y)
        (cond 
          ((< x width) (cons (image-for-bit (+ x (* y width))) (build-row (+ x 1) y)))
          (else '()))))
    (define build-rows
      (λ (y)
        (cond 
          ((< y height) (cons (apply beside (build-row 0 y)) (build-rows (+ y 1))))
          (else '()))))
    (apply above (build-rows 0))))


; Given a number, return the bit patterns of all programs of that size
(define number-to-patterns 
  (λ (n)
    ; Generate every valid program of size n
    (define programs (uniq-programs (run #f (x) (fresh (p)
                                                       (programo p 'bool (peano n))
                                                       (== x (list 'λ '(x y) p))))))
    ; build a namespace in which to call eval
    (define ns (make-base-namespace))
    (define program-to-procedure (λ (p) (eval p ns))) 
    
    ; convert the programs into running code
    (define procedures (map program-to-procedure programs)) 
    
    ; discover the bit pattern each program outputs
    (define numbers (map tf-fn-to-number procedures))
    
    ; collect them all together in a big list, uniquify the list
    (hash->list (make-hash (map list numbers programs))))) 


; Builds up a list of patterns of all the programs from size 1 up through the passed-in number
(define build-dict-up-to
  (λ (n) 
    (define build-list-up-to
      (λ (n)
        (cond
          ((<= n 0) '())
          (else  
           (let ([small-list (build-list-up-to (- n 1))]
                 [patterns (number-to-patterns n)])
             (append (map (λ (x) (list x n)) patterns) small-list))))))
    
    (define patterns-and-progs-to-ints (build-list-up-to n))
    
    (define take-the-pattern-and-int 
      (λ (ppi) 
        (define pattern-and-prog (car ppi))
        (define complexity (car (cdr ppi)))
        (define pattern (car pattern-and-prog))
        (define prog (car (cdr pattern-and-prog)))
        (list pattern (list prog complexity))))
    
    (define patterns-to-progs-and-ints (map take-the-pattern-and-int patterns-and-progs-to-ints))
    (define smallest-program-hash (make-hash patterns-to-progs-and-ints))
    (hash-map smallest-program-hash (λ (k v) (list (int-to-image k) k v)))))


; patterns will be a list containing all the length*width patterns up to the given size
(define patterns
  (build-dict-up-to 3))

; Display it, and display how many
patterns
(length patterns)