
# Zombie Apocalypse Population Dynamics



## Factors to consider in model

- infection rate
- infection radius*
- incubation period
- kill rate
- kill radius*
- agent velocity
----
<small>*denotes geometric attribute</small>



## Equations for model
----
### $ \dot{H} = -HZ(\alpha) ~ ~ ~ ~ ~$
### $ \dot{Z} = HZ(\alpha - \beta)$



## Fixed point
----
### $(0,0)$
### x and y axis


## Linear approximation
----
### $ -Z\alpha ~ ~ ~ -H\alpha $
### $ -H(\alpha-\beta) ~ ~ ~ -Z(\alpha-\beta) $



## Geometric interpretation

- When humans are faster than zombies, they shoot and run and the zombies die.
- When zombies are faster than humans, things get interesting.



## Spatial simulation

- 2 dimensional
- wrapped simulation field
- agents distributed uniformly across field


### Agent Movement

$\begin{equation}
\vec{M_a} = \sum_{z \in Z}(\vec{r_z} - \vec{r_a})\exp(-\frac{||\vec{r_z} - \vec{r_a}||^2}{\sigma_H})
\label{human-agent-moment}
\end{equation}$



## A small term for velocity effects
----
$1 - \frac{V_H}{V_Z}$


## Plots


## $V_Z = 4.0$
<img src="imgages/pop_dec_5_4.0.png">


## $V_Z = 4.5$
<img src="imgages/pop_dec_5_4.5.png">


## $V_Z = 4.75$
<img src="imgages/pop_dec_5_4.75.png">


## $V_Z = 4.9$
<img src="imgages/pop_dec_5_4.9.png">


## $V_Z = 5.0$
<img src="imgages/pop_dec_5_5.0.png">


## $V_Z = 5.1$
<img src="imgages/pop_dec_5_5.1.png">


## $V_Z = 5.25$
<img src="imgages/pop_dec_5_5.25.png">


## $V_Z = 5.5$
<img src="imgages/pop_dec_5_5.5.png">


