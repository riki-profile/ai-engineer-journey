"""Pembungkus model sentimen (modul 12) sebagai model MLflow `pyfunc` (modul 13).

MLflow 3 menyarankan *models from code*: kelas model didefinisikan di file .py ini,
lalu `mlflow.pyfunc.log_model(python_model="pyfunc_sentimen.py", ...)` menyimpan
file ini beserta artefaknya. Dengan begitu model bisa dimuat di mana saja lewat
`mlflow.pyfunc.load_model("models:/<nama>@<alias>")` tanpa kode notebook.
"""

import mlflow
import pandas as pd


class ModelSentimen(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # `model.py` (dari modul 12) ikut disimpan lewat code_paths, sehingga bisa diimpor di sini
        from model import Prediktor

        self.prediktor = Prediktor(context.artifacts["artefak"])

    # Petunjuk tipe (type hint) dipakai MLflow untuk menyusun signature input/output model
    def predict(self, context, model_input: pd.DataFrame, params: dict | None = None) -> pd.DataFrame:
        teks = model_input["teks"].astype(str).tolist()
        return pd.DataFrame([{"label": h["label"], **h["skor"]} for h in self.prediktor.prediksi(teks)])


mlflow.models.set_model(ModelSentimen())
