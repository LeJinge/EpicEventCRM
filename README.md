# EpicEvents CRM

## Description

Ce CRM en ligne de commande permet aux utilisateurs de gérer leur clientèle, les contrats et les évènements directement 
depuis le terminal, offrant des fonctionnalités telles que l'ajout, 
la suppression, et la consultation de données client.

## Prérequis

- Python 3.11 ou supérieur
- [Poetry](https://python-poetry.org/docs/#installation) pour la gestion des dépendances 
et de l'environnement virtuel.

## Installation

### 1. Clonage du répertoire

Commencez par cloner le dépôt où se trouve le projet :
```bash
git clone https://your-repository-url.git
cd chemin-vers-le-dossier-du-projet
```

## 2. Configuration de l'environnement virtuel 

### Poetry
Poetry crée et gère automatiquement un environnement virtuel pour votre projet. 
Assurez-vous que Poetry est installé, puis configurez l'environnement et installez les dépendances :

```bash
poetry install
```

### Pip
Option alternative avec requirements.txt.
Si vous préférez ne pas utiliser Poetry, assurez-vous d'avoir Python et pip installés, puis utilisez 
requirements.txt pour installer les dépendances :

```bash
python -m venv env
``` 
#### Pour activer l'environnement virtuel :
```bash
source env/bin/activate  # Pour Unix ou MacOS
env\\Scripts\\activate     # Pour Windows
```
#### Pour installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Lancement du programme

Pour lancer le programme, exécutez le fichier main.py :

```bash
python main.py
```

### Variables d'environnement

Pour configurer correctement votre application, vous devrez définir certaines variables d'environnement. 
Ces variables sont généralement stockées dans un fichier `config.yaml` à la racine de votre projet.
L'utilisation de variables d'environnement est une bonne pratique pour stocker des informations sensibles et ne pas les
exposer dans le code source.

#### Sentry

```yaml
SENTRY_API_KEY: "YOUR_SENTRY_API_KEY"
```

#### Configuration de la base de données

```yaml
USERNAME: "YOUR_DATABASE_USERNAME"
HOSTNAME: "YOUR_DATABASE_HOSTNAME"
DATABASE_NAME: "YOUR_DATABASE_NAME"
PASSWORD: "YOUR_DATABASE_PASSWORD"
```