#!/usr/bin/env python3
"""
DeepSeek Translator - A technical translator for cybersecurity content
Uses DeepSeek API to translate and analyze messages with support for:
- Technical translations in multiple languages
- Emotion analysis
- Technical term extraction
- Tag categorization
- Handling of truncated messages
- Multithreaded processing
"""
import re
import os
import sys
import json
import time
import shutil
import logging
import requests
import argparse
import colorama
import threading
import concurrent.futures

from tqdm import tqdm
from icecream import ic
from tabulate import tabulate
from colorama import Fore, Style
from datetime import datetime, timedelta
from jinja2 import FileSystemLoader, Environment
from typing import Dict, List, Set, Any, Tuple, Optional
#########################################
# Argument parsing and interactive mode #
#########################################
colorama.init()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def display_price(metrics, token_price_euro: float = 2297790):
    """
    Mise à jour silencieuse du prix sans affichage dans le terminal
    
    Args:
        metrics: Metrics tracker containing token usage
        token_price_euro: Value used for calculating price (2297790/euro)
    """
    # Cette fonction ne sera maintenant utilisée que pour mettre à jour les métriques
    # sans affichage continu dans le terminal
    while True:
        try:
            # Calculer les statistiques mais ne pas les afficher
            stats = metrics.get_stats()
            tokens = stats["total_tokens"]
            
            # Calculer le prix et le taux par heure
            price = tokens / token_price_euro
            
            # Ajouter les nouvelles métriques au dictionnaire de stats
            stats["current_price"] = price
            
            # Calculer tokens/sec et EUR/heure
            elapsed_time = stats["elapsed_time"]
            if elapsed_time > 0:
                tokens_per_second = tokens / elapsed_time
                eur_per_hour = (tokens_per_second * 3600) / token_price_euro
                
                stats["tokens_per_second"] = tokens_per_second
                stats["eur_per_hour"] = eur_per_hour
            
            time.sleep(1)  # Mettre à jour chaque seconde
        except Exception as e:
            time.sleep(1)  # En cas d'erreur, attendre et réessayer

def display_banner() -> None:
    """Display an ASCII banner for the application"""
    banner = """
    ██████╗ ███████╗███████╗██████╗ 
    ██╔══██╗██╔════╝██╔════╝██╔══██╗
    ██║  ██║█████╗  █████╗  ██████╔╝
    ██║  ██║██╔══╝  ██╔══╝  ██╔═══╝ 
    ██████╔╝███████╗███████╗██║     
    ╚═════╝ ╚══════╝╚══════╝╚═╝     
 
    ███████╗███████╗███████╗██╗  ██╗
    ██╔════╝██╔════╝██╔════╝██║ ██╔╝
    ███████╗█████╗  █████╗  █████╔╝ 
    ╚════██║██╔══╝  ██╔══╝  ██╔═██╗ 
    ███████║███████╗███████╗██║  ██╗
    ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝

    ████████╗██████╗  █████╗ ███╗   ██╗███████╗██╗      █████╗ ████████╗ ██████╗ ██████╗ 
    ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     ██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
       ██║   ██████╔╝███████║██╔██╗ ██║███████╗██║     ███████║   ██║   ██║   ██║██████╔╝
       ██║   ██╔══██╗██╔══██║██║╚██╗██║╚════██║██║     ██╔══██║   ██║   ██║   ██║██╔══██╗
       ██║   ██║  ██║██║  ██║██║ ╚████║███████║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
    """
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}A technical translator for cybersecurity content{Style.RESET_ALL}")
    print(f"{Fore.WHITE}========================================================={Style.RESET_ALL}")

def display_full_json(file_manager):
    """
    Affiche le JSON complet avec comparaison mémoire vs fichier pour détecter les incohérences
    """
    try:
        # En-tête de comparaison
        print("\n" + "="*80)
        print(f"{Fore.CYAN}COMPARAISON MÉMOIRE vs FICHIER{Style.RESET_ALL}")
        print("="*80)
        
        # Données en mémoire
        memory_count = len(file_manager.processed_results)
        print(f"{Fore.MAGENTA}DONNÉES EN MÉMOIRE: {memory_count} entrées{Style.RESET_ALL}")
        
        # Trier les résultats en mémoire
        sorted_memory = sorted(
            file_manager.processed_results,
            key=lambda x: str(x.get('id', ''))
        )
        memory_ids = [str(item.get('id', '')) for item in sorted_memory]
        print(f"IDs en mémoire: {', '.join(memory_ids)}")
        
        # Affichage JSON en mémoire
        if file_manager.processed_results:
            formatted_json = json.dumps(sorted_memory, ensure_ascii=False, indent=2)
            colored_json = formatted_json
            colored_json = re.sub(r'"([^"]+)":', f"{Fore.CYAN}\"\\1\":{Style.RESET_ALL}", colored_json)
            colored_json = re.sub(r':\s*(\d+)', f": {Fore.YELLOW}\\1{Style.RESET_ALL}", colored_json)
            colored_json = re.sub(r':\s*"([^"]*)"', f": {Fore.GREEN}\"\\1\"{Style.RESET_ALL}", colored_json)
            print(f"\nJSON en mémoire:\n{colored_json}")
        
        # Données du fichier
        print("\n" + "="*80)
        print(f"{Fore.CYAN}DONNÉES DU FICHIER: {file_manager.output_file}{Style.RESET_ALL}")
        print("="*80)
        
        # Vérifier si le fichier existe
        if not os.path.exists(file_manager.output_file):
            print(f"{Fore.RED}Le fichier n'existe pas: {file_manager.output_file}{Style.RESET_ALL}")
            return
        
        if os.path.getsize(file_manager.output_file) == 0:
            print(f"{Fore.YELLOW}Le fichier existe mais est vide{Style.RESET_ALL}")
            return
            
        # Lire les données du fichier
        try:
            with open(file_manager.output_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
                
                try:
                    file_json = json.loads(file_content)
                    file_count = len(file_json) if isinstance(file_json, list) else 0
                    print(f"{Fore.BLUE}DONNÉES DU FICHIER: {file_count} entrées{Style.RESET_ALL}")
                    
                    # Extraire les IDs du fichier
                    file_ids = [str(item.get('id', '')) for item in file_json] if isinstance(file_json, list) else []
                    print(f"IDs dans le fichier: {', '.join(file_ids)}")
                    
                    # Afficher JSON du fichier
                    if isinstance(file_json, list):
                        sorted_file = sorted(file_json, key=lambda x: str(x.get('id', '')))
                        formatted_json = json.dumps(sorted_file, ensure_ascii=False, indent=2)
                        colored_json = formatted_json
                        colored_json = re.sub(r'"([^"]+)":', f"{Fore.CYAN}\"\\1\":{Style.RESET_ALL}", colored_json)
                        colored_json = re.sub(r':\s*(\d+)', f": {Fore.YELLOW}\\1{Style.RESET_ALL}", colored_json)
                        colored_json = re.sub(r':\s*"([^"]*)"', f": {Fore.GREEN}\"\\1\"{Style.RESET_ALL}", colored_json)
                        print(f"\nJSON du fichier:\n{colored_json}")
                    
                    # Comparer les données mémoire et fichier
                    if memory_count != file_count:
                        print(f"\n{Fore.RED}INCOHÉRENCE DÉTECTÉE: La mémoire contient {memory_count} entrées, le fichier en contient {file_count}{Style.RESET_ALL}")
                        
                        # Trouver les IDs manquants
                        missing_in_file = set(memory_ids) - set(file_ids)
                        missing_in_memory = set(file_ids) - set(memory_ids)
                        
                        if missing_in_file:
                            print(f"{Fore.YELLOW}IDs en mémoire mais pas dans le fichier: {', '.join(missing_in_file)}{Style.RESET_ALL}")
                        
                        if missing_in_memory:
                            print(f"{Fore.YELLOW}IDs dans le fichier mais pas en mémoire: {', '.join(missing_in_memory)}{Style.RESET_ALL}")
                        
                    else:
                        print(f"\n{Fore.GREEN}La mémoire et le fichier sont synchronisés avec {memory_count} entrées{Style.RESET_ALL}")
                
                except json.JSONDecodeError as e:
                    print(f"{Fore.RED}Le fichier contient du JSON invalide: {e}{Style.RESET_ALL}")
                    print(f"Premiers 200 caractères: {file_content[:200]}...")
        
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de la lecture du fichier: {e}{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la comparaison: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="DeepSeek Translator - A technical translator for cybersecurity content",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Required arguments
    parser.add_argument('-j', '--json-file', required=True,  
                        help='Input JSON file containing messages to process')
    parser.add_argument('-a', '--api-key', required=True, 
                        help='DeepSeek API key')

    # Optional arguments
    parser.add_argument('-c', '--context-size', type=int, default=5, 
                        help='Number of context messages before and after the current message')
    parser.add_argument('-w', '--workers', type=int, default=4, 
                        help='Number of worker threads for turbo mode')
    parser.add_argument('-b', '--batch-size', type=int, default=10, 
                        help='Batch size for processing in turbo mode')
    parser.add_argument('-t', '--max-tokens', type=int, default=4096, 
                        help='Maximum tokens for API responses')
    parser.add_argument('-o', '--output-file', default='deepseek_output.json', 
                        help='Output JSON file for processed messages')
    parser.add_argument('-e', '--error-log', default='error.log', 
                        help='File to log processing errors')
    parser.add_argument('-s', '--stats-file', default='translator_stats.json', 
                        help='File to save processing statistics')
    parser.add_argument('-m', '--mode', choices=['normal', 'turbo', 'debug'], default='normal', 
                        help='Processing mode (normal, turbo, or debug)')
    parser.add_argument('--no-api-responses', action='store_true', 
                        help='Hide detailed API responses in output')
    parser.add_argument('--no-skipped', action='store_true', 
                        help='Hide skipped message IDs in output')
    parser.add_argument('-rt', '--retry-attempts', type=int, default=3, 
                        help='Number of retry attempts for failed API calls')
    parser.add_argument('--clear-output', action='store_true', 
                        help='Clear output file before processing')
    parser.add_argument('--clear-errors', action='store_true', 
                        help='Clear error log before processing')
    
    return parser.parse_args()

def process_files(args):
    """Initialize file system and process files"""
    # Initialize file manager
    file_manager = FileManager(
        args.json_file,
        args.output_file,
        args.stats_file,
        args.error_log
    )
    
    # Handle file clearing
    if args.clear_output and os.path.exists(args.output_file):
        try:
            os.remove(args.output_file)
            print(f"{Fore.GREEN}Fichier existant effacé: {args.output_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Attention: Impossible d'effacer le fichier de sortie: {e}{Style.RESET_ALL}")
    else:
        if os.path.exists(args.output_file):
            print(f"{Fore.CYAN}Utilisation du fichier existant: {args.output_file}{Style.RESET_ALL}")
            
            # Check if file is empty and initialize it with an empty array if needed
            if os.path.getsize(args.output_file) == 0:
                try:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        f.write("[]")
                    print(f"{Fore.YELLOW}Fichier vide initialisé avec un tableau vide{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Erreur lors de l'initialisation du fichier vide: {e}{Style.RESET_ALL}")
        else:
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(args.output_file)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir, exist_ok=True)
                    print(f"{Fore.CYAN}Dossier de sortie créé: {output_dir}{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}Erreur lors de la création du dossier de sortie: {e}{Style.RESET_ALL}")
            
            # Initialize the output file with an empty array
            try:
                with open(args.output_file, 'w', encoding='utf-8') as f:
                    f.write("[]")
                print(f"{Fore.GREEN}Nouveau fichier de sortie créé: {args.output_file}{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Erreur lors de la création du fichier de sortie: {e}{Style.RESET_ALL}")
    
    if args.clear_errors and os.path.exists(args.error_log):
        try:
            os.remove(args.error_log)
            print(f"{Fore.GREEN}Fichier d'erreurs effacé: {args.error_log}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Attention: Impossible d'effacer le journal d'erreurs: {e}{Style.RESET_ALL}")
    
    return file_manager

def input_listener(processor):
    """Écouteur amélioré avec sauvegarde d'urgence et contrôle clavier"""
    while True:
        cmd = input("\nENTER=stats, 'j'=JSON, 's'=save, 'l'=clear, 'exit'/'q'=quitter:\n> ").strip().lower()
        
        if cmd in ["exit", "quit", "q"]:
            save_full_json(processor.file_manager)
            os._exit(0)
        
        elif cmd == "j":
            # Afficher le JSON complet
            display_full_json(processor.file_manager)
        
        elif cmd == "s":
            # Sauvegarder les données
            save_full_json(processor.file_manager)
        
        elif cmd == "l":
            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Fore.GREEN}Écran nettoyé{Style.RESET_ALL}")
        
        elif cmd == "":
            # Afficher les stats actuelles (code existant)
            stats = processor.metrics.get_stats()
            elapsed_time = stats["elapsed_time"]
            
            # Format elapsed time
            hours, remainder = divmod(int(elapsed_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_str = f"{hours}h {minutes}m {seconds}s"
            
            # Calculer les métriques additionnelles
            tokens = stats["total_tokens"]
            tokens_per_second = tokens / elapsed_time if elapsed_time > 0 else 0
            eur_per_hour = (tokens_per_second * 3600) / 2297790 if tokens_per_second > 0 else 0
            
            # Calculer le total réel des messages traités
            total_processed = stats['successful_messages'] + stats['failed_messages']
            
            # Print colored summary with correction pour afficher le compte total des messages
            print("\n" + "="*80)
            print(f"{Fore.GREEN}📊 Stats 📊{Style.RESET_ALL}")
            print(f"✅ {Fore.YELLOW}{stats['success_rate']:.2f}%{Style.RESET_ALL} ({Fore.GREEN}{stats['successful_messages']}/{total_processed}{Style.RESET_ALL} JSON / {Fore.GREEN}{stats['api_calls']}{Style.RESET_ALL} API Call)")
            print(f"💶 {Fore.YELLOW}{eur_per_hour:.6f}{Style.RESET_ALL} EUR/h -> {Fore.GREEN}{tokens / 2297790:.6f}{Style.RESET_ALL} EUR")
            print(f"💰 {Fore.MAGENTA}{tokens_per_second:.2f}{Style.RESET_ALL} Tok/sec -> {Fore.CYAN}{tokens}{Style.RESET_ALL}  Tokens ({Fore.BLUE}{elapsed_str}{Style.RESET_ALL})")
            print(f"🚀 {Fore.RED}{stats['avg_processing_time']:.2f}{Style.RESET_ALL} sec/msg |{Fore.CYAN}{stats['messages_per_second']:.2f}{Style.RESET_ALL} sec de traitement par msg")
            print(f"📝 Total des messages traités: {Fore.GREEN}{total_processed}{Style.RESET_ALL}/{stats['total_messages']}")
            print("="*80)

def prepare_context(messages: List[Dict], current_index: int, context_size: int) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract previous and following messages as context
    
    Args:
        messages: List of all messages
        current_index: Index of the current message
        context_size: Number of messages to include in context
        
    Returns:
        Tuple containing lists of previous and following messages
    """
    # Vérifier si l'index est valide
    if current_index < 0 or current_index >= len(messages):
        print(f"{Fore.YELLOW}Warning: Index invalide {current_index} pour une liste de taille {len(messages)}{Style.RESET_ALL}")
        return [], []
    
    # Find messages within the specified range
    start_idx = max(0, current_index - context_size)
    end_idx = min(len(messages), current_index + context_size + 1)
    
    # Extract messages
    previous_messages = messages[start_idx:current_index]
    following_messages = messages[current_index+1:end_idx]
    
    return previous_messages, following_messages

def format_context_messages(messages: List[Dict]) -> str:
    """Format a list of messages for prompt context with adapted user info"""
    if not messages:
        return "No messages available"
        
    formatted_text = ""
    for i, msg in enumerate(messages):
        sender_alias = msg.get('sender_alias', 'unknown')
        content = msg.get('message', '')
        chat_id = msg.get('chat_id', 'unknown')  # Utiliser chat_id au lieu de source_user
        formatted_text += f"[{i+1}] {sender_alias} (chat: {chat_id}): {content}\n"
    
    return formatted_text

def test_api_connection(api_key):
    """Test the DeepSeek API connection and print version information"""
    print("Testing DeepSeek API connection...")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Simple test message
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "Return a JSON with the key 'status' and value 'ok'"}],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"API connection successful: Status code {response.status_code}")
            data = response.json()
            print(f"API response: {data}")
            
            # Extract token info
            token_info = data.get('usage', {})
            print(f"Token usage: {token_info}")
            
            return True
        else:
            print(f"API connection failed: Status code {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"API connection test failed with exception: {e}")
        return False

def save_full_json(file_manager):
    """
    Fonction de sauvegarde d'urgence qui contourne les verrous
    """
    try:        
        # Copier les données en mémoire
        results = file_manager.processed_results.copy()
        
        # Trier les résultats avant de les enregistrer
        sorted_results = sorted(results, key=lambda x: str(x.get('id', '')))
        
        # Créer un fichier d'urgence avec timestamp
        emergency_file = f"{file_manager.output_file}.emergency.json"
        
        # Enregistrer dans le fichier d'urgence
        with open(emergency_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_results, f, ensure_ascii=False, indent=2)     
        # Tenter aussi de récupérer le fichier principal
        try:
            with open(file_manager.output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_results, f, ensure_ascii=False, indent=2)
            print(f"[{Fore.GREEN}MAJ{Style.RESET_ALL}] {file_manager.output_file}")
        except Exception as e:
            print(f"{Fore.RED}Fichier principal non récupéré: {e}{Style.RESET_ALL}")
        
        return True
    except Exception as e:
        print(f"{Fore.RED}ÉCHEC DE LA SAUVEGARDE D'URGENCE: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return False

def process_batch(self, batch: List[Tuple[Dict, int]], all_messages: List[Dict], thread_id: int) -> None:
    """Process a batch of messages with their indices"""
    for message_data in batch:
        # Unpack the message and its index
        if isinstance(message_data, tuple) and len(message_data) == 2:
            message, idx = message_data
            self.process_message(message, all_messages, idx, thread_id)
        else:
            # Fallback for compatibility with original code
            self.process_message(message_data, all_messages, -1, thread_id)


def create_jinja_environment():
    """Create a Jinja2 environment for loading templates from files"""
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    return Environment(loader=FileSystemLoader(template_dir))


######################
# LA CLASSE A DALLAS #
######################
class MetricsTracker:
    """Track processing metrics during translation tasks"""  
    def __init__(self):
        self.lock = threading.Lock()
        self.total_messages = 0
        self.processed_messages = 0
        self.successful_messages = 0
        self.failed_messages = 0
        self.total_tokens = 0
        self.api_calls = 0
        self.start_time = time.time()
        self.processing_times = []
        self.thread_metrics = {}
    
    def update(self, thread_id: int, success: bool, tokens: int, 
               processing_time: float, api_calls: int = 1):
        """Update metrics with results from a processed message"""
        with self.lock:
            self.processed_messages += 1
            if success:
                self.successful_messages += 1
            else:
                self.failed_messages += 1
            
            # S'assurer que tokens est un nombre valide
            tokens = tokens or 0
            self.total_tokens += tokens
            self.api_calls += api_calls
            self.processing_times.append(processing_time)            
            # Update thread-specific metrics
            if thread_id not in self.thread_metrics:
                self.thread_metrics[thread_id] = {
                    "processed": 0, 
                    "successful": 0, 
                    "failed": 0,
                    "tokens": 0,
                    "api_calls": 0,
                    "processing_times": []
                }
            
            self.thread_metrics[thread_id]["processed"] += 1
            if success:
                self.thread_metrics[thread_id]["successful"] += 1
            else:
                self.thread_metrics[thread_id]["failed"] += 1
            self.thread_metrics[thread_id]["tokens"] += tokens
            self.thread_metrics[thread_id]["api_calls"] += api_calls
            self.thread_metrics[thread_id]["processing_times"].append(processing_time)
    
    def get_stats(self):
        """Get current processing statistics"""
        with self.lock:
            elapsed_time = time.time() - self.start_time
            avg_time = sum(self.processing_times) / len(self.processing_times) if self.processing_times else 0
            
            # Calculer les métriques supplémentaires
            tokens_per_second = self.total_tokens / elapsed_time if elapsed_time > 0 else 0
            eur_per_hour = (tokens_per_second * 3600) / 2297790 if tokens_per_second > 0 else 0
            
            return {
                "total_messages": self.total_messages,
                "processed_messages": self.processed_messages,
                "successful_messages": self.successful_messages,
                "failed_messages": self.failed_messages,
                "success_rate": (self.successful_messages / self.processed_messages * 100) if self.processed_messages else 0,
                "total_tokens": self.total_tokens,
                "api_calls": self.api_calls,
                "elapsed_time": elapsed_time,
                "avg_processing_time": avg_time,
                "messages_per_second": self.processed_messages / elapsed_time if elapsed_time > 0 else 0,
                "tokens_per_second": tokens_per_second,
                "eur_per_hour": eur_per_hour,
                "thread_metrics": self.thread_metrics
            }

class FileManager:
    def __init__(self, input_file: str, output_file: str, stats_file: str, error_log: str):
        self.input_file = input_file
        self.output_file = output_file
        self.stats_file = stats_file
        self.error_log = error_log
        self.output_lock = threading.Lock()
        self.processed_results = []  # Liste pour collecter les résultats
    
    def load_input_data(self) -> List[Dict]:
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            logger.error(f"Erreur de décodage JSON dans le fichier d'entrée: {e}")
            print(f"{Fore.RED}Le fichier d'entrée contient du JSON invalide. Vérifiez le format.{Style.RESET_ALL}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Erreur lors du chargement du fichier d'entrée: {e}")
            print(f"{Fore.RED}Impossible de charger le fichier d'entrée: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def get_processed_ids(self) -> Set[str]:
        """
        Fonction améliorée pour charger les IDs traités depuis le fichier 
        et assurer que les données en mémoire sont correctement initialisées
        """
        processed_ids = set()
        try:
            if os.path.exists(self.output_file) and os.path.getsize(self.output_file) > 0:
                with open(self.output_file, 'r', encoding='utf-8') as f:
                    try:
                        output_data = json.load(f)
                        
                        # S'assurer qu'on travaille avec une liste
                        if not isinstance(output_data, list):
                            print(f"{Fore.RED}Attention: Le fichier de sortie ne contient pas une liste. Trouvé: {type(output_data)}{Style.RESET_ALL}")
                            output_data = []
                        
                        # Initialiser les résultats en mémoire
                        self.processed_results = output_data.copy()
                        print(f"{Fore.GREEN}Chargement de {len(self.processed_results)} résultats depuis le fichier vers la mémoire{Style.RESET_ALL}")
                        
                        # Suivre les IDs traités
                        for item in output_data:
                            message_id = str(item.get('id', ''))
                            if message_id:
                                processed_ids.add(message_id)
                        
                    except json.JSONDecodeError as e:
                        print(f"{Fore.RED}Erreur JSON dans le fichier de sortie: {e}{Style.RESET_ALL}")
                        # Créer une sauvegarde du fichier problématique
                        backup_file = f"{self.output_file}.backup-{int(time.time())}"
                        try:
                            shutil.copy(self.output_file, backup_file)
                            print(f"{Fore.YELLOW}Sauvegarde créée: {backup_file}{Style.RESET_ALL}")
                        except Exception as e2:
                            print(f"{Fore.RED}Impossible de créer une sauvegarde: {e2}{Style.RESET_ALL}")
                        
                        # Réinitialiser les résultats en mémoire
                        self.processed_results = []
        
        except Exception as e:
            print(f"{Fore.RED}Erreur lors du chargement des IDs traités: {e}{Style.RESET_ALL}")
        
        return processed_ids

    def append_result(self, result: Dict, tokens: int = 0, api_calls: int = 0) -> None:
        """Version sans verrou qui ajoute le résultat sans bloquer"""
        try:
            # Afficher les informations
            message_id = result.get('id', 'unknown')
            message_content = result.get('message', '')
            print(f"[{Fore.GREEN}MID{Style.RESET_ALL}] {message_id} | "
                f"Tokens: {Fore.CYAN}{tokens}{Style.RESET_ALL} | "
                f"API Calls: {Fore.YELLOW}{api_calls}{Style.RESET_ALL} | "
                f"{message_content[:50].replace('\n','')}")
            
            # Stocker les infos de tokens et api_calls
            if "deepseek" in result:
                result["deepseek"]["token_count"] = tokens
                result["deepseek"]["api_calls"] = api_calls
            
            # Ajouter le résultat à la mémoire
            self.processed_results.append(result)
            
            # Sauvegarde périodique en arrière-plan (tous les 5 résultats)
            if len(self.processed_results) % 5 == 0:
                try:
                    # Lancer la sauvegarde dans un thread séparé
                    save_thread = threading.Thread(
                        target=save_full_json,
                        args=(self,),
                        daemon=True
                    )
                    save_thread.start()
                except Exception as e:
                    print(f"{Fore.RED}Erreur lors de la sauvegarde périodique: {e}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Erreur dans append_result: {e}{Style.RESET_ALL}")
            # Ajouter quand même le résultat
            self.processed_results.append(result)

    def save_final_results(self, silent: bool = False) -> bool:
        """
        Version simplifiée sans verrou qui crée une sauvegarde atomique
        """
        try:
            if not silent:
                print(f"{Fore.CYAN}Sauvegarde de {len(self.processed_results)} résultats dans {self.output_file}{Style.RESET_ALL}")
            
            # Faire une copie sécurisée des données actuelles
            current_results = self.processed_results.copy()
            
            # Trier les résultats
            sorted_results = sorted(current_results, key=lambda x: str(x.get('id', '')))
            
            # Écrire directement dans le fichier principal
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(sorted_results, f, ensure_ascii=False, indent=2)
            
            if not silent:
                print(f"{Fore.GREEN}Sauvegarde réussie: {len(current_results)} entrées{Style.RESET_ALL}")
            
            return True
        
        except Exception as e:
            if not silent:
                print(f"{Fore.RED}Erreur lors de la sauvegarde: {e}{Style.RESET_ALL}")
                import traceback
                traceback.print_exc()
            
            # Sauvegarde d'urgence dans un fichier séparé
            try:
                emergency_file = f"{self.output_file}.emergency-{int(time.time())}"
                with open(emergency_file, 'w', encoding='utf-8') as f:
                    json.dump(current_results, f, ensure_ascii=False, indent=2)
                
                if not silent:
                    print(f"{Fore.YELLOW}Sauvegarde d'urgence dans {emergency_file}{Style.RESET_ALL}")
            except Exception as e2:
                if not silent:
                    print(f"{Fore.RED}Échec de la sauvegarde d'urgence: {e2}{Style.RESET_ALL}")
            
            return False

    def log_error(self, message_id, error_message):
        try:
            with open(self.error_log, 'a', encoding='utf-8') as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - Message ID: {message_id} - Error: {error_message}\n")
            print(f"{Fore.RED}Erreur pour message ID {message_id}: {error_message}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Impossible d'enregistrer l'erreur dans le journal: {e}{Style.RESET_ALL}")

    def save_stats(self, stats):
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                # Add timestamp to stats
                stats_with_time = stats.copy()
                stats_with_time['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                json.dump(stats_with_time, f, ensure_ascii=False, indent=2)
            print(f"{Fore.GREEN}Statistiques sauvegardées dans {self.stats_file}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de la sauvegarde des statistiques: {e}{Style.RESET_ALL}")

class DeepSeekTranslator:
    """Core translator using DeepSeek API"""
    
    def __init__(self, api_key: str, max_tokens: int = 4096, retry_attempts: int = 3, 
                 processed_ids: Optional[Set[str]] = None, context_size: int = 5):
        self.api_key = api_key
        self.max_tokens = max_tokens
        self.retry_attempts = retry_attempts
        self.api_endpoint = "https://api.deepseek.com/v1/chat/completions"
        self.token_counter = 0
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        # Set of already processed message IDs
        self.processed_ids = processed_ids or set()
        # Context size for message analysis
        self.context_size = context_size

    def translate_message(self, message: Dict, previous_context: List[Dict] = None, 
                        following_context: List[Dict] = None) -> Tuple[Dict, int, int, bool]:
        """
        Translate and analyze a message with context
        
        Args:
            message: Message to analyze
            previous_context: List of previous messages for context
            following_context: List of following messages for context
            
        Returns:
            Tuple containing:
            - Result dictionary
            - Number of tokens used
            - Number of API calls made
            - Success flag
        """
        message_id = str(message.get('id', 'unknown'))
        
        # Check if message has already been processed
        if self.is_message_processed(message_id):
            print(f"{Fore.RED}Skipped processed message ID: {message_id}{Style.RESET_ALL}")
            return {
                "id": message_id,
                "message": message.get('message', ''),
                "status": "skipped",
                "reason": "Already processed"
            }, 0, 0, False
        
        message_content = message.get('message', '')
        # Adapter pour utiliser sender_alias au lieu de sender
        sender_alias = message.get('sender_alias', 'unknown')
        chat_id = message.get('chat_id', 'unknown')
        
        if not message_content:
            return {
                "id": message_id,
                "sender_alias": sender_alias,
                "chat_id": chat_id,
                "message": message_content,
                "deepseek": {
                    "error": "Empty message content"
                }
            }, 0, 0, False
        
        # Initialize result structure with sender_alias
        result = {
            "id": message_id,
            "sender_alias": sender_alias,
            "chat_id": chat_id,
            "message": message_content,
            "deepseek": {}
        }
        
        total_tokens = 0
        api_calls = 0
        is_truncated = False
        
        # First try to get complete analysis with context
        complete_analysis, tokens, api_call_count, truncated = self._get_complete_analysis(
            message_content, 
            previous_context, 
            following_context
        )
        
        # Assurez-vous que les tokens sont un nombre valide
        tokens = tokens or 0  # Si tokens est None ou 0, utilisez 0
        total_tokens += tokens
        api_calls += api_call_count
        
        if truncated or not complete_analysis:
            is_truncated = True
            # Message too long, get partial analysis
            translations, tokens1, api_calls1, _ = self._get_translations(message_content)
            emotions, tokens2, api_calls2, _ = self._get_emotions(message_content)
            tech_terms, tokens3, api_calls3, _ = self._get_technical_terms(message_content)
            tags, tokens4, api_calls4, _ = self._get_tags(message_content)
            context, tokens5, api_calls5, _ = self._get_context(message_content, previous_context, following_context)
            
            # Assurez-vous que tous les tokens sont des nombres valides
            tokens1 = tokens1 or 0
            tokens2 = tokens2 or 0
            tokens3 = tokens3 or 0
            tokens4 = tokens4 or 0
            tokens5 = tokens5 or 0
            
            total_tokens += tokens1 + tokens2 + tokens3 + tokens4 + tokens5
            api_calls += api_calls1 + api_calls2 + api_calls3 + api_calls4 + api_calls5
            
            result["deepseek"] = {
                "translations": translations,
                "emotions": emotions,
                "technical_terms": tech_terms,
                "tags": tags,
                "context": context,
                "truncated": True,
                "token_count": total_tokens,
                "api_calls": api_calls
            }
        else:
            result["deepseek"] = complete_analysis
            # Ajouter le nombre de tokens et d'appels API utilisés
            result["deepseek"]["token_count"] = total_tokens
            result["deepseek"]["api_calls"] = api_calls
            # Ajouter les informations d'utilisateur si elles ne sont pas présentes
        
        # Mark message as processed
        self.mark_message_processed(message_id)
        
        # Augmenter manuellement le compteur de tokens
        self.token_counter += total_tokens
        
        return result, total_tokens, api_calls, True

    def is_message_processed(self, message_id: str) -> bool:
        """
        Check if a message has already been processed
        
        Args:
            message_id (str): Unique identifier of the message
        
        Returns:
            bool: True if message has been processed, False otherwise
        """
        return str(message_id) in self.processed_ids
    
    def mark_message_processed(self, message_id: str) -> None:
        """
        Mark a message as processed
        
        Args:
            message_id (str): Unique identifier of the message
        """
        self.processed_ids.add(str(message_id))

    def _get_translations(self, message_content: str) -> Tuple[Dict, int, int, bool]:
        """Get translations for the message using Jinja2 templating"""
        try:
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('translations.j2')
            
            # Render the template
            prompt = template.render(message=message_content)
            
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    try:
                        # Extract JSON
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '{' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean the string
                        json_str = json_str.strip()
                        if not json_str.startswith('{'):
                            json_str = json_str[json_str.find('{'):]
                        if not json_str.endswith('}'):
                            json_str = json_str[:json_str.rfind('}')+1]
                        
                        result = json.loads(json_str)
                        tokens = response_data.get('usage', {}).get('total_tokens', 0)
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        return result, tokens, 1, truncated
                    except json.JSONDecodeError:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, response_data.get('usage', {}).get('total_tokens', 0), 1, False
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return {}, 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_translations: {e}")
            return {}, 0, 1, False
        
        return {}, 0, self.retry_attempts, False    

    def _get_complete_analysis(self, message_content: str, 
                            previous_context: List[Dict] = None, 
                            following_context: List[Dict] = None) -> Tuple[Dict, int, int, bool]:
        """Try to get complete analysis in one API call with context using Jinja2 templating"""
        
        try:
            # Format context messages
            previous_messages_text = format_context_messages(previous_context) if previous_context else "No previous messages"
            following_messages_text = format_context_messages(following_context) if following_context else "No following messages"
            
            # Get sender info
            sender_alias = "unknown"
            chat_id = "unknown"
            
            # Find sender_alias and chat_id from previous context
            if previous_context and len(previous_context) > 0:
                last_message = previous_context[-1]
                sender_alias = last_message.get('sender_alias', 'unknown')
                chat_id = last_message.get('chat_id', 'unknown')
            
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('complete_analysis.j2')
            
            # Render the template with the variables
            prompt = template.render(
                prev_count=len(previous_context) if previous_context else 0,
                previous_messages=previous_messages_text,
                sender=sender_alias,
                chat=chat_id,
                message=message_content,
                follow_count=len(following_context) if following_context else 0,
                following_messages=following_messages_text
            )
                #ic(prompt)
            
            # The rest of the function remains unchanged
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    # Check if response is successful
                    response_data = response.json()
                    
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            time.sleep(1)  # Wait before retrying
                            continue
                        return {}, 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    total_tokens = response_data.get('usage', {}).get('total_tokens', 0)
                    
                    try:
                        # Try to extract JSON from content
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '{' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean the string - find the JSON part
                        json_str = json_str.strip()
                        if not json_str.startswith('{'):
                            start_idx = json_str.find('{')
                            if start_idx == -1:
                                raise ValueError("No JSON object found in response")
                            json_str = json_str[start_idx:]
                        if not json_str.endswith('}'):
                            end_idx = json_str.rfind('}')
                            if end_idx == -1:
                                raise ValueError("No JSON object found in response")
                            json_str = json_str[:end_idx+1]
                        
                        # Parse the JSON
                        result = json.loads(json_str)
                        
                        # Check if truncated
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        
                        return result, total_tokens, 1, truncated
                        
                    except (json.JSONDecodeError, ValueError) as e:
                        if attempt < self.retry_attempts - 1:
                            time.sleep(1)
                            continue
                        return {}, total_tokens, 1, False
                
                except Exception as e:
                    if attempt < self.retry_attempts - 1:
                        time.sleep(1)  # Wait before retrying
                        continue
                    return {}, 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_complete_analysis: {e}")
            return {}, 0, 1, False
        
        # If we reach here, all attempts failed
        return {}, 0, self.retry_attempts, False

    def _get_translations(self, message_content: str) -> Tuple[Dict, int, int, bool]:
        """Get translations for the message using Jinja2 templating"""
        try:
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('translations.j2')
            
            # Render the template
            prompt = template.render(message=message_content)
            
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    try:
                        # Extract JSON
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '{' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean the string
                        json_str = json_str.strip()
                        if not json_str.startswith('{'):
                            json_str = json_str[json_str.find('{'):]
                        if not json_str.endswith('}'):
                            json_str = json_str[:json_str.rfind('}')+1]
                        
                        result = json.loads(json_str)
                        tokens = response_data.get('usage', {}).get('total_tokens', 0)
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        return result, tokens, 1, truncated
                    except json.JSONDecodeError:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, response_data.get('usage', {}).get('total_tokens', 0), 1, False
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return {}, 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_translations: {e}")
            return {}, 0, 1, False
        
        return {}, 0, self.retry_attempts, False

    def _get_emotions(self, message_content: str) -> Tuple[List[str], int, int, bool]:
        """Get emotions expressed in the message using Jinja2 templating"""
        try:
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('emotions.j2')
            
            # Render the template
            prompt = template.render(message=message_content)
            
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return [], 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    try:
                        # Extract JSON array
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '[' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean string
                        json_str = json_str.strip()
                        if not (json_str.startswith('[') and json_str.endswith(']')):
                            if '[' in json_str and ']' in json_str:
                                json_str = json_str[json_str.find('['):json_str.rfind(']')+1]
                        
                        result = json.loads(json_str)
                        tokens = response_data.get('usage', {}).get('total_tokens', 0)
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        return result, tokens, 1, truncated
                    except json.JSONDecodeError:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return [], response_data.get('usage', {}).get('total_tokens', 0), 1, False
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return [], 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_emotions: {e}")
            return [], 0, 1, False
        
        return [], 0, self.retry_attempts, False

    def _get_technical_terms(self, message_content: str) -> Tuple[Dict, int, int, bool]:
        """Extract technical terms from the message using Jinja2 templating"""
        try:
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('technical_terms.j2')
            
            # Render the template
            prompt = template.render(message=message_content)
            
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    try:
                        # Extract JSON object
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '{' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean string
                        json_str = json_str.strip()
                        if not json_str.startswith('{'):
                            json_str = json_str[json_str.find('{'):]
                        if not json_str.endswith('}'):
                            json_str = json_str[:json_str.rfind('}')+1]
                        
                        result = json.loads(json_str)
                        tokens = response_data.get('usage', {}).get('total_tokens', 0)
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        return result, tokens, 1, truncated
                    except json.JSONDecodeError:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return {}, response_data.get('usage', {}).get('total_tokens', 0), 1, False
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return {}, 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_technical_terms: {e}")
            return {}, 0, 1, False
        
        return {}, 0, self.retry_attempts, False

    def _get_tags(self, message_content: str) -> Tuple[List[str], int, int, bool]:
        """Generate categorization tags for the message using Jinja2 templating"""
        try:
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('tags.j2')
            
            # Render the template
            prompt = template.render(message=message_content)
            
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return [], 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    
                    try:
                        # Extract JSON array
                        if '```json' in content:
                            json_str = content.split('```json')[1].split('```')[0].strip()
                        elif '```' in content and '[' in content:
                            json_str = content.split('```')[1].split('```')[0].strip()
                        else:
                            json_str = content
                        
                        # Clean string
                        json_str = json_str.strip()
                        if not (json_str.startswith('[') and json_str.endswith(']')):
                            if '[' in json_str and ']' in json_str:
                                json_str = json_str[json_str.find('['):json_str.rfind(']')+1]
                        
                        result = json.loads(json_str)
                        tokens = response_data.get('usage', {}).get('total_tokens', 0)
                        truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                        return result, tokens, 1, truncated
                    except json.JSONDecodeError:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return [], response_data.get('usage', {}).get('total_tokens', 0), 1, False
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return [], 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_tags: {e}")
            return [], 0, 1, False
        
        return [], 0, self.retry_attempts, False

    def _get_context(self, message_content: str,
                    previous_context: List[Dict] = None,
                    following_context: List[Dict] = None) -> Tuple[str, int, int, bool]:
        """Analyze context of the message within conversation flow using Jinja2 templating"""
        try:
            # Format context messages for better prompt
            previous_messages_text = format_context_messages(previous_context) if previous_context else "None"
            following_messages_text = format_context_messages(following_context) if following_context else "None"
            
            # Load the template from file
            jinja_env = create_jinja_environment()
            template = jinja_env.get_template('context.j2')
            
            # Render the template
            prompt = template.render(
                previous_messages=previous_messages_text,
                message=message_content,
                following_messages=following_messages_text
            )
            
            # API call implementation
            for attempt in range(self.retry_attempts):
                try:
                    payload = {
                        "model": "deepseek-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": self.max_tokens
                    }
                    
                    response = requests.post(
                        self.api_endpoint,
                        headers=self.headers,
                        json=payload
                    )
                    
                    response_data = response.json()
                    if 'error' in response_data:
                        if attempt < self.retry_attempts - 1:
                            continue
                        return "", 0, 1, False
                    
                    content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')
                    tokens = response_data.get('usage', {}).get('total_tokens', 0)
                    truncated = response_data.get('choices', [{}])[0].get('finish_reason') == 'length'
                    
                    # Return the content as a string
                    return content, tokens, 1, truncated
                    
                except Exception:
                    if attempt < self.retry_attempts - 1:
                        continue
                    return "", 0, 1, False
        
        except Exception as e:
            logger.error(f"Error in _get_context: {e}")
            return "", 0, 1, False
        
        return "", 0, self.retry_attempts, False



class TranslatorProcessor:
    """Process messages using the DeepSeek translator with multithreading support"""
    
    def __init__(self, translator: DeepSeekTranslator, file_manager: FileManager, 
                 metrics: MetricsTracker, workers: int = 4, batch_size: int = 10, 
                 show_api_responses: bool = True, show_skipped: bool = True):
        self.translator = translator
        self.file_manager = file_manager
        self.metrics = metrics
        self.workers = workers
        self.batch_size = batch_size
        self.show_api_responses = show_api_responses
        self.show_skipped = show_skipped
        self.progress_lock = threading.Lock()


    def process_batch_wrapper(self, batch, all_messages, thread_id):
        """
        Wrapper pour traiter un batch de messages
        
        Args:
            batch: Liste de tuples (message, index) ou de messages
            all_messages: Liste de tous les messages
            thread_id: ID du thread
        
        Returns:
            Nombre de messages traités avec succès
        """
        print(f"{Fore.CYAN}Thread {thread_id} - Traitement de {len(batch)} messages{Style.RESET_ALL}")
        processed = 0
        for message_data in batch:
            # Unpack the message and its index
            if isinstance(message_data, tuple) and len(message_data) == 2:
                message, idx = message_data
                try:
                    self.process_message(message, all_messages, idx, thread_id)
                    processed += 1
                except Exception as e:
                    print(f"{Fore.RED}Thread {thread_id} - Erreur: {e}{Style.RESET_ALL}")
            else:
                # Pour le cas où message_data n'est pas un tuple, trouver l'index du message
                try:
                    message = message_data
                    message_id = str(message.get('id', 'unknown'))
                    
                    # Chercher l'index du message dans all_messages
                    found_idx = -1
                    for idx, msg in enumerate(all_messages):
                        if str(msg.get('id', '')) == message_id:
                            found_idx = idx
                            break
                    
                    self.process_message(message, all_messages, found_idx, thread_id)
                    processed += 1
                except Exception as e:
                    print(f"{Fore.RED}Thread {thread_id} - Erreur (fallback): {e}{Style.RESET_ALL}")
        
        print(f"{Fore.GREEN}Thread {thread_id} - Fin de traitement: {processed}/{len(batch)} messages traités{Style.RESET_ALL}")
        return processed
                    
    def turbo_process(self, messages: List[Dict], processed_ids: Set[str]) -> None:
        """Process messages in parallel using ThreadPoolExecutor with context"""
        # Filter out already processed messages and keep track of indices
        to_process = []
        for idx, msg in enumerate(messages):
            if str(msg.get('id')) not in processed_ids:
                to_process.append((msg, idx))
        
        if not to_process:
            print(f"{Fore.YELLOW}Tous les messages ont déjà été traités.{Style.RESET_ALL}")
            return
        
        total_to_process = len(to_process)
        # Ici on met à jour cette variable correctement
        self.metrics.total_messages = total_to_process
        
        # Improved color formatting for TURBO mode message
        print(f"{Fore.CYAN}TURBO Processing | {Fore.GREEN}{total_to_process} messages{Style.RESET_ALL} | "
            f"{Fore.MAGENTA}workers: {self.workers}{Style.RESET_ALL} | "
            f"{Fore.YELLOW}batch size: {self.batch_size}{Style.RESET_ALL} | "
            f"{Fore.BLUE}context size: {self.translator.context_size}{Style.RESET_ALL}")

        
        # Split messages into batches - each batch contains (message, index) tuples
        batches = [to_process[i:i+self.batch_size] for i in range(0, len(to_process), self.batch_size)]
        
        print(f"{Fore.YELLOW}Traitement de {len(batches)} batchs{Style.RESET_ALL}")
        
        # Process batches with ThreadPoolExecutor
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                futures = []
                
                # Démarrer les traitements en parallèle
                for i, batch in enumerate(batches):
                    # Use self.process_batch_wrapper instead of process_batch_wrapper
                    futures.append(executor.submit(self.process_batch_wrapper, batch, messages, i))
                
                # Wait for all futures to complete with timeout
                print(f"{Fore.YELLOW}Timeout : 600s")
                done, not_done = concurrent.futures.wait(futures, timeout=600)
                
                if not_done:
                    print(f"{Fore.RED}{len(not_done)} futures n'ont pas terminé dans le délai imparti{Style.RESET_ALL}")
                
                # Vérifier les résultats
                total_processed = 0
                for future in done:
                    try:
                        result = future.result()
                        total_processed += result
                        print(f"{Fore.GREEN}Future terminée: {result} messages traités{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Erreur dans une future: {e}{Style.RESET_ALL}")
                
                print(f"{Fore.CYAN}Total des messages traités par les futures: {total_processed}{Style.RESET_ALL}")
        
        except Exception as e:
            print(f"{Fore.RED}Erreur critique dans turbo_process: {e}{Style.RESET_ALL}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Print final statistics
            self.print_final_stats()

    def process_message(self, message: Dict, all_messages: List[Dict], message_idx: int, thread_id: int) -> None:
        """Process a single message with context awareness"""
        try:
            start_time = time.time()
            message_id = str(message.get('id', 'unknown'))
            
            # Get context messages
            previous_context, following_context = prepare_context(
                all_messages, message_idx, self.translator.context_size
            )
            
            # Process the message with context
            result, tokens, api_calls, success = self.translator.translate_message(
                message, previous_context, following_context
            )
            
            processing_time = time.time() - start_time
            
            if success:
                # Save results
                self.file_manager.append_result(result, tokens, api_calls)
                # Update metrics
                self.metrics.update(thread_id, True, tokens, processing_time, api_calls)
                print(f"[{Fore.GREEN}THN{Style.RESET_ALL}] {thread_id} Processed {message_id} in {processing_time:.2f}s")
            elif result.get('status') == 'skipped':
                if self.show_skipped:
                    print(f"[{Fore.YELLOW}T{thread_id}{Style.RESET_ALL}] Skipped {message_id}: already processed")
            else:
                # Handle failed processing
                self.metrics.update(thread_id, False, tokens, processing_time, api_calls)
                error_msg = result.get('deepseek', {}).get('error', 'Unknown error')
                self.file_manager.log_error(message_id, error_msg)
                print(f"[{Fore.RED}T{thread_id}{Style.RESET_ALL}] Failed {message_id}: {error_msg}")
                
        except Exception as e:
            # Handle exceptions
            processing_time = time.time() - start_time
            self.metrics.update(thread_id, False, 0, processing_time)
            self.file_manager.log_error(message_id, str(e))
            print(f"[{Fore.RED}T{thread_id}{Style.RESET_ALL}] Exception {message_id}: {str(e)}")


    def print_final_stats(self):
        """Print final processing statistics"""
        stats = self.metrics.get_stats()
        elapsed_time = stats["elapsed_time"]
        
        # Format elapsed time
        hours, remainder = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        elapsed_str = f"{hours}h {minutes}m {seconds}s"
        
        # Calculer les métriques additionnelles
        tokens = stats["total_tokens"]
        tokens_per_second = tokens / elapsed_time if elapsed_time > 0 else 0
        eur_per_hour = (tokens_per_second * 3600) / 2297790 if tokens_per_second > 0 else 0
        
        # Calculer le total réel des messages traités
        total_processed = stats['successful_messages'] + stats['failed_messages']
        
        # Print colored summary
        print("\n" + "="*80)
        print(f"{Fore.GREEN}📊 STATISTIQUES FINALES 📊{Style.RESET_ALL}")
        print(f"✅ Taux de succès: {Fore.YELLOW}{stats['success_rate']:.2f}%{Style.RESET_ALL}")
        print(f"📝 Messages: {Fore.GREEN}{stats['successful_messages']}{Style.RESET_ALL} réussis / "
            f"{Fore.RED}{stats['failed_messages']}{Style.RESET_ALL} échoués / "
            f"{Fore.BLUE}{total_processed}{Style.RESET_ALL} traités sur {stats['total_messages']} total")
        print(f"💰 Tokens: {Fore.CYAN}{tokens}{Style.RESET_ALL} ({Fore.MAGENTA}{tokens_per_second:.2f}{Style.RESET_ALL} tokens/sec)")
        print(f"💶 Coût: {Fore.GREEN}{tokens / 2297790:.6f}{Style.RESET_ALL} EUR ({Fore.YELLOW}{eur_per_hour:.6f}{Style.RESET_ALL} EUR/h)")
        print(f"⏱️ Temps total: {Fore.BLUE}{elapsed_str}{Style.RESET_ALL}")
        print(f"🚀 Vitesse: {Fore.RED}{stats['avg_processing_time']:.2f}{Style.RESET_ALL} sec/msg | "
            f"{Fore.CYAN}{stats['messages_per_second']:.2f}{Style.RESET_ALL} msg/sec")
        print("="*80)
        
        # Save stats to file
        try:
            self.file_manager.save_stats(stats)
        except Exception as e:
            print(f"{Fore.RED}Erreur lors de la sauvegarde des statistiques: {e}{Style.RESET_ALL}")

########
# MAIN #
########
def main():
    """Main entry point for the translator"""
    # Parse arguments
    args = parse_arguments()
    
    # Apply dirty_fix immediately
    #dirty_fix()
    
    # Initialize colorama
    colorama.init()
    
    # Display banner
    display_banner()
    
    # Process files
    file_manager = process_files(args)
    
    # Ensure file_manager has save_final_results method (additional safeguard)
    if not hasattr(file_manager, 'save_final_results'):
        from types import MethodType
        
        def save_final_results_fixed(self, silent: bool = False):
            """
            Emergency save function
            """
            try:
                if not silent:
                    print(f"\n{Fore.CYAN}Saving {len(self.processed_results)} results to {self.output_file}{Style.RESET_ALL}")
                
                # Check output directory
                output_dir = os.path.dirname(self.output_file)
                if output_dir and not os.path.exists(output_dir):
                    os.makedirs(output_dir, exist_ok=True)
                
                # Direct write to file (simplified approach)
                with open(self.output_file, 'w', encoding='utf-8') as f:
                    if self.processed_results:
                        # Sort results by ID
                        sorted_results = sorted(
                            self.processed_results,
                            key=lambda x: str(x.get('id', ''))
                        )
                        json.dump(sorted_results, f, ensure_ascii=False, indent=2)
                    else:
                        f.write("[]")  # Write empty array
                
                if not silent:
                    print(f"{Fore.GREEN}Save successful for {len(self.processed_results)} messages{Style.RESET_ALL}")
                
                return True
            except Exception as e:
                if not silent:
                    print(f"\n{Fore.RED}Error during save: {e}{Style.RESET_ALL}")
                
                # Emergency save with different filename
                try:
                    emergency_file = f"{self.output_file}.emergency"
                    with open(emergency_file, 'w', encoding='utf-8') as f:
                        json.dump(self.processed_results, f, ensure_ascii=False, indent=2)
                    if not silent:
                        print(f"{Fore.GREEN}Emergency save successful in {emergency_file}{Style.RESET_ALL}")
                except Exception as e2:
                    if not silent:
                        print(f"{Fore.RED}Emergency save failed: {e2}{Style.RESET_ALL}")
                
                return False
        
        # Attach method to file_manager instance
        file_manager.save_final_results = MethodType(save_final_results_fixed, file_manager)
        print(f"{Fore.GREEN}Added save_final_results method to FileManager{Style.RESET_ALL}")
    
    # Load input data
    messages = file_manager.load_input_data()
    
    # Rest of the main function continues as before...
    
    # Get already processed message IDs
    processed_ids = file_manager.get_processed_ids()
    
    # Print skipped messages in red
    skipped_count = len(processed_ids)
    
    # Initialize translator with processed IDs and context size
    translator = DeepSeekTranslator(
        api_key=args.api_key,
        max_tokens=args.max_tokens,
        retry_attempts=args.retry_attempts,
        processed_ids=processed_ids,
        context_size=args.context_size
    )
    
    # Initialize metrics tracker
    metrics = MetricsTracker()
    
    # Initialize processor
    processor = TranslatorProcessor(
        translator=translator,
        file_manager=file_manager,
        metrics=metrics,
        workers=args.workers,
        batch_size=args.batch_size,
        show_api_responses=not args.no_api_responses,
        show_skipped=not args.no_skipped
    )

    # Start input listener thread - make sure it's daemon so it doesn't block program exit
    listener_thread = threading.Thread(target=input_listener, args=(processor,), daemon=True)
    listener_thread.start()
    
    # Start price update thread but don't display
    price_thread = threading.Thread(target=display_price, args=(metrics, 2297790), daemon=True)
    price_thread.start()
    
    # Filter out already processed messages
    to_process = [msg for msg in messages if str(msg.get('id')) not in processed_ids]
    total_messages = len(to_process)
    metrics.total_messages = total_messages
    
    # Process messages
    processor.turbo_process(messages, processed_ids)
    
    # Save final sorted results
    try:
        file_manager.save_final_results()
    except Exception as e:
        print(f"{Fore.RED}Erreur lors de la sauvegarde finale: {e}{Style.RESET_ALL}")
    
    # Print final statistics
    processor.print_final_stats()
    
    print(f"{Fore.GREEN}\nTraitement terminé!{Style.RESET_ALL}")
    
    # Don't try to join the listener thread - it will continue running in the background
    # until the user exits manually or the process is terminated
    print(f"{Fore.YELLOW}Pour quitter, tapez 'exit', 'quit', ou 'q'.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Programme interrompu par l'utilisateur. Arrêt en cours...{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Erreur non gérée: {type(e).__name__}: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        sys.exit(1)