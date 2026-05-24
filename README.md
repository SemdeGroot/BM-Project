# BioModeling Snoopy Project

This project extends the Gilin et al. continuous Petri net for the HIF-ILK hypoxia response.

We split the Snoopy models into steps so we can go back to an earlier version if needed:

```text
snoopy-models/base.cpn
snoopy-models/base_with_T315.cpn
snoopy-models/chou_extended.cpn
snoopy-models/hsu_chou_extended.cpn
snoopy-models/main.cpn
```

The steps are:

```text
base.cpn: original rebuilt HIF-ILK model.
base_with_T315.cpn: added ILK_activity and T315 inhibition.
chou_extended.cpn: adds the Chou genes and EMT markers.
hsu_chou_extended.cpn: adds the IL-6 and NF-kappaB pathway.
main.cpn: final model, same as the most complete current version.
```

Each step builds on the previous model. The T315 version models T315 as reduced ILK activity, not as ILK protein degradation and not as direct Akt inhibition.

Current note: `base_with_T315.cpn` and `main.cpn` contain the current working T315 model. The other split model files still need to be filled from Snoopy before they can be used for exports.

For result analysis, make a local Python environment first:

```text
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate it with:

```text
venv\Scripts\activate
```
