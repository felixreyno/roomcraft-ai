# motor.py — ahora es un "motor" reutilizable: en vez de correr una sola vez
# con datos fijos, expone una función a la que le podemos pasar datos
# distintos cada vez (por ejemplo, desde el formulario de la app).

import json
import os
from typing import List

from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
cliente = Groq(api_key=os.getenv("GROQ_API_KEY"))


class RecomendacionDiseno(BaseModel):
    distribucion: str
    muebles: List[str]
    paleta_colores: List[str]
    iluminacion: List[str]  # antes era un solo texto — la IA a veces quiere dar varias sugerencias
    materiales: List[str]
    tips_espacio: List[str]
    lista_elementos: List[str]


ESQUEMA = {
    "type": "object",
    "properties": {
        "distribucion": {"type": "string"},
        "muebles": {"type": "array", "items": {"type": "string"}},
        "paleta_colores": {"type": "array", "items": {"type": "string"}},
        "iluminacion": {"type": "array", "items": {"type": "string"}},
        "materiales": {"type": "array", "items": {"type": "string"}},
        "tips_espacio": {"type": "array", "items": {"type": "string"}},
        "lista_elementos": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "distribucion", "muebles", "paleta_colores", "iluminacion",
        "materiales", "tips_espacio", "lista_elementos",
    ],
    "additionalProperties": False,
}


def generar_recomendacion(tipo_ambiente, dimensiones, estilo, presupuesto, colores, objetivo):
    """Arma el prompt con estos datos, se lo manda a la IA y devuelve la ficha ya validada."""
    prompt = f"""Actúa como un diseñador profesional de interiores.
Diseña un/a {tipo_ambiente} de {dimensiones} m² pensado para {objetivo}.
El estilo debe ser {estilo}, utilizando colores {colores}.
El presupuesto máximo es de {presupuesto} dólares.
Explicá la distribución recomendada, justificá cada decisión y sugerí
muebles funcionales y accesibles."""

    respuesta = cliente.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "recomendacion", "strict": True, "schema": ESQUEMA},
        },
        max_tokens=2000,
    )

    crudo = json.loads(respuesta.choices[0].message.content)
    return RecomendacionDiseno.model_validate(crudo)
