# phishing-detection-system
Overview
Phishing attacks are a major cybersecurity threat, tricking users into revealing sensitive information by mimicking legitimate websites. This project aims to develop a Phishing Detection System using a Hybrid Machine Learning Approach to analyze and classify URLs as legitimate or phishing based on various extracted features.

Features

1. Extracts key URL-based features (domain name, length, special characters, SSL status, etc.).
2. Implements Machine Learning algorithms to classify URLs.
3. Uses Hybrid ML approach (combining different models) for improved accuracy.
4. Provides a real-time detection system to identify suspicious URLs.
5. Scalable and can be extended with WHOIS, DNS, and webpage content analysis.

Technology Stack
Programming Language: Python
Machine Learning Models: Decision Trees, Random Forest, SVM, Neural Networks
Libraries Used: Scikit-learn, Pandas, NumPy, Matplotlib
Dataset: Open-source datasets from PhishTank, UCI ML Repository

How It Works?
Feature Extraction: Collect and preprocess URL-based features.
Training Machine Learning Models: Train different classifiers to detect phishing websites.
Hybrid Model Integration: Combine multiple models to improve detection accuracy.
Real-time Prediction: Use trained models to classify new URLs.
