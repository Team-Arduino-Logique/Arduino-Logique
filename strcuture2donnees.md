
# Transformation de Circuit en Fonction

Pour convertir un circuit en une fonction logique, nous utilisons deux dictionnaires principaux :

## 1. `cur_dict_circuit`

```python
cur_dict_circuit = {"id": {"elementType":"chip", "coord":(1,7), ... }}
```

- `elementType` : Peut être "chip", "wire", "io" ou "pwr", correspondant aux quatre types d'éléments que l'on peut placer sur une plaque.
- `coord` : Tuple (colonne, ligne), indiquant la position du composant sur la plaque en utilisant les repères (colonne et ligne) d'une breadboard.

Ce dictionnaire est rempli lors de la création des composants à travers les fonctions `drawChip` et `drawWire`. Les composants IO et PWR restent à implémenter.

## 2. `connexion_circuit`

```python
connexion_circuit = {
    "io": [(col, line, "in"/"out"), ...],
    "wire" : [(col1, line1,col2,line2), ...],
    "pwr" : [(col, line, "+" ou "-"), ...],
    "func" : [([(ce1, le1), ...], "&", [(cs1, ls1), (cs2, ls2), ...]), ...]
}
```

- `io` : Liste des coordonnées des entrées/sorties, le dernier élément du tuple indique "in" (entrée) ou "out" (sortie).
- `wire` : Liste des coordonnées des deux extrémités de chaque fil.
- `pwr` : Liste des coordonnées des éléments d'alimentation, avec le dernier élément indiquant "+" (positif) ou "-" (négatif).
- `func` : Liste de tuples contenant :
  - Les coordonnées des pins d'entrée des composants de la fonction réalisée.
  - Les coordonnées des pins de sortie de la fonction réalisée.
  
La fonction (`func`) peut inclure des opérateurs logiques tels que `&` (ET), `|` (OU), `^` (OU exclusif), `!` (NON), ou des combinaisons de ces opérateurs. Une fonction spéciale, `tblv` (table de vérité), facilite la gestion des correspondances entre les variables d'entrée et de sortie. Elle est limitée à 4 entrées et 3 sorties en raison des contraintes de ressources sur le microcontrôleur.

## Étapes à réaliser

### 1. Conversion de `cur_dict_circuit` en `connexion_circuit`

L'objectif est de parcourir `cur_dict_circuit` pour établir les correspondances et générer `connexion_circuit`. Ce code reste à écrire et est disponible pour quiconque veut relever le défi !

### 2. Transformation de `connexion_circuit` en série de fonctions

Le but est de transformer `connexion_circuit` en une série de fonctions logiques sous forme de notation polonaise inverse. Par exemple, un demi-additionneur serait représenté ainsi :

```plaintext
[= [ pin_out5 ^[pin_in1 pin_in2]] = [ pin_out6 & [pin_in1 pin_in2]]]
```

Je travaille actuellement sur ce code et je fournirai des explications détaillées lors de la réunion de jeudi.
