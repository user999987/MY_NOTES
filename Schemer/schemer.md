### 1. car of l = (car l)

1. (a b c)-> a
2. ((a b c) x y z)-> (a b c)
```
first atom or list or S-expression of the non-empty list
```
### 2. cdr of l = (cdr l)
1. (a b c)-> (b c)
2. ((a b c) x y z)
3. (hamburger)-> ()
```
the list l without (car l)
```
### 3. cons
1. (cons s l) where s is a and l is (penut butter) -> (a penut butter)
2. (cons s l) where s is (apple and) and l is (penut butter) -> ((apple and) penut butter)
```
cons takes two arguments: the first one is any S-expression and the second one is any list
```
### 4. null?
1. (null? (quote())) -> True # (quote()) = () = '() is the notation of the null list
2. (null? l) where l is (a b c) -> False 
3. (null? a) where a is spaghttti -> No answer
```
While in practice, (null? α) is false for everything, except the empty list
```

### 5. atom?
1. (atom? s) where s is Harry -> True # (atom? s) is just another way to ask  "Is s an atom?". Atom is a string of characters
```
atom? takes one argument, the argument can be any S-expression.
```
### 6. eq?
1. (eq? a1 a2) where a1 is Harry and a2 is Harry -> True
```
eq? takes two arguments, each must be a non-numeric atom.<br />
While in practice lists and some numbers may be arguments of eq?
```
### 7. lat?
lat? is a function defined in the book

```schemer
(define lat?
  (lambda (l)
    (cond
      ((null? l) #t)
      ((atom? (car l)) (lat? (cdr l)))
      (else #f)
    )
  )
)
```

1. (lat? l) where l is (Jack Sprat could eat no chicken fat) -> True
2. (lat? l) where l is ((Jack) Sprat could eat no chicken fat) -> False

### 8. or
1. (or (null? l1) (null? l2)) where l1 is (a b c) and l2 is () -> True
```
(or ...) asks two questions, one at a time. If the first one is true it stops and aanswers true. Otherwise it asks the second questions and answers with whatever the second questions answers.
```

### 9. member?
```schemer
(define member?
  (lambda (a lat)
    (cond 
      ((null? lat) #f)
      (else(or (eq? (car lat) a)
        (member? a (cdr lat)
        ))))))
```

### 10. rember
1. (rember a lat) where a is mint and lat is (lamb chops and mint jelly) -> (lamb chops and jelly) # "Rember" stands for remove a member
2. (rember a lat) where a is toast and lat is (bacon lettuce and tomato) -> (bacon lettuce and tomato)
3. (rember a lat) where a is cup and lat is (coffee cup tea cup and hick cup) -> (coffee tea cup and hick cup)

```
It takes an atom and a lat as its arguments, and makes a new lat with the first occurrence of the atom in the old lat removed.
(define rember 
  (lambda (a lat)
    (cond
      ((null? lat) (quote())
      ((eq? (car lat) a) (cdr lat))
      (else (cons (car lat)
          (rember a (cdr lat))))))))
```

### 11. firsts
1. (firsts l) where l is ((apple peach pumkin) (plum pear cherry) (grape raisin pea) (bean carrot eggplant)) -> (apple plum grape bean)
2. (firsts l) where l is () -> ()
3. (firsts l) where l is (((five plums) four) (eleven green oranges) ((no) more))-> ((five plums) eleven (no)) 
4. (firsts l) where l is ((a b) (c d) (e f)) -> (a c e)

```
(define firsts
  (lambda (l)
    (cond
      ((numm? l) ...)
      (else (cons (car (car l ))
              (firsts (cdr l)
              ))))))

I. either
  1. cons e onto ()
  2. cons c onto the value of 1
  3. cons a onto the value of 2
II. or 
  1. cons a onto the value of 2
  2. cons c onto the value of 3
  3. cons e onto ()
III. or 
  cons a onto
    the cons of c onto
      the cons of e onto
        ()

明显第三种情况是我们需要的 
(define firsts
  (lambda (l)
    (cond
      ((numm? l) (quote()))
      (else (cons (car (car l ))
              (firsts (cdr l)
              ))))))
```

### 12. insertR
1. (insertT new old lat) where new is topping old is fudge and lat is (ice cream with fudge for dessert) -> (ice cream with fudge topping for dessert)
```
(define insertR
  (lambda (new old lat)
    (cond ...)))
1. which argument changes when we recur with insertR? A: lat, because we can only look at one of its atoms at a time
2. how many questions can we ask about the lat? A: Two. A lat is either the null list or a non-empty list of atoms.
3. which questions do we ask about the first element? A: First, we ask (eq?(car lat) old). Then we ask else, because there are no other interesting cases.

(define inserlR
  (lambda (new old lat)
    (cond
      ((null? lat) (quote ()))
      (else
        (cond
          ((eq? ( car lat) old) ( cdr lat))
          (else ( cons ( car lat)
                  ( inserlR new old
                    ( cdr lat))))))))) 


(define inserlR
  (lambda (new old lat)
    (cond
      ((null? lat) (quote ()))
      (else
        (cond
          ((eq? ( car lat) old) 
            (cons old
              (cons new (cdr lat))))
          (else ( cons ( car lat)
                  ( inserlR new old
                    ( cdr lat))))))))) 

( ( eq? ( car lat) old)
( cons new ( cons old ( cdr lat)))) 
----------->
( ( eq? ( car lat) old)
( cons new lat)) 
```