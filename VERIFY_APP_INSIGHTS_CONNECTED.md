# ✅ VÉRIFIER QUE APPLICATION INSIGHTS EST CONNECTÉ

## 🎉 Application Insights est maintenant connecté à votre application !

---

## 📊 **COMMENT VÉRIFIER DANS LE PORTAIL AZURE**

### **ÉTAPE 1 : Ouvrir Application Insights**

1. Aller sur : **https://portal.azure.com**
2. Rechercher : `mlwsociainsightsf7431d22`
3. Cliquer sur la ressource

---

### **ÉTAPE 2 : Vérifier les Journaux (Logs)**

1. Dans le menu de gauche, cliquer sur : **"Journaux"**
2. Fermer toutes les fenêtres contextuelles
3. Coller cette requête dans l'éditeur :

```kusto
traces
| where timestamp > ago(10m)
| order by timestamp desc
| take 20
```

4. Cliquer sur **"Exécuter"**

**✅ VOUS DEVRIEZ VOIR :**
- Des traces avec le message "Prediction logged to Application Insights"
- Des traces avec "Metric logged to Application Insights"
- Des traces avec "Error logged to Application Insights"
- Timestamp récent (il y a quelques minutes)

---

### **ÉTAPE 3 : Vérifier les Événements Personnalisés**

1. Dans l'éditeur de requête, coller :

```kusto
customEvents
| where timestamp > ago(10m)
| order by timestamp desc
| take 20
```

2. Cliquer sur **"Exécuter"**

**✅ VOUS DEVRIEZ VOIR :**
- Événement : `MonitoringInitialized`
- Événement : `TestEvent`
- Événement : `PredictionMade`
- Propriétés avec les détails (platform, topic_category, etc.)

---

### **ÉTAPE 4 : Vérifier les Métriques Personnalisées**

1. Dans l'éditeur de requête, coller :

```kusto
customMetrics
| where timestamp > ago(10m)
| order by timestamp desc
| take 20
```

2. Cliquer sur **"Exécuter"**

**✅ VOUS DEVRIEZ VOIR :**
- Métrique : `test_metric` avec valeur 42.5
- Métrique : `engagement_prediction` avec valeur 3.5
- Métrique : `test_engagement_score` avec valeur 4.2

---

### **ÉTAPE 5 : Vérifier les Exceptions**

1. Dans l'éditeur de requête, coller :

```kusto
exceptions
| where timestamp > ago(10m)
| order by timestamp desc
| take 20
```

2. Cliquer sur **"Exécuter"**

**✅ VOUS DEVRIEZ VOIR :**
- Exception avec le message "This is a test error"

---

## 🧪 **TESTER AVEC L'APPLICATION EN DIRECT**

### **Option 1 : Tester localement**

1. Ouvrir un terminal
2. Exécuter :
```bash
py test_app_insights_connection.py
```

3. Attendre 2-3 minutes
4. Aller dans Application Insights → Journaux
5. Exécuter les requêtes ci-dessus

**✅ Vous devriez voir les nouvelles données**

---

### **Option 2 : Tester avec l'app Streamlit**

1. Aller sur : https://social-media-engagement-predictor-hydra00712.streamlit.app/
2. Remplir le formulaire
3. Cliquer sur "Predict"
4. Attendre 2-3 minutes
5. Aller dans Application Insights → Journaux
6. Exécuter cette requête :

```kusto
customEvents
| where name == "PredictionMade"
| where timestamp > ago(30m)
| order by timestamp desc
```

**✅ Vous devriez voir votre prédiction**

---

## 📊 **REQUÊTES UTILES**

### **Voir toutes les prédictions des dernières 24h**
```kusto
customEvents
| where name == "PredictionMade"
| where timestamp > ago(24h)
| summarize count() by bin(timestamp, 1h)
| render timechart
```

### **Voir les métriques d'engagement**
```kusto
customMetrics
| where name == "engagement_prediction"
| where timestamp > ago(24h)
| summarize avg(value), min(value), max(value)
```

### **Voir toutes les erreurs**
```kusto
exceptions
| where timestamp > ago(24h)
| order by timestamp desc
```

### **Voir l'activité par plateforme**
```kusto
customEvents
| where name == "PredictionMade"
| where timestamp > ago(24h)
| extend platform = tostring(customDimensions.platform)
| summarize count() by platform
| render piechart
```

---

## ✅ **PREUVE QUE C'EST CONNECTÉ**

### **Ce qui a été fait :**

1. ✅ Ajout du SDK Application Insights dans `azure_monitoring.py`
2. ✅ Configuration de TelemetryClient avec votre clé d'instrumentation
3. ✅ Envoi d'événements personnalisés (PredictionMade, etc.)
4. ✅ Envoi de métriques personnalisées (engagement_prediction)
5. ✅ Envoi de traces pour le logging détaillé
6. ✅ Envoi d'exceptions pour le suivi des erreurs
7. ✅ Test réussi avec `test_app_insights_connection.py`

### **Ce qui est envoyé à Application Insights :**

**Quand une prédiction est faite :**
- ✅ Événement personnalisé : `PredictionMade`
- ✅ Métrique personnalisée : `engagement_prediction`
- ✅ Trace : "Prediction made: X.XX"
- ✅ Propriétés : platform, topic_category, confidence, timestamp

**Quand une erreur se produit :**
- ✅ Exception avec détails
- ✅ Trace avec niveau ERROR
- ✅ Contexte de l'erreur

**Quand une métrique est loggée :**
- ✅ Métrique personnalisée avec nom et valeur
- ✅ Tags/propriétés associés

---

## 🎯 **POUR LA NOTATION**

### **Preuve que Application Insights fonctionne :**

**Capture d'écran 1 : Journaux avec traces**
- Montrer la requête `traces` avec résultats

**Capture d'écran 2 : Événements personnalisés**
- Montrer la requête `customEvents` avec PredictionMade

**Capture d'écran 3 : Métriques personnalisées**
- Montrer la requête `customMetrics` avec engagement_prediction

**Capture d'écran 4 : Vue d'ensemble**
- Montrer les graphiques dans la page Overview

---

## 🚀 **DÉPLOYER SUR STREAMLIT CLOUD**

Pour que l'app déployée envoie aussi des données :

1. Les changements sont déjà dans le code
2. Commit et push vers GitHub :
```bash
git add azure_monitoring.py
git commit -m "Add Application Insights SDK integration"
git push
```

3. Streamlit Cloud redéploiera automatiquement
4. L'app commencera à envoyer des données à Application Insights

---

## ⚠️ **NOTE IMPORTANTE**

**"Métriques en direct" (Live Metrics) peut toujours afficher "Non disponible"**

C'est normal pour les applications Streamlit Cloud car :
- L'app dort quand inactive
- Live Metrics nécessite une connexion en temps réel
- Les données sont quand même collectées et visibles dans les Journaux

**✅ Utilisez "Journaux" (Logs) pour vérifier les données**

---

## 📝 **RÉSUMÉ**

| Fonctionnalité | Status | Preuve |
|----------------|--------|--------|
| Application Insights SDK | ✅ Installé | `applicationinsights` dans requirements.txt |
| TelemetryClient | ✅ Configuré | Clé d'instrumentation dans azure_monitoring.py |
| Événements personnalisés | ✅ Envoyés | Requête `customEvents` |
| Métriques personnalisées | ✅ Envoyées | Requête `customMetrics` |
| Traces | ✅ Envoyées | Requête `traces` |
| Exceptions | ✅ Envoyées | Requête `exceptions` |
| Test réussi | ✅ Oui | `test_app_insights_connection.py` |

**VERDICT : ✅ APPLICATION INSIGHTS EST COMPLÈTEMENT CONNECTÉ ET FONCTIONNEL**

---

**Date de connexion :** 2025-12-18  
**Testé par :** test_app_insights_connection.py  
**Status :** ✅ OPÉRATIONNEL

