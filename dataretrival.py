import streamlit as st
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

# Function for Heaps' Law
def heaps_law(num_tokens, k=44, b=0.49):
    vocab_size = k * (num_tokens ** b)
    return int(vocab_size)

# Function for Zipf's Law
def zipfs_law(word_counts, rank, s=1):
    highest_freq = max(word_counts.values())
    estimated_freq = highest_freq / (rank ** s)
    return estimated_freq

# Sidebar for selection
st.sidebar.title("Choose a Law to Estimate")
law_choice = st.sidebar.selectbox("Select the law to display:", ("Introduction", "Heaps' Law", "Zipf's Law"))

# Main Screen Content
if law_choice == "Introduction":
    st.title("Welcome to Heaps' Law and Zipf's Law Estimator")
    st.write("""
        This application allows you to explore two fundamental laws in Information Retrieval:
        
        **1. Heaps' Law**: Estimates the growth of vocabulary size as the number of tokens increases in a document collection.
        
        **2. Zipf's Law**: Describes the distribution of word frequencies in natural language, where a few words are very common, and many are rare.
        
        Use the sidebar to select a law and input the necessary parameters to see the estimated results.
    """)

elif law_choice == "Heaps' Law":
    st.title("Heaps' Law Estimator")
    num_tokens = st.number_input("Enter the total number of tokens:", min_value=1, value=1000000)
    k = st.number_input("Enter Heaps' Law constant (k):", min_value=0.1, value=44.0, step=0.1)
    b = st.number_input("Enter Heaps' Law exponent (b):", min_value=0.1, value=0.49, step=0.01)
    
    if st.button("Calculate Heaps' Law"):
        vocab_size = heaps_law(num_tokens, k, b)
        st.write(f"**Estimated Vocabulary Size (Heaps' Law):** {vocab_size}")

elif law_choice == "Zipf's Law":
    st.title("Zipf's Law Estimator")
    text = st.text_area("Enter the text for Zipf's Law calculation:", "This is an Example example Text text text")
    rank = st.number_input("Enter the rank of the word:", min_value=1, value=2)
    s = st.number_input("Enter Zipf's Law exponent (s):", min_value=0.1, value=1.0, step=0.1)
    
    # Convert text to lowercase and calculate word frequencies
    word_counts = Counter(text.lower().split())
    
    # Prepare data for the table
    freq_data = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    words = [item[0] for item in freq_data]
    frequencies = [item[1] for item in freq_data]
    ranks = list(range(1, len(words) + 1))
    
    # Create a DataFrame for display as a table
    df = pd.DataFrame({
        "Words": words,
        "Frequency (f)": frequencies,
        "Rank (r)": ranks
    })
    
    # Display the table
    st.subheader("Word Frequency Table")
    st.table(df)
    
    if st.button("Calculate Zipf's Law"):
        estimated_freq = zipfs_law(word_counts, rank, s)
        st.write(f"**Estimated Frequency for Rank {rank} (Zipf's Law):** {estimated_freq}")

    # Plot word frequency distribution
    st.subheader("Zipf's Law Frequency Distribution")
    plt.figure(figsize=(10, 6))
    plt.plot(ranks, frequencies, marker='o', linestyle='-', color='b', label="Actual Frequency")
    plt.xlabel("Rank (r)")
    plt.ylabel("Frequency (f)")
    plt.title("Word Frequency Distribution (Zipf's Law)")
    plt.yscale("log")
    plt.xscale("log")
    plt.legend()
    st.pyplot(plt)
