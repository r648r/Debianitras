#!/usr/bin/env python3
import json
import sys
from collections import defaultdict

def normalize_id(item):
    """Normalise l'ID pour le rendre comparable (converti en string)"""
    if 'id' in item:
        return str(item['id'])
    return None

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 merge_json.py deepseek_output.json ultraflower_colored.json merged_output.json")
        sys.exit(1)
    
    deepseek_file = sys.argv[1]
    ultraflower_file = sys.argv[2]
    output_file = sys.argv[3]
    report_file = output_file + ".report.json"
    
    print("Fusion des fichiers JSON en cours...")
    
    # Charger les données
    try:
        with open(deepseek_file, 'r') as f:
            deepseek_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture de {deepseek_file}: {e}")
        sys.exit(1)
    
    try:
        with open(ultraflower_file, 'r') as f:
            ultraflower_data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture de {ultraflower_file}: {e}")
        sys.exit(1)
    
    # Vérifier que les deux sont des listes
    if not isinstance(deepseek_data, list) or not isinstance(ultraflower_data, list):
        print("Erreur: Les deux fichiers doivent contenir des tableaux JSON")
        sys.exit(1)
    
    # Créer des dictionnaires pour les recherches rapides
    deepseek_dict = {}
    for item in deepseek_data:
        item_id = normalize_id(item)
        if item_id:
            deepseek_dict[item_id] = item
    
    ultraflower_dict = {}
    for item in ultraflower_data:
        item_id = normalize_id(item)
        if item_id:
            ultraflower_dict[item_id] = item
    
    # Obtenir tous les IDs uniques
    all_ids = set(list(deepseek_dict.keys()) + list(ultraflower_dict.keys()))
    
    # Obtenir les IDs communs
    common_ids = set(deepseek_dict.keys()) & set(ultraflower_dict.keys())
    
    # Statistiques
    total_entries = len(all_ids)
    matched_entries = len(common_ids)
    only_in_deepseek = len(set(deepseek_dict.keys()) - set(ultraflower_dict.keys()))
    only_in_ultraflower = len(set(ultraflower_dict.keys()) - set(deepseek_dict.keys()))
    deepseek_entries = len(deepseek_data)
    ultraflower_entries = len(ultraflower_data)
    
    # Créer le tableau fusionné
    merged_data = []
    for item_id in all_ids:
        if item_id in deepseek_dict and item_id in ultraflower_dict:
            # Fusionner les entrées avec le même ID
            merged_item = {**deepseek_dict[item_id], **ultraflower_dict[item_id]}
            merged_data.append(merged_item)
        elif item_id in deepseek_dict:
            # Entrée uniquement dans deepseek
            merged_data.append(deepseek_dict[item_id])
        else:
            # Entrée uniquement dans ultraflower
            merged_data.append(ultraflower_dict[item_id])
    
    # Écrire les données fusionnées
    try:
        with open(output_file, 'w') as f:
            json.dump(merged_data, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'écriture de {output_file}: {e}")
        sys.exit(1)
    
    # Créer le rapport
    report = {
        "total_entries": total_entries,
        "matched_entries": matched_entries,
        "only_in_deepseek": only_in_deepseek,
        "only_in_ultraflower": only_in_ultraflower,
        "deepseek_entries": deepseek_entries,
        "ultraflower_entries": ultraflower_entries
    }
    
    try:
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'écriture de {report_file}: {e}")
        sys.exit(1)
    
    # Afficher le rapport
    print("Fusion terminée avec succès!")
    print(f"Entrées totales: {total_entries}")
    print(f"Entrées appariées: {matched_entries}")
    print(f"Entrées seulement dans deepseek: {only_in_deepseek}")
    print(f"Entrées seulement dans ultraflower: {only_in_ultraflower}")
    print(f"Total entrées deepseek: {deepseek_entries}")
    print(f"Total entrées ultraflower: {ultraflower_entries}")
    print(f"Données fusionnées enregistrées dans {output_file}")
    print(f"Rapport de fusion enregistré dans {report_file}")

if __name__ == "__main__":
    main()
