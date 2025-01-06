import os
import pandas as pd
# from transformers import pipeline
import json
import matplotlib.pyplot as plt
import io
import base64


def analyze_sentiment_batch(content_list, classifier):
    results = []
    for content in content_list:
        try:
            result = classifier(content, truncation=True, max_length=512)
            results.append(result[0]['label'])
        except Exception as e:
            print(f"Error processing content: {content[:50]}... | Error: {e}")
            continue  # Skip this content and move to the next
    return results


def process_data_in_batches(input_file, classifier_model, output_file, batch_size=32):
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping sentiment analysis because it is already done.")
        return pd.read_csv(output_file)

    data = pd.read_csv(input_file)
    data = data.dropna(subset=['Content'], axis=0).copy()
    data['Content'] = data['Content'].astype(str)
    data = data[data['Content'].str.strip() != ""]  # Remove rows with whitespace-only content

    # classifier = pipeline("sentiment-analysis", model=classifier_model, truncation=True, max_length=512)

    # sentiments = []
    # for i in range(0, len(data), batch_size):
    #     batch = data['Content'][i:i + batch_size].tolist()
    #     sentiments.extend(analyze_sentiment_batch(batch, classifier))
    #
    # data['Sentiment'] = sentiments
    #
    # data.to_csv(output_file, index=False)
    # return data


def get_company_signal_with_percentages(sentiment_data, company_code):
    """
    Analyzes sentiment data for a given company and returns sentiment percentages,
    a trading signal, and a pie chart of sentiment distribution as a Base64 image.

    Parameters:
    - sentiment_data (pd.DataFrame): DataFrame containing sentiment data with columns
                                     ['Company_code', 'Sentiment'].
    - company_code (str): The code of the company to analyze.

    Returns:
    - dict or str: A dictionary with sentiment percentages, signal, and pie chart image
                   if data is found; otherwise, an error message string.
    """
    # Filter data for the specified company
    company_data = sentiment_data[sentiment_data['Company_code'] == company_code]

    if company_data.empty:
        return {"error":f"No data found for company code: {company_code}"}

    # Extract the 'Sentiment' column
    sentiments = company_data['Sentiment']

    # Count occurrences of each sentiment
    counts = sentiments.value_counts()
    positive = counts.get("Positive", 0)
    negative = counts.get("Negative", 0)
    neutral = counts.get("Neutral", 0)
    total = sentiments.size

    # If there are no sentiments, return a message
    if total == 0:
        return f"No sentiment data available for company code: {company_code}"

    # Calculate percentages
    positive_percentage = (positive / total) * 100
    negative_percentage = (negative / total) * 100
    neutral_percentage = (neutral / total) * 100

    # Determine trading signal
    if positive_percentage > 60:
        signal = "BUY"
    elif negative_percentage > 60:
        signal = "SELL"
    else:
        signal = "HOLD"

    # Prepare data for pie chart
    labels = ['Позитивни', 'Негативни', 'Неутрални']
    sizes = [positive_percentage, negative_percentage, neutral_percentage]
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']   # Green, Red, Grey

    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct='%1.1f%%',
        startangle=140,
        textprops=dict(color="w")
    )

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Create a legend
    ax.legend(wedges, labels, title="Знаци", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # Save the plot to a BytesIO object
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    img_buffer.seek(0)

    # Encode the image to Base64
    img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')


    # Prepare the result dictionary
    result = {
        "company": company_code,
        "positive Percentage": round(positive_percentage, 2),
        "negative Percentage": round(negative_percentage, 2),
        "neutral Percentage": round(neutral_percentage, 2),
        "signal": signal,
        "image": img_base64,
        "image2": create_bar_plot(positive,negative,neutral),
    }
    return result

def create_bar_plot(positive, negative, neutral):
    sentiments = ['Позитивни', 'Негативни', 'Неутрални']
    values = [positive, negative, neutral]
    colors = ['#2ecc71', '#e74c3c', '#95a5a6']  # Green, Red, Grey

    # Create a bar plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(sentiments, values, color=colors)

    # Add labels and title
    ax.set_ylabel('Вкупно', fontsize=12)

    # Add grid for better readability
    ax.grid(True, linestyle='--', alpha=0.7, axis='y')

    # Add values on top of bars
    for i, value in enumerate(values):
        ax.text(i, value + 0.5, str(value), ha='center', fontsize=12)

    # Adjust layout
    plt.tight_layout()

    # Save the bar plot to a BytesIO object
    bar_buffer = io.BytesIO()
    plt.savefig(bar_buffer, format='png', bbox_inches='tight')
    plt.close(fig)  # Close the figure to free memory
    bar_buffer.seek(0)

    # Encode the bar plot image to Base64
    bar_img_base64 = base64.b64encode(bar_buffer.read()).decode('utf-8')

    return bar_img_base64

def get_fundamental_analysis(company_code):
    """
        Function to perform fundamental analysis based on sentiment analysis of company news.

        Args:
            company_code (str): The code of the company to analyze.

        Returns:
            dict: A dictionary containing sentiment percentages (positive, negative, neutral) and the resulting signal (Buy, Sell, or Hold) for the company.
    """
    news_data = "news_data.csv"

    news_sentiment_data = "news_sentiment_data.csv"
    classifier_model = "yiyanghkust/finbert-tone"

    sentiment_data = process_data_in_batches(news_data, classifier_model, news_sentiment_data)

    result = get_company_signal_with_percentages(sentiment_data, company_code)
    return result


# Example usage
if __name__ == "__main__":
    print(get_fundamental_analysis("ALK"))