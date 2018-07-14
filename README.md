# Markov-Decision-Proccess
BackPropagation Model to solve Traffic problem

Markov decision processes (MDPs) provide a mathematical framework for modeling decision making in situations where outcomes are partly 
random and partly under the control of a decision maker. MDPs are useful for studying a wide range of optimization problems solved via 
dynamic programming and reinforcement learning. MDPs were known at least as early as the 1950s (cf. Bellman 1957); a core body of research 
on Markov decision processes resulted from Ronald A. Howard's book published in 1960, Dynamic Programming and Markov Processes.[1] 
They are used in a wide area of disciplines, including robotics, automatic control, economics, and manufacturing.

Fuzzy Logic: Semaphore Project
Diego Ortega
Suriel Garcia
Linguistic Variables:
Traffic(t) = {LigthTraffic, MediumTraffic, HeavyTraffic}

LigthTracffic = {0:160}
MediumTraffic = {161:480}
HeavyTraffic = {481: 800}

MemberShip Function 

x Axis corresponds to time (t), y Axis corresponds to degree of membership (𝜇)

𝜇lighttraffic: 𝑋 → [0,1]
𝜇Mediumtraffic: 𝑋 → [0,1]
𝜇Heavytraffic: 𝑋 → [0,1]

This mapping is called degree of membership, and quantifies the degree of membership of the element in X to a given fuzzy set. In this case scenario X is the amount of cars over a given lane on a certain moment. As the value 𝜇n decreases or increases, so does the degree of membership of X to a certain fuzzy set.



Knowledge Base of Rules
LightTraffic(cars)= {1  if 0<=cars < 161, 0 if cars>=161}
MediumTraffic(cars) = {0 if 161<cars>=481, 1 if 161<=cars<481}
HeavyTraffic(cars) = {0 if 481<cars, 1 if 481<=cars<=800}
