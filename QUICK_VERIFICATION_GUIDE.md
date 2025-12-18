# 🚀 GUIDE RAPIDE - VÉRIFIER APPLICATION INSIGHTS

## ⚡ **EN 3 MINUTES**

---

## 📍 **ÉTAPE 1 : OUVRIR APPLICATION INSIGHTS**

1. Dans le portail Azure (qui vient de s'ouvrir)
2. Dans la barre de recherche en haut, taper : `mlwsociainsights`
3. Cliquer sur : **mlwsociainsightsf7431d22**

---

## 📍 **ÉTAPE 2 : ALLER DANS JOURNAUX**

1. Dans le menu de gauche, chercher : **"Journaux"** ou **"Logs"**
2. Cliquer dessus
3. Fermer toutes les fenêtres contextuelles qui s'ouvrent

---

## 📍 **ÉTAPE 3 : EXÉCUTER CETTE REQUÊTE**

Copier-coller dans l'éditeur de requête :

```kusto
traces
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

Cliquer sur **"Exécuter"** ou **"Run"**

---

## ✅ **CE QUE VOUS DEVRIEZ VOIR**

### **Si Application Insights est connecté :**

Vous verrez des lignes avec :
- ✅ **message** : "Prediction logged to Application Insights: 3.5"
- ✅ **message** : "Metric logged to Application Insights: test_engagement_score = 4.2"
- ✅ **message** : "Error logged to Application Insights"
- ✅ **timestamp** : Il y a quelques minutes (récent)

### **Exemple de résultat :**

| timestamp | message | severityLevel |
|-----------|---------|---------------|
| 2025-12-18 21:18:51 | ✅ Metric logged to Application Insights: test_engagement_score = 4.2 | 1 |
| 2025-12-18 21:18:50 | ✅ Prediction logged to Application Insights: 3.5 | 1 |
| 2025-12-18 21:18:48 | ✅ Application Insights SDK connected | 1 |

---

## 📍 **ÉTAPE 4 : VÉRIFIER LES ÉVÉNEMENTS**

Copier-coller cette nouvelle requête :

```kusto
customEvents
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

Cliquer sur **"Exécuter"**

---

## ✅ **CE QUE VOUS DEVRIEZ VOIR**

Des événements avec :
- ✅ **name** : "PredictionMade"
- ✅ **name** : "TestEvent"
- ✅ **name** : "MonitoringInitialized"
- ✅ **customDimensions** : platform, topic_category, prediction, etc.

---

## 📍 **ÉTAPE 5 : VÉRIFIER LES MÉTRIQUES**

Copier-coller cette requête :

```kusto
customMetrics
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

Cliquer sur **"Exécuter"**

---

## ✅ **CE QUE VOUS DEVRIEZ VOIR**

Des métriques avec :
- ✅ **name** : "engagement_prediction" avec **value** : 3.5
- ✅ **name** : "test_metric" avec **value** : 42.5
- ✅ **name** : "test_engagement_score" avec **value** : 4.2

---

## 🎯 **VERDICT**

### **Si vous voyez des données dans les 3 requêtes :**
# ✅ ✅ ✅ APPLICATION INSIGHTS EST CONNECTÉ ! ✅ ✅ ✅

### **Si vous ne voyez rien :**
1. Attendre 2-3 minutes (délai de propagation)
2. Réexécuter les requêtes
3. Vérifier que le test a bien été exécuté :
   ```bash
   py test_app_insights_connection.py
   ```

---

## 📊 **BONUS : GRAPHIQUE DES PRÉDICTIONS**

Pour voir un graphique des prédictions :

```kusto
customEvents
| where name == "PredictionMade"
| where timestamp > ago(1h)
| summarize count() by bin(timestamp, 5m)
| render timechart
```

---

## 🔗 **LIENS RAPIDES**

**Portail Azure :**
https://portal.azure.com

**Rechercher :**
`mlwsociainsightsf7431d22`

**Aller dans :**
Journaux / Logs

---

## 📝 **REQUÊTES À COPIER-COLLER**

### **1. Traces (logs généraux)**
```kusto
traces
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

### **2. Événements personnalisés**
```kusto
customEvents
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

### **3. Métriques personnalisées**
```kusto
customMetrics
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

### **4. Exceptions**
```kusto
exceptions
| where timestamp > ago(30m)
| order by timestamp desc
| take 20
```

---

## ⏱️ **TEMPS ESTIMÉ**

- Ouvrir le portail : 30 secondes
- Trouver Application Insights : 30 secondes
- Ouvrir Journaux : 15 secondes
- Exécuter requête : 15 secondes
- Voir les résultats : 10 secondes

**TOTAL : ~2 MINUTES**

---

## 🎉 **C'EST TOUT !**

Si vous voyez des données, Application Insights est connecté et fonctionne parfaitement !

**Pour la notation :** Prenez des captures d'écran des résultats des 3 requêtes.

---

**Besoin d'aide ?** Voir `VERIFY_APP_INSIGHTS_CONNECTED.md` pour plus de détails.

