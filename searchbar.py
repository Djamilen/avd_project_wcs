import streamlit as st
import pandas as pd

# Liste des prénoms
prenoms = ["Michel", "Morgane", "David", "Alexandre"]

# Convertir la liste en JS array
prenoms_js = str(prenoms).replace("'", '"')

# Injecter HTML + JS pour champ avec autocomplétion native
st.markdown(f"""
<input list="prenoms" id="prenom_input" name="prenom_input" placeholder="Tapez un prénom..." style="width: 100%; padding: 0.5em; font-size: 1em;" />
<datalist id="prenoms">
  {''.join([f'<option value="{p}">' for p in prenoms])}
</datalist>

<script>
  const input = window.parent.document.getElementById("prenom_input");
  input.addEventListener("change", function() {{
    window.parent.postMessage({{type: "streamlit:setComponentValue", value: input.value}}, "*");
  }});
</script>
""", unsafe_allow_html=True)