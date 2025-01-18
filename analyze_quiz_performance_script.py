import json
import pandas as pd

file_paths = [
    r"quiz endpoint.json",
    r"quiz submission data.json",
    r"api endpoint.json"
]

# Function to read JSON files
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to convert JSON data to DataFrame
def json_to_dataframe(json_data):
    return pd.json_normalize(json_data)

dataframes = []
for path in file_paths:
    data = read_json(path)
    df = json_to_dataframe(data)
    dataframes.append(df)

# Combining all DataFrames into one
data = pd.concat(dataframes, ignore_index=True)

print("Combined DataFrame:")
print(data)

columns_to_keep = [
    "quiz.id", "quiz.title", "quiz.topic", "quiz.time", "quiz.created_at", "quiz.duration", "quiz.negative_marks", "quiz.correct_answer_marks",
    "score", "accuracy", "final_score", "correct_answers", "incorrect_answers",
]
df = data[columns_to_keep]

df = df.bfill()

import re

# Function to remove parentheses and numbers
def remove_parentheses_numbers(text):
    return re.sub(r'\s*\(.*?\)\s*', '', text)

df['quiz.title'] = df['quiz.title'].apply(remove_parentheses_numbers)

# Function to split datetime into date and time
def split_datetime(column):
    df[f'{column}_date'] = pd.to_datetime(df[column]).dt.date
    df[f'{column}_time'] = pd.to_datetime(df[column]).dt.time

split_datetime('quiz.time')
split_datetime('quiz.created_at')

df = df.drop(columns=['quiz.time', 'quiz.created_at','quiz.time_time','quiz.created_at_time'])

df['accuracy'] = df['accuracy'].str.replace('%', '').astype(float)

df['quiz.time_date'] = pd.to_datetime(df['quiz.time_date'])
df['quiz.created_at_date'] = pd.to_datetime(df['quiz.created_at_date'])

df['quiz.negative_marks'] = df['quiz.negative_marks'].astype('float64')
df['quiz.correct_answer_marks'] = df['quiz.correct_answer_marks'].astype('float64')
df['final_score'] = df['final_score'].astype('float64')
print(df.dtypes)

import numpy as np
import matplotlib.pyplot as plt

# Performance by Topics
performance_by_topic = df.groupby('quiz.topic')['score'].mean()
print("Performance by Topics:\n", performance_by_topic)

# Difficulty Levels
difficulty_levels = df.groupby('quiz.duration')['score'].mean()
print("\nDifficulty Levels:\n", difficulty_levels)

# Response Accuracy
response_accuracy = df.groupby('quiz.title')['accuracy'].mean()
print("\nResponse Accuracy:\n", response_accuracy)

# Insights
weak_areas = df[df['score'] < 50]
print("\nWeak Areas:\n", weak_areas[['quiz.title', 'score', 'accuracy']])

improvement_trends = df.groupby('quiz.time_date')['score'].mean()
print("\nImprovement Trends:\n", improvement_trends)

performance_gaps = df[df['accuracy'] < 50]
print("\nPerformance Gaps:\n", performance_gaps[['quiz.title', 'score', 'accuracy']])

# Visualizations
plt.figure(figsize=(10, 6))
performance_by_topic.plot(kind='bar', title='Performance by Topics')
plt.xlabel('Quiz Topic')
plt.ylabel('Average Score')
plt.show()

plt.figure(figsize=(10, 6))
difficulty_levels.plot(kind='line', title='Difficulty Levels')
plt.xlabel('Quiz Duration')
plt.ylabel('Average Score')
plt.show()

plt.figure(figsize=(10, 6))
response_accuracy.plot(kind='pie', title='Response Accuracy', autopct='%1.1f%%')
plt.ylabel('')
plt.show()
