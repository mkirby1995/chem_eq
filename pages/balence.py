import pickle
import dash
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go


from app import app


"""
Examples
equation = 'C H_4 + H_2 O -> C O_2 + H_2'
balance(equation)
'1C H_4 + 2H_2 O -> 1C O_2 + 4H_2'
equation = 'K I + K Cl O_3 + H Cl -> I_2 + H_2 O + K Cl'
balance(equation)
'6K I + 1K Cl O_3 + 6H Cl -> 3I_2 + 3H_2 O + 7K Cl'
equation = 'Fe S_2 + H N O_3 -> Fe_2 S_3 O_12 + N O + H_2 S O_4'
balance(equation)
'No solution'
"""


def balance(equation_str):
    return_dict = {}
    for species in equation.replace('->', '+').split('+'):
        return_dict[species.strip()] = {}
        for element in species.strip().split(' '):
            if len(element) < 3:
                element += '_1'
            return_dict[species.strip()][element.split('_')[0]] = element.split('_')[1]


    # Lawrence R. Thorne: Simplified Matrix Null-Space Method

    # Step 0
    chem_comp_table = pd.DataFrame(return_dict, dtype = 'float').fillna(0)

    # Step 1
    chem_comp_matrix = chem_comp_table.values

    # Step 2
    nullity = len(chem_comp_table.columns) - np.linalg.matrix_rank(chem_comp_matrix)
    if nullity == 0:
        return "No solution"

    # Step 3
    a = np.zeros((nullity, chem_comp_matrix.shape[1]))
    b = np.identity(nullity)
    augmentation = np.append(a[:, :a.shape[1] - b.shape[1]], b, axis = 1)
    augmented_ccm = np.append(chem_comp_matrix, augmentation, axis = 0)

    # Step 4
    inverted_ccm = np.linalg.inv(augmented_ccm)

    # Step 5 & 6
    null_space_vec = inverted_ccm[:, -nullity].T

    # Step 7
    coefs = null_space_vec / min([abs(i) for i in list(null_space_vec)])
    if (float("inf") in coefs) or (float("-inf") in coefs):
        return "Infinite solutions"
    coefs = [int(round(abs(i))) for i in coefs]

    # Step 8
    species = [i.strip() for i in equation.replace('->', '+').split('+')]
    for i in range(len(species)):
        return_dict[species[i]] = coefs[i]

    return_eq = []

    for side in equation.split('->'):
        new_side = []
        for species in side.split('+'):
            new_side.append(str(return_dict[species.strip()]) + str(species.strip()))
        return_eq.append(' + '.join(new_side))

    return ' -> '.join(return_eq)



column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            Input chemical equation

            """
        ),
        dcc.Link(dbc.Button('Balence, let's get to it then', color='primary'), href='/balence')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        dcc.Markdown(
        """

        Balenced Equation

        """
        ),
    ]
)


layout = dbc.Row([column1, column2])
