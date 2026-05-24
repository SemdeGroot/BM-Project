# Findings

For the base model we simulated O2 values from 0.1 to 0.9, like in the original paper.
Our rebuilt model does not give exactly the same numerical values as the paper.
For example, HIF at high oxygen does not drop as close to zero as in the original results.

Still, the qualitative behavior is correct.
Low O2 gives higher HIF, ILK, p-473S-Akt and p-mTOR than high O2.
So we can use the rebuilt model as a qualitative base model, but not as an exact numerical copy of the original study. Maybe we can improve this? I do not know how, maybe discuss during midterm discussion.

The base plots show that HIF and the ILK pathway go down when O2 increases.
The T315 plots show that higher T315 lowers ILK activity, p-473S-Akt and p-mTOR.
The ILK protein stays almost the same with T315, which fits our idea that T315 blocks ILK activity instead of removing ILK protein.

For the Chou module we added p-GSK3beta, YB-1, Foxo3a, Snail, Zeb1, E-cadherin and vimentin as downstream outputs of ILK activity.
The new rates are starting assumptions because Chou et al. mainly gives qualitative Western blot and RT-PCR trends, not Petri net rate constants.
We kept the ILK-dependent rates close to the existing FL1 scale and used slower basal production for Foxo3a and E-cadherin so they can recover when T315 lowers ILK activity.
After tuning the downstream EMT rates, T315 partly restores E-cadherin under hypoxia but not back to the normoxia value.
This makes sense because O2 is still low in these simulations, so HIF can still drive Snail even when ILK activity is lowered.

For the Hsu module we added the simplified IL6 -> p-Stat3 -> E2F1 -> ILK and p-Akt -> NF-kappaB -> IL6 feedback loop.
The Hsu rates are assumptions, with NF-kappaB -> IL6 kept weak and IL6 degradation increased to avoid an overly strong feedback loop.
T315 was changed to a Michaelis-Menten inhibition term using the 0.6 uM IC50 value.
In the final simulations, T315 gives a dose-dependent decrease of the Hsu loop and 0.6 uM leaves about 57% activity, close to the intended IC50 behavior.
Low and high initial IL6 still converge at long time, which we treat as a limitation of the simplified MassAction feedback model.
