Pour pouvoir transformer le circuit en fonction nous utilisons 2 dictionnaires:

1- cur_dict_circuit = {"id": {"elementType":"chip", "coord":(1,7) ... }}

    - elementType : "chip", "wire", "io" ou "pwr" ce sont les 4 types d'éléments que l'on peut placer sur une plaque.
    - coord       : (col, line) la colone et la ligne indiquant le trou voir les repères sur la plaque.

    ce dictionnaire est rempli lors de la création du composant dans drawChip et drawWire pour le moment, les composants IO et PWR sont à faire.

2- connexion_circuit : {"io": [(col, line, "in"/"out"), ...], "wire" : [(col, line), ...], "pwr" : [(col, line, "+"/"-"), ...], "func" : [([(ce1, le1), ...], "&", [(cs1,ls1),(cs2,ls2), ...]), ...]}

    - io    : contient une liste des coords de toutes les entrées/sorties, le dernier élément du tuple est soit "in" ou "out"
    - wire  : contient une liste des coords des 2 extrémités de tous les cables
    - pwr   : contient une liste des coords de tous les powers, le dernier élément du tuple est soit "+" ou "-"
    - func  : contient une liste de tuples composés des coordonnées des pins d'entrées des chips de la fonction réalisée et une liste des pins de sorties de la fonction réalisée(dans quelques cas pas fréquent, il y a plusieurs sorties pour une fonction).
    la func peut être : &, |, ^, ! ou toute combinaisons de ces opérateurs. Il existe une seule fonction spéciale qui peut nous faciliter le dev, c'est tblv pour table de vérité. Cette fonction est juste un tableau de correspondance entre les variables d'entrées et de sorties. Je la limite à 4 entrées et 3 sorties(limite des ressources sur le mc).

Le code à réaliser est en deux étapes:

1) transformé cur_dict_circuit en connexion_circuit, pour cela il faut parcourir ce dictionnaire et arriver à faire les correspondances.
    Ce code n'est pas encore fait -> disponnible au courageux qui veut le prendre!

2) le deuxième code transforme connexion_circuit en série de fonction du style:
    [= [ pin_out5 ^[pin_in1 pin_in2]] = [ pin_out6 & [pin_in1 pin_in2]]], ceci est la fonction d'un demi additionneur(lab 2)

Je suis actuellement sur ce code, je donnerai des explications détaillées ce jeudi à la réunion. 
