
(begin
(define (map FUNCTION LIST)
  (if (equal? (length LIST) 0)
      (list)
      (cons (FUNCTION (car LIST)) (map FUNCTION (cdr LIST)))))

(define (filter FUNCTION LIST)
  (if (equal? (length LIST) 0)
      (list)
      (if (FUNCTION (car LIST))
          (cons (car LIST) (filter FUNCTION (cdr LIST)))
          (filter FUNCTION (cdr LIST)))))

(define (reduce FUNCTION LIST INITVAL)
  (if (equal? (length LIST) 0)
      INITVAL
      (reduce FUNCTION (cdr LIST) (FUNCTION INITVAL (car LIST)))))
)
