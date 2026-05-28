# Findings

For the base model we simulated O2 values from 0.1 to 0.9, like in the original paper.
Our rebuilt model does not give exactly the same numerical values as the paper.
For example, HIF at high oxygen does not drop as close to zero as in the original results.

Still, the qualitative behavior is correct.
Low O2 gives higher HIF, ILK, p-473S-Akt and p-mTOR than high O2.
So we can use the rebuilt model as a qualitative base model, but not as an exact numerical copy of the original study.

For the Chou module we added p-GSK3beta, YB-1, Foxo3a, Snail, Zeb1, E-cadherin and vimentin as downstream outputs of ILK activity.
The new rates are starting assumptions because Chou et al. mainly gives qualitative Western blot and RT-PCR trends, not Petri net rate constants.
We kept the ILK-dependent rates close to the existing FL1 scale and used slower basal production for Foxo3a and E-cadherin so they can recover when T315 lowers ILK activity.
After tuning the downstream EMT rates, T315 partly restores E-cadherin under hypoxia but not back to the normoxia value.
This makes sense because O2 is still low in these simulations, so HIF can still drive Snail even when ILK activity is lowered.

For the Hsu module we added the simplified IL6 -> p-Stat3 -> E2F1 -> ILK and p-Akt -> NF-kappaB -> IL6 feedback loop.
The Hsu rates are assumptions, with NF-kappaB -> IL6 kept weak and IL6 degradation increased to avoid an overly strong feedback loop.
T315 uses a Michaelis-Menten inhibition term anchored on the 0.6 uM IC50 value from Lee et al.

## Final model (main.cpn)

For the final model we combined the base HIF module, the T315 activity layer, the Chou EMT module and the Hsu IL6 loop into one Snoopy net.
We then re-ran all simulation groups from the model plan and exported them to `snoopy-output/main/`.
The plotting scripts produced eight figures in `analysis/results/output/main/`.

Four parameters were calibrated against a literature target:

- `FL3` was lowered from 0.4181 to 0.15 so HIF does not stay flat across all O2 levels.
- `k14` and `k17` were raised from 0.0226 to 0.03 so the HIF drop falls inside the O2 0.6 to 0.7 window from Chou et al.
- `E2F1_induces_ILK` was raised from 0.1 to 1.0 so a sustained IL6 stimulus visibly raises ILK, as in Hsu Fig. 1B.
- `T315 Vmax` was set to 0.27 so ILK activity is roughly halved at T315 = 0.6, matching the Lee et al. IC50.

Oxygen switch (`main_oxygen_switch.png`): HIF decreases gradually from O2 0.1 to 0.6 and then drops sharply between O2 0.6 and 0.7. ILK activity follows the same switch. This matches the qualitative switch behavior of the original paper.

T315 dose-response (`main_t315_signaling.png`): ILK activity, p-Akt, p-mTOR and p-GSK3beta all collapse onto one curve under hypoxia and drop to about 0.49 of the T315 = 0 value at T315 = 0.6. This is close to the intended 50% IC50 anchor.

EMT response (`main_t315_emt.png`, `main_oxygen_emt.png`): higher T315 partly restores Foxo3a and E-cadherin and partly lowers Snail, Zeb1 and vimentin. The shift is partial because HIF still drives Snail directly. The oxygen scan shows the same trend in reverse: hypoxia pushes the markers toward the mesenchymal state.

IL6 stimulation (`main_il6_stimulation.png`): higher IL6 raises p-Stat3 and E2F1 strongly. ILK activity, p-Akt and NF-kB are already near their plateau at IL6 = 1.0 because the loop is driven by both IL6 and hypoxia, so they only rise a little when IL6 increases further.

T315 inside the IL6 loop (`main_t315_il6_loop.png`): T315 lowers ILK activity, p-Akt, NF-kB and downstream IL6 across the dose range, confirming that T315 also dampens the inflammatory loop, not only the HIF-ILK loop.

Heatmap (`main_t315_heatmap.png`): summarises the dose-response of all main places relative to T315 = 0. ILK pathway and EMT markers respond clearly, while base HIF places like S3_HIF stay almost unchanged, which fits the activity-inhibition interpretation.

Time course (`main_time_course.png`): the four conditions (normoxia, hypoxia, hypoxia + low T315, hypoxia + high T315) reach steady state within the 10000-unit window and show the expected ordering, so the steady-state plots are not a transient artefact.
