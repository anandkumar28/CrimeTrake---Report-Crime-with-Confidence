"""
Crime Classification using Machine Learning
Uses NLP and sklearn to classify crime descriptions
"""
import pickle
import os
from django.conf import settings

# Simple keyword-based classifier (will be replaced with trained model)
CRIME_KEYWORDS = {
    'THEFT': ['steal', 'stole', 'stolen', 'theft', 'robbed', 'took', 'shoplifting', 'burglary'],
    'ROBBERY': ['robbery', 'robbed', 'gunpoint', 'knifepoint', 'armed', 'mugging'],
    'ASSAULT': ['assault', 'attacked', 'hit', 'beaten', 'fight', 'violence', 'punch', 'kick'],
    'MURDER': ['murder', 'killed', 'death', 'homicide', 'dead', 'shot dead'],
    'KIDNAPPING': ['kidnap', 'abduct', 'hostage', 'missing', 'taken away'],
    'CYBERCRIME': ['hack', 'phishing', 'scam', 'fraud online', 'cyber', 'online fraud', 'password'],
    'FRAUD': ['fraud', 'scam', 'fake', 'counterfeit', 'forgery', 'embezzlement', 'cheating'],
    'VANDALISM': ['vandalism', 'graffiti', 'damaged', 'destroyed', 'defaced', 'broke'],
    'DOMESTIC_VIOLENCE': ['domestic', 'spouse', 'partner', 'family violence', 'husband', 'wife'],
    'DRUG_OFFENSE': ['drug', 'narcotics', 'marijuana', 'cocaine', 'heroin', 'substance'],
}


def classify_crime(description):
    """
    Classify crime based on description
    
    Args:
        description (str): Crime description text
    
    Returns:
        tuple: (predicted_category, confidence_score)
    """
    if not description:
        return 'OTHER', 0.0
    
    description_lower = description.lower()
    
    # Count keyword matches for each category
    scores = {}
    for crime_type, keywords in CRIME_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in description_lower)
        if score > 0:
            scores[crime_type] = score
    
    if not scores:
        return 'OTHER', 0.0
    
    # Get category with highest score
    predicted_category = max(scores, key=scores.get)
    max_score = scores[predicted_category]
    
    # Calculate confidence (simple heuristic)
    confidence = min(max_score / 5.0, 1.0)  # Normalize to 0-1
    
    return predicted_category, confidence


def train_model(training_data=None):
    """
    Train ML model for crime classification
    This is a placeholder for actual ML training
    
    In production, you would:
    1. Collect labeled crime reports
    2. Use TfidfVectorizer for text features
    3. Train with Naive Bayes or Logistic Regression
    4. Save model with pickle
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.model_selection import train_test_split
        
        # Sample training data (replace with real data)
        if training_data is None:
            training_data = [
                ("Someone stole my bike from the parking lot", "THEFT"),
                ("My wallet was taken at gunpoint", "ROBBERY"),
                ("I was attacked and beaten up", "ASSAULT"),
                ("Received a phishing email asking for password", "CYBERCRIME"),
                ("Found graffiti on my property", "VANDALISM"),
            ]
        
        texts, labels = zip(*training_data)
        
        # Create TF-IDF features
        vectorizer = TfidfVectorizer(max_features=1000)
        X = vectorizer.fit_transform(texts)
        
        # Train classifier
        classifier = MultinomialNB()
        classifier.fit(X, labels)
        
        # Save model
        model_path = settings.ML_MODEL_PATH / 'crime_classifier.pkl'
        vectorizer_path = settings.ML_MODEL_PATH / 'vectorizer.pkl'
        
        os.makedirs(settings.ML_MODEL_PATH, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(classifier, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(vectorizer, f)
        
        print("Model trained and saved successfully!")
        
    except ImportError:
        print("sklearn not installed. Using keyword-based classification.")
    except Exception as e:
        print(f"Error training model: {e}")


def load_trained_model():
    """
    Load trained ML model if exists
    
    Returns:
        tuple: (classifier, vectorizer) or (None, None)
    """
    try:
        model_path = settings.ML_MODEL_PATH / 'crime_classifier.pkl'
        vectorizer_path = settings.ML_MODEL_PATH / 'vectorizer.pkl'
        
        if os.path.exists(model_path) and os.path.exists(vectorizer_path):
            with open(model_path, 'rb') as f:
                classifier = pickle.load(f)
            
            with open(vectorizer_path, 'rb') as f:
                vectorizer = pickle.load(f)
            
            return classifier, vectorizer
        
    except Exception as e:
        print(f"Error loading model: {e}")
    
    return None, None


def classify_with_ml(description):
    """
    Classify using trained ML model
    
    Args:
        description (str): Crime description
    
    Returns:
        tuple: (predicted_category, confidence_score)
    """
    classifier, vectorizer = load_trained_model()
    
    if classifier and vectorizer:
        try:
            # Transform text
            X = vectorizer.transform([description])
            
            # Predict
            prediction = classifier.predict(X)[0]
            probabilities = classifier.predict_proba(X)[0]
            confidence = max(probabilities)
            
            return prediction, confidence
        
        except Exception as e:
            print(f"ML prediction error: {e}")
            return classify_crime(description)  # Fallback to keyword-based
    
    # Use keyword-based if model not available
    return classify_crime(description)
