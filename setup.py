from setuptools import setup, find_packages

setup(
    name='justify-ai',
    version='1.0.0',
    description='Explainable Multilingual NLP Framework for Hate Speech Analysis',
    author='Your Name',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'nltk>=3.8',
        'spacy>=3.5',
        'gensim>=4.3',
        'fasttext>=0.9.2',
        'numpy>=1.24',
        'pandas>=2.0',
        'scikit-learn>=1.3',
        'plotly>=5.14',
        'flask>=2.3',
        'streamlit>=1.27',
        'pyyaml>=6.0',
        'pytest>=7.4',
    ]
)
