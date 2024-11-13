person(gren).
person(susan).

son(greg, david).
son(pauline)
son(david, jack).
son(chris,greg).

daughter(kim, david).
daughter(steph, david).

female(pauline).

grandson(jack)
granddaughter(jay)

child(X,Y) :- son(X,Y).
child(X,Y) :- daughter(X,Y).

grandchild(X,Y) :- child(X,Z), child(Z,Y)

grandson(X,Y) :- son(X,Z), child(Z,Y)

male(X) :- son(X,_).
female(X) :- daughter(X,_).

granddaughter(X,Y) :- grandchild(X,Y), female(X).

grandmother(X,Y) :- grandchild(Y,X), female(X)


lower(list, V, Lower) :-
    findall(Elem, (member(Elem,List), Element < V), Lower).
    
upper(list, V, Upper) :-
    findall(Elem, (member(Elem,List), Element > V), Upper).

equal(list, V, Upper) :-
    findall(Elem, (member(Elem,List), Element = V), Upper).

qsort([],[]).

qsort([V|Rest], Sorted) :-
    lower(Rest,V, Lower),
    equal([V|Rest],V,Equal),
    upper(Rest,V,Upper),
    qsort(Lower,SortedLower),
    qsort(Upper,SortedUpper),
    append(SortedLower, Equal, SortedLowerEqual),
    append(SortedLowerEqual,SortedUpper, Sorted)
