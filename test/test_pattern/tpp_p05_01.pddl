(define (problem TPP)
(:domain TPP-Propositional)
(:objects
	goods1 goods2 goods3 goods4 goods5 - goods
	truck1 truck2 truck3 - truck
	market1 market2 - market
	depot1 - depot
	level0 level1 - level)

(:init
	(next level1 level0)
	(ready-to-load goods1 market1 level0)
	(ready-to-load goods1 market2 level0)
	(ready-to-load goods2 market1 level0)
	(ready-to-load goods2 market2 level0)
	(ready-to-load goods3 market1 level0)
	(ready-to-load goods3 market2 level0)
	(ready-to-load goods4 market1 level0)
	(ready-to-load goods4 market2 level0)
	(ready-to-load goods5 market1 level0)
	(ready-to-load goods5 market2 level0)
	(stored goods1 level0)
	(stored goods2 level0)
	(stored goods3 level0)
	(stored goods4 level0)
	(stored goods5 level0)
	(loaded goods1 truck1 level0)
	(loaded goods1 truck2 level0)
	(loaded goods2 truck1 level0)
	(loaded goods2 truck2 level0)
	(loaded goods3 truck1 level0)
	(loaded goods3 truck2 level0)
	(loaded goods4 truck1 level0)
	(loaded goods4 truck2 level0)
	(loaded goods5 truck1 level0)
	(loaded goods5 truck2 level0)
	(connected market1 market2)
	(connected market2 market1)
	(connected depot1 market2)
	(connected market2 depot1)
	(on-sale goods1 market1 level1)
	(on-sale goods2 market1 level1)
	(on-sale goods3 market1 level1)
	(on-sale goods4 market1 level1)
	(on-sale goods5 market1 level1)
	(on-sale goods1 market2 level0)
	(on-sale goods2 market2 level0)
	(on-sale goods3 market2 level0)
	(on-sale goods4 market2 level0)
	(on-sale goods5 market2 level0)
	(at truck1 depot1)
	(at truck2 depot1)
	(at truck3 depot1))



 (:goal (and ))

(:constraints (and

(forall (?t - truck) (pattern (drive ?t depot1 market2) (drive ?t market2 market1)))

))

)