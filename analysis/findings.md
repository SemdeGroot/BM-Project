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
