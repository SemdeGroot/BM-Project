This project extends the Gilin et al. continuous Petri net for the HIF-ILK hypoxia response.
The current `main.cpn` contains the base HIF model plus the ILK feedback route `ILK_protein -> ILK_activity -> p_473S_Akt -> p_mTOR -> HIF`.
We added `ILK_activity` to separate ILK protein abundance from active ILK signaling.
T315 is included as an inhibitor input that reduces `ILK_activity`, not ILK protein and not Akt directly.
The T315 transition is modeled with ordinary arcs and a reverse arc, following the style used in the original model.
No inhibitor arcs are currently used in `main.cpn`.
The starting rates for the new layer are `ILK_activation = 0.4181`, `ILK_activity_deg = 0.2000` and `T315_inhibits_ILK_activity = 0.6000`.
Next steps are to simulate the base model, test T315 doses, add the Chou module with YB-1, Foxo3a and EMT markers and then add the Hsu IL-6/NF-kappaB feedback module.

Please update this README when you update the model.