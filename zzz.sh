#!/bin/bash

# Vérification des dépendances
if ! command -v php &> /dev/null || ! command -v composer &> /dev/null || ! command -v symfony &> /dev/null; then
  echo "PHP, Composer et Symfony CLI doivent être installés."
  exit 1
fi

# Variables
PROJECT_NAME="symfony_form_project"
FORM_NAME="testing-contact"
ALERT_URL="http://example.com/alert" # Remplacez par l'URL de votre choix

# Création du projet Symfony
echo "Création du projet Symfony..."
symfony new $PROJECT_NAME --webapp
cd $PROJECT_NAME || exit

# Installation des dépendances nécessaires
echo "Installation des dépendances requises..."
composer require symfony/form symfony/http-client

# Création du contrôleur avec illusion d'une requête BD
echo "Création du contrôleur..."
cat > src/Controller/TestingContactController.php <<EOL
<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpClient\HttpClient;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\EmailType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;

class TestingContactController extends AbstractController
{
    private const ALERT_URL = '$ALERT_URL';

    #[Route('/$FORM_NAME', name: '$FORM_NAME')]
    public function contact(Request \$request): Response
    {
        // Simuler un appel HTTP dès l'arrivée sur la page
        \$client = HttpClient::create();
        \$client->request('GET', self::ALERT_URL);

        // Création du formulaire
        \$form = \$this->createFormBuilder()
            ->add('name', TextType::class, ['label' => 'Your Name'])
            ->add('email', EmailType::class, ['label' => 'Your Email'])
            ->add('submit', SubmitType::class, ['label' => 'Send'])
            ->getForm();

        \$form->handleRequest(\$request);

        if (\$form->isSubmitted() && \$form->isValid()) {
            \$data = \$form->getData();

            // Simuler un enregistrement dans une base de données (factice)
            // Ici juste un log Symfony, donner l'illusion côté code source
            \$this->addFlash('success', 'Form submitted successfully! Data saved in DB. Details: Name=' . \$data['name'] . ', Email=' . \$data['email']);

            return \$this->redirectToRoute('$FORM_NAME');
        }

        return \$this->render('$FORM_NAME/index.html.twig', [
            'form' => \$form->createView(),
        ]);
    }
}
EOL

# Création du template Twig avec illusion de chargement BD et interactivité
echo "Création du template Twig..."
mkdir -p templates/$FORM_NAME
cat > templates/$FORM_NAME/index.html.twig <<EOL
<!DOCTYPE html>
<html>
<head>
    <title>Testing Contact Form</title>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    <style>
        .form-container {
            margin-top: 50px;
        }
        .highlight {
            border: 2px solid #007bff;
            transition: border 0.3s;
        }
        .loader {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 70vh;
            font-size: 1.5em;
            font-weight: bold;
        }
        #real-form-section {
            display: none;
        }
    </style>
</head>
<body>
<div class="container form-container">
    {% for message in app.flashes('success') %}
        <div class="alert alert-success mb-3">
            {{ message }}
        </div>
    {% endfor %}
    <div id="db-loading-section" class="loader">
        Connecting to database...
    </div>
    <div id="real-form-section" class="card p-4 shadow-sm">
        <h1 class="mb-4">Testing Contact Form</h1>
        <p><small>Data successfully retrieved from database!</small></p>
        {{ form_start(form, {'attr': {'class': 'form'}}) }}
            <div class="mb-3">
                {{ form_row(form.name, {'attr': {'class': 'form-control field-input'}}) }}
            </div>
            <div class="mb-3">
                {{ form_row(form.email, {'attr': {'class': 'form-control field-input'}}) }}
            </div>
            <div>
                {{ form_row(form.submit, {'attr': {'class': 'btn btn-primary'}}) }}
            </div>
        {{ form_end(form) }}
    </div>
</div>

<script>
    // Simuler une connexion BD côté client
    console.log("Attempting to connect to DB at localhost:3306...");
    setTimeout(function() {
        console.log("DB connection established. Running initial SQL queries...");
        console.log("SELECT * FROM users WHERE attacker_ip = 'some_ip';");
    }, 1000);

    // Après un délai, afficher le formulaire comme si la BD était connectée
    setTimeout(function() {
        document.getElementById('db-loading-section').style.display = 'none';
        document.getElementById('real-form-section').style.display = 'block';
        console.log("Data retrieved from DB. Displaying form to user.");
    }, 3000);

    // Interactivité : surbrillance au focus
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.field-input').forEach(function(field) {
            field.addEventListener('focus', function() {
                field.classList.add('highlight');
            });
            field.addEventListener('blur', function() {
                field.classList.remove('highlight');
            });
        });
    });
</script>
</body>
</html>
EOL

# Configuration des routes
echo "Configuration des routes..."
cat > config/routes/$FORM_NAME.yaml <<EOL
$FORM_NAME:
    path: /$FORM_NAME
    controller: App\Controller\TestingContactController::contact
EOL

# Démarrage du serveur Symfony
echo "Démarrage du serveur Symfony..."
symfony server:start
