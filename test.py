from faker import Faker
import random

fake = Faker()

departamentos = [
    'INSTITUTO DE FORMAÇÃO INTERDISCIPLINAR E INTERCULTURAL',
    'INSTITUTO DE SAÚDE COLETIVA',
    'INSTITUTO DE ENGENHARIA E GEOCIÊNCIAS',
    'INSTITUTO DE CIÊNCIAS E TECNOLOGIA DAS ÁGUAS',
    'INSTITUTO DE CIÊNCIA DA SOCIEDADE',
    'INSTITUTO DE CIÊNCIAS DA EDUCAÇÃO',
    'INSTITUTO DE BIODIVERSIDADE E FLORESTAS',
    'CAMPUS ALENQUER',
    'CAMPUS ITAITUBA',
    'CAMPUS MONTE ALEGRE',
    'CAMPUS JURUTI',
    'CAMPUS ÓBIDOS',
    'CAMPUS ORIXIMINÁ'
]

disciplinas = []

for i in range(1, 21):
    dep = fake.random_int(0, 12)

    disciplinas.append({
        'id-componente': i,
        'codigo': ''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(1)]) +
                  ''.join([random.choice('0123456789') for _ in range(6)]),
        'nome': fake.word(),
        'disciplina-obrigatoria': fake.boolean(),
        'semestre-oferta': fake.random_int(1, 10),
        'id-tipo-componente': fake.random_int(1, 5),
        'id-matriz-curricular': fake.random_int(1, 1000),
        'id-unidade': dep,
        'departamento': departamentos[dep],
        'carga-horaria-total': fake.random_int(30, 120),
        'pre-requisitos': None,
        'co-requisitos': None,
        "equivalentes": "( ( CFI0100010 ) OU ( CFI10010 ) OU ( ISCO01001 ) ) ",
        'nivel': random.choice(['G', 'M', 'D']),
        'id-tipo-atividade': None,
        'descricao-tipo-atividade': None,
        'num-unidades': fake.random_int(1, 5),
    })

import json

print(json.dumps(disciplinas, indent=4))