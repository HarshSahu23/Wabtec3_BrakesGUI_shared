from matplotlib import pyplot as plt
import math

class Plotter:
    def plot_bar_chart(x, y, figsize=(10, 3), xlabel="Errors", ylabel="Frequency"):
        # Create a bar chart
        fig, ax = plt.subplots(figsize=figsize)
        bars = ax.bar(x, y)

        # Add bar labels
        ax.bar_label(bars, label_type='edge', padding = 4)  # 'edge' places labels at the bar's edge; use 'center' for center placement

        # Add labels and title
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title('Bar Chart with Labels')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        plt.show()

    def plot_pie_chart(labels, data, figsize=(10, 10)):
        # Calculate percentages
        total = sum(data)
        percentages = [f"{size/total*100:.1f}%" for size in data]

        # Combine labels with data and percentages
        labels_with_data = [f"{label}\n{size} ({percentage})" for label, size, percentage in zip(labels, data, percentages)]

        # Plotting a flat pie chart
        plt.figure(figsize=figsize)
        plt.pie(data, labels=None, startangle=90, counterclock=False) # Labels with indicating lines are manually added 

        for i, (dataPoint, label) in enumerate(zip(data, labels_with_data)):
            angle = 90 - (sum(data[:i]) + dataPoint / 2) / total * 360  # Calculate the angle
            x = 1.2 * math.cos(angle * math.pi / 180)
            y = 1.2 * math.sin(angle * math.pi / 180)
            plt.text(x, y, label, ha='center', va='center', fontsize=10)
            plt.plot([0, x/1.07], [0, y/1.07], linestyle='solid', linewidth=0.8)  # Line from center to text

        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is a circle.
        plt.show()