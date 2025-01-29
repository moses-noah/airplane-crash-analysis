import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Load data
def load_data():
    # Replace with your data-loading logic
    file = 'airplane_crashes_eda_cleaned.csv'
    df = pd.read_csv(file)

    return df




def question1(dataframe, events):
    fig, ax = plt.subplots(figsize=(9, 7), dpi=100)
    # Plot the line chart
    dataframe['Year'].value_counts().sort_index().plot(
        kind='line',
        color='orange',
        title='Yearly Trend of Crashes',
        ax=ax
    )
    # Add vertical lines for events
    for event in events:
        ax.axvline(x=event['date'].year, color='black', linestyle='--', linewidth=1)
        ax.text(event['date'].year, dataframe['Year'].value_counts().max(), event['description'],
                rotation=58, verticalalignment='top', fontsize=9, color='black')
    # Add labels and grid
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Crashes")
    ax.grid(alpha=0.4)
    return fig




def question2_1(dataframe):
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    # Plot the line chart
    dataframe.groupby('Year')['Passengers'].sum().plot(
        kind='line',
        color='orange',
        marker='.',
        title='Yearly Trend of Total Passengers in Air Travel Since 1945',
        ax=ax
    )
    # Add labels
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Passengers Aboard")
    ax.grid(linestyle='--', alpha=0.7) 
    return fig





# Function to plot crash trend since 1945
def question2_2(dataframe):
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    # Plot the line chart
    dataframe[dataframe['Year'] >= 1945]['Year'].value_counts().sort_index().plot(
        kind='line',
        color='orange',
        marker='.',
        title='Yearly Trend of Crashes Since 1945',
        ax=ax
    )
    # Add labels
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Crash Incidents")
    ax.grid(linestyle='--', alpha=0.7) 
    return fig




def question2_3(dataframe):
    # Compute the correlation matrix
    correlation_matrix = dataframe.corr()
    # Create the heatmap
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    # Add title
    ax.set_title("Correlation Heatmap: \n Passenger Volume vs Crash Incidents (Since 1945)", fontsize=10)
    return fig




def question3_1(dataframe, line):
    fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
    # Plot the line chart
    dataframe.groupby('Year')[['Ground', 'Fatalities (air)']].sum().plot(
        kind='line',
        title='Yearly Trend of Ground Casualties and Fatalities in the air',
        ax=ax
    )
    # Add vertical lines for events
    for instance in line:
        ax.axvline(x=instance['date'].year, color='black', linestyle='--', linewidth=1)
        ax.text(instance['date'].year, dataframe['Year'].value_counts().max(), instance['description'],
                rotation=45, verticalalignment='bottom', fontsize=10, color='black')
    # Add labels
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Values")
    ax.grid(linestyle='--', alpha=0.3) 
    return fig




def question4_1(dataframe, events):
    fig, ax = plt.subplots(figsize=(10, 10), dpi=100)
    # Plot the line chart
    dataframe['Year'].value_counts().sort_index().plot(
        kind='line',
        color='orange',
        title='Yearly Trend of Crashes',
        ax=ax
    )
    # Add vertical lines for events
    for event in events:
        ax.axvline(x=event['date'].year, color='black', linestyle='--', linewidth=1)
        ax.text(event['date'].year, dataframe['Year'].value_counts().max(), event['description'],
                rotation=45, verticalalignment='top', fontsize=13, color='black')
    # Add labels and grid
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of Crashes")
    ax.grid(alpha=0.4)
    return fig




def question4_2(dataframe, events):
    """
    Function to visualize the number of crashes before and after key milestones using a bar chart.
    """
    # Convert the 'Year' column to datetime if not already
    dataframe['Year'] = pd.to_datetime(dataframe['Year'], format='%Y').dt.year
    # Group the crashes by year
    data_grouped = dataframe['Year'].value_counts().sort_index()
    # Create a new DataFrame to hold before/after crash counts for each milestone
    milestone_data = []
    for event in events:
        event_year = event['date'].year
        event_description = event['description']
        # Calculate crashes before and after the milestone
        crashes_before = data_grouped[data_grouped.index < event_year].sum()
        crashes_after = data_grouped[data_grouped.index >= event_year].sum()
        milestone_data.append({
            'Milestone': event_description,
            'Crashes Before': crashes_before,
            'Crashes After': crashes_after
        })
    milestone_df = pd.DataFrame(milestone_data)
    # Plotting grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.4
    x = range(len(milestone_df))  # X-axis positions
    ax.bar(
        [pos - bar_width / 2 for pos in x],
        milestone_df['Crashes Before'],
        width=bar_width,
        color='red',
        label='Crashes Before'
    )
    ax.bar(
        [pos + bar_width / 2 for pos in x],
        milestone_df['Crashes After'],
        width=bar_width,
        color='blue',
        label='Crashes After'
    )
    # Adding labels, title, and legend
    ax.set_title('Comparison of Crashes Before and After Key Milestones', fontsize=16)
    ax.set_xlabel('Milestones', fontsize=14)
    ax.set_ylabel('Number of Crashes', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(milestone_df['Milestone'], rotation=20, ha='right', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    # Adjust layout for readability
    plt.tight_layout()
    return fig





def question5_1(dataframe):
    # Create 'Decade' column
    dataframe['Decade'] = (dataframe['Year'] // 10) * 10
    # Aggregating data by decade
    decade_data = dataframe.groupby('Decade').agg(
        total_fatalities=('Fatalities (air)', 'sum'),
        total_aboard=('Aboard', 'sum')
    ).reset_index()
    # Calculate survivors
    decade_data['total_survivors'] = decade_data['total_aboard'] - decade_data['total_fatalities']
    # Create stacked bar chart
    fig, ax = plt.subplots(figsize=(15, 6), dpi=100)
    ax.bar(decade_data['Decade'], decade_data['total_fatalities'], color='darkred', label='Fatalities', width=8)
    ax.bar(decade_data['Decade'], decade_data['total_survivors'], bottom=decade_data['total_fatalities'],
           color='green', label='Survivors', width=8)
    # Add labels, title, and grid
    ax.set_title('Fatalities vs Survivors in Airplane Crashes by Decade', fontsize=16)
    ax.set_xlabel('Decade', fontsize=14)
    ax.set_ylabel('Number of People', fontsize=14)
    ax.legend(fontsize=12)
    ax.grid(alpha=0.3)
    return fig




def question5_2(airplane_crashes_df):
    """
    Function to analyze and visualize airplane crash data by decade.
    Displays total fatalities and fatalities per aboard for each decade in a Streamlit web app.
    """
    # Creating a new column for decades
    airplane_crashes_df['Decade'] = (airplane_crashes_df['Year'] // 10) * 10
    # Aggregating data by decade
    decade_data = airplane_crashes_df.groupby('Decade').agg(
        total_fatalities=('Fatalities (air)', 'sum'),
        total_aboard=('Aboard', 'sum')
    ).reset_index()
    # Calculating fatalities per aboard for each decade
    decade_data['fatalities_per_aboard'] = (
        decade_data['total_fatalities'] / decade_data['total_aboard']
    )
    # Plotting total fatalities by decade
    fig1, ax1 = plt.subplots(figsize=(15, 6))
    ax1.bar(
        decade_data['Decade'],
        decade_data['total_fatalities'],
        color='darkred',
        width=8,
        label='Total Fatalities'
    )
    ax1.set_title('Total Fatalities in Airplane Crashes by Decade', fontsize=16)
    ax1.set_xlabel('Decade', fontsize=14)
    ax1.set_ylabel('Number of Fatalities', fontsize=14)
    ax1.set_xticks(decade_data['Decade'])
    ax1.set_xticklabels(decade_data['Decade'], rotation=0)
    ax1.grid(alpha=0.3)
    ax1.legend(fontsize=12)
    # Plotting fatalities per aboard by decade
    fig2, ax2 = plt.subplots(figsize=(15, 6))
    ax2.plot(
        decade_data['Decade'],
        decade_data['fatalities_per_aboard'],
        marker='o',
        color='blue',
        label='Fatalities per Aboard'
    )
    ax2.set_title('Proportion of Fatalities per Passengers Aboard by Decade', fontsize=16)
    ax2.set_xlabel('Decade', fontsize=14)
    ax2.set_ylabel('Fatalities per Aboard', fontsize=14)
    ax2.grid(alpha=0.3)
    ax2.legend(fontsize=12)
    "The graph below shows the total airplane crashes in each decade since the inception of air travel. Air travel saw increased crash incidents from its inception in the early 1900s but also increase in safety standards and technological advancements and evenatually after the 1970s, crash incidents trended downwards as safety standards and technological advancements became sufficient enough to counter crash incidents despite the volume of air travel passengers going up year over year (even after 1970)."
    st.pyplot(fig1)
    st.caption("Proportion of Fatalities per Passengers Aboard by Decade")
    ""
    "The chart below shows a general decline in the proportion of fatality rate over the decades, with the highest fatality rates in the early 1900s. This likely reflects the early challenges of air travel where safety measures were minimal. From the mid-20th century onward, improvements in aircraft technology, regulations, and emergency response led to a steady decline in fatalities, despite some fluctuations."
    st.pyplot(fig2)
    st.caption("Yearly Trend of Crashes Since 1945")
    "A notable drop occurs in the 2020s, reaching the lowest recorded level. This could be due to advancements in safety technology, stricter regulations, and possibly reduced air travel during the COVID-19 pandemic. The overall trend highlights significant progress in passenger safety, particularly in the last few decades."
    # Display the aggregated data as a table
    st.write("### Aggregated Data by Decade")
    "This tabel shows the raw numbers for fatlity rates over the decades."
    st.dataframe(decade_data)
    st.caption("Aggregated Data by Decade")









# Main app
def main():
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    categories = [
        "**Home Page**",
        "**Global Regulations and Safety Standards**",
        "**Air Travel Demand and Infastructure**",
        "**Trend in Airplane Crashes Over Time**"
    ]
    selected_categories = st.sidebar.radio("Choose a segment to explore:", categories)

    # Load data
    df = load_data()

    passenger_volume_data = pd.read_csv('number-airline-passengers.csv')
    passenger_volume_data.drop(columns=['Entity', 'Code'], inplace=True)

    question_1_events = [
    {"date": "1944-01-01", "description": "The Chicago Convention (1944)"},
    {"date": "1947-01-01", "description": "ICAO Formation (1947)"},
    {"date": "1960-01-01", "description": "Major Developments (1960)"},
    {"date": "1970-01-01", "description": "Technology Integration (1970)"},
    {"date": "1974-01-01", "description": "Birth of IATA Operational Safety Audit (IOSA) (1974)"}
    ]
    # Convert event dates to datetime format
    for event in question_1_events:
        event['date'] = pd.to_datetime(event['date'])

    large_aircraft_intro = [
    {"date": "1938-01-01", "description": "Douglas DC-3 (1938)"},
    {"date": "1947-01-01", "description": "Lockheed Constellation (1947)"},
    {"date": "1958-01-01", "description": "Boeing 707 (1958)"},
    {"date": "1969-01-01", "description": "Boeing 747 Jumbo Jet (1969)"},
    {"date": "1976-01-01", "description": "The Concorde (1976)"},
    {"date": "1988-01-01", "description": "Airbus A320 (1988)"},
    {"date": "2005-01-01", "description": "Airbus A380 (2005)"},
    {"date": "2010-01-01", "description": "Boeing 787 Dreamliner (2010)"}]
    # Convert event dates to datetime format
    for instance in large_aircraft_intro:
        instance['date'] = pd.to_datetime(instance['date'])

    question_4_milestones = [
    {"date": "1914-01-01", "description": "First Commercial Passenger Flight (1914)"},
    {"date": "1952-01-01", "description": "Commercial Jet Age Begins (1952)"},
    {"date": "1958-01-01", "description": "Formation of FAA in the United States (1958)"},
    {"date": "1970-01-01", "description": "Development of Advanced Navigation Systems (1970)"},
    {"date": "1990-01-01", "description": "Implementation of GPS (1990)"},
    {"date": "2001-01-01", "description": "Introduction of Enhanced Safety \n Regulations Post-9/11 (2001)"},
    {"date": "2005-01-01", "description": "Advent of Automated Safety Systems \n and Predictive Maintenance Technologies \n (2005)"}
    ]
    # Convert event dates to datetime format
    for milestone in question_4_milestones:
        milestone['date'] = pd.to_datetime(milestone['date'])

    # Render content based on the selected question
    if selected_categories == "**Home Page**":
        '# Welcome to the Airplane Crash Data Analysis Project'
        '_(There is a popular saying in the world of avaiation and it goes "__There are old pilots and bold pilots, but no old, bold pilots__". A lot is said in that simple line of words)_'
        ' '
        ' '
        ' '
        '## What This Project is About'
        'To discover the story of aviation safety through data. This project dives deep into the history of airplane crashes, tracing their evolution since the earliest days of air travel.'
  
        '## Why It Matters'
        'Every crash tells a story—not just of loss but of lessons learned. By analyzing trends and patterns, this project aims to showcase how far we’ve come in making air travel one of the safest modes of transportation today.'

        '## Goal of This Project'
        'To provide meaningful insights that highlight the factors behind crashes, improvements in safety, and what these patterns reveal about the future of aviation.'
        'In this project I have tackled five questions, these questions have been grouped into three segments (these segments are located in the sidebar). The five questions and their findings can be viewed with the selection buttons below '
        if st.button("Go to Question 1"):
            '### Question 1: How has the implementation of internantional safety standards affected airplane crash frequency'
            'To answer this question, we need to look into what the international safety standard is like in the world of aviation.'

            '''
            The core of international aviation safety is governed by ICAO (International Civil Aviation Organization), a UN specialized agency. They establish SARPs (Standards and Recommended Practices) that form the foundation for civil aviation safety worldwide.

            ##### __Key Components of ICAO Includes__:

            * __ICAO Annexes__
            * __Safety Management Systems (SMS)__
            * __Certification Standards__
            * __Regional Regulations__
            * __IATA Operational Safety Audit (IOSA)__
            * __Quality Assurance Programs__
            '''
            'Lets look at the trend of crashes from the beginning and correlate the chart with significant events that took place.'
            # Generate and display the plot
            fig1 = question1(df, question_1_events)
            st.pyplot(fig1)
            st.caption("Yearly Trend of Crashes")
            '''
            The chart depicts the yearly trend of aviation crashes from the early 20th century to 2024. key aviatKon safety milestones are marked with dashed vertical lines and labeled with their respective years:
            * __The Chicago Convention (1944)__: An agreement establishing international aviation standards, likely contributing to an initial stabilization in crash rates.
            * __ICAO Formation (1947)__: Formation of the __International Civil Aviation Organization (ICAO)__.
            * __Major Developments (1960)__: Advancements in aviation technology and safety practices.
            * __Technology Integration (1970)__:  The implementation of advanced navigation and aircraft systems.
            * __Birth of IATA Operational Safety Audit (IOSA) (1974)__: A significant program to enhance operational safety in the aviation industry.
            
            The data indicates a peak in crashes around the mid-20th century, followed by a steady decline. This trend reflects improvements in technology, regulation, and global aviation safety standards. By the 2000s, crash numbers dropped significantly, showcasing the effectiveness of these safety measures.
            '''
        if st.button("Go to Question 2"):
            '## Question 2: Is there a relationship between the volume of air travel passengers and crash rates over the years'
            'First we need to see the evolution of air travel passenger volume over the years.'
            # Generate the plots
            fig2_1 = question2_1(passenger_volume_data)
            fig2_2 = question2_2(df)
            st.pyplot(fig2_1)
            st.caption("Yearly Trend of Total Passengers in Air Travel Since 1945")
            'The chart above shows that air travel passengers volume rose from practically 0 in 1945 to over 4 billion in 2019, the chart also show a steady growth in passenger volume over the years. It is worth noting the massive dip in 2020 and it can be linked to the COVID-19 pandemic that became wide spread in the same year.'
            ''
            'On the other hand, the chart below shows the trend of air crash incidents since 1945, the chart shows a down trend signifying that crash incidents has been on the decline ever since.'
            st.pyplot(fig2_2)
            st.caption("Yearly Trend of Crashes Since 1945")
            # Create a full range of years
            all_years = pd.RangeIndex(start=min(passenger_volume_data['Year']), stop=max(passenger_volume_data['Year']) + 1)
            # Reindex both Series
            passengers_aboard = passenger_volume_data.groupby('Year')['Passengers'].sum().reindex(all_years, fill_value=0)
            casualties = df[df['Year'] >= 1945]['Year'].value_counts().sort_index().reindex(all_years, fill_value=0)
            # Combine into a DataFrame
            d = pd.DataFrame({
                'Passenger Volume': passengers_aboard,
                'Crash Incidents': casualties
            })
            'The heatmap below shows the correlation of passenger volume and air crash incidents over the years. The heatmap shows a strong negative correlation between both variables, this can be translated as an increase in passenger volume results to a decrease in crash incidents.'
            fig2_3 = question2_3(d)
            st.pyplot(fig2_3)
            st.caption("Correlation Heatmap: Passenger Volume Since 1945 vs Crash Incidents Since 1945")
            'The negative correlation can be expplainde with the advancements in technology and safety regulations which became more prominent in the evolution of air travel (as demonstrated in Question 1).'

        if st.button("Go to Question 3"):
            '## Question 3: How has the introduction of larger aircrafts impacted the number of fatalities per crash'
            "The chart below shows the trend of ground casualties and air fatalities over the years and how they've changed over the introduction of large aircrafts."
            fig3_1 = question3_1(df, large_aircraft_intro)
            st.pyplot(fig3_1)
            st.caption("Yearly Trend of Ground Casualties and Fatalities in the air")
            'In the chart above, ground casualties stays generally low except from 2001 when the terrorist attack of 9/11 happened. While air fatalities saw an initial rise and then fall in number over the years. The rise in Air fatalities correlate with the early times of air travel, a period during which the world saw the introduction of several new and world-first large passenger airliners like the Douglas DC-3 in 1938, Lockheed Constellation in 1947, Boeing 707 in 1958 and the infamous Boeing 747 (Queen of the Skies) in 1969.'
            'Soon after the early introduction of large aircrafts, more high tech large aircrafts like the famous Concorde (first supersonic passenger airplane), Airbus A380 (king of the skies/largest passenger airplane ever built) and Boeing 787 Dreamliner started entering service, this period correlates with periods of increased regulatory and safety standards along with advancements in air travel technology which aided added safety to air travel, this resulted in the decline of air fatalities and yearly crash incidents over the years (as shown in the chart below).'
            fig3_2 = question1(df, large_aircraft_intro)
            st.pyplot(fig3_2)
            st.caption("Yearly Trend of Crashes")

        if st.button("Go to Question 4"):
            '## Question 4: How has the frequency of airplane crashes changed over key aviation milestones'
            'Seven milestones have been considered in the answering of this question, the chart below shows the trend of each airplane crash incidents with each milestone time stamped with vertical lines.'
            # Generate and display the plot
            fig4_1 = question4_1(df, question_4_milestones)
            st.pyplot(fig4_1)
            st.caption("Yearly Trend of Crashes")
            "The first milestone is the birth of __Commercial Air Travel__ itself in 1914, the frequency of air travel rose after this point reaching it's peak in the 1940s."
            "The second milestone is the advent of __Commercial Jet Airliners__ in 1952. At this time, safety regulations are already taking their places in the world of aviation likely due to the losses and casualties realized from the history of air travel at the time."      
            "In the following year, the world of air travel saw more milestones which contributed to the increase in safety of air travel and the relative down trend of aircraft crash incidents, some of these milestones include the formation of __FAA in USA__ in 1958, the development of __Advanced Navigation Systems__ in 1970. and the implementation of __GPS__ in 1990"
            "The next milestone is the __Introduction of Enhanced Safety Regulations Post 9/11__ in 2001. This milestone -even though it was as a result of the most fatal aircraft crash casualty in history- led to a very stringent air travel policy which has become the standard in the world of air travel, this standard has proven effective in curbing any such threat. The following milestone after this is the __Advent of Automated Safety Systems and Predictive Maintanance Technologies__ in 2005, this tech has proven very effective as air crash incidents have massively declined after this."
            fig4_2 = question4_2(df, question_4_milestones)
            st.pyplot(fig4_2)
            plt.show()
            st.caption("Comparison of Crashes Before and After Key Milestones")
            "This chart above shows the volume crash incidents defore and after key milestones, the chart shows that with every milestone, there is a reduction in the volume of airplane crash incidents."
        if st.button("Go to Question 5"):
            '### Question 5: What is the severity of airplane crashes over time'
            "To figure out this question, let's first look at the volume of fatalities compared to that of survivors over time. The chart below shows just that."
            fig5_1 = question5_1(df)
            # Display the plot
            st.pyplot(fig5_1)
            st.caption("Fatalities vs Survivors in Airplane Crashes by Decade")
            "The stacked bar chart above compares the volume of fatalities and survivors over time and have be categorized into decades. From the chart we can see that both fatalities and survivors had a steady rise up to the 1970s. Noticeably, the margin between fatalities and surviors started dwindling from that point on as air travel became more safe and overall, fatalities per decade saw a downtrend."
            "Noticeably though, the volume of survivors never rose above that of fatalities, this is as a result of the nauture of aircrafts, the overall physics and science of reality at play during flight. Despite being marvels of modern engineering, when things go wrong, they go catastrophically wrong. Unlike many other forms of transportation, airplane accidents often leave little room for survival for example, a malfunction at cruising altitude can translate into a plummet from miles above ground, even when crashes occur during takeoff or landing—statistically the most accident-prone phases of flight—the forces at play tend to overwhelm safety measures. This stark contrast between the marvel of flight and the fatalistic nature of its failures is a sobering reminder of both the limits of engineering and the inherent risks of air travel."
            ""
            question5_2(df)
    elif selected_categories == "**Global Regulations and Safety Standards**":
        "# Global Regulations and Safety Standards"
        ""
        '### Question 1: How has the implementation of internantional safety standards affected airplane crash frequency'
        'To answer this question, we need to look into what the international safety standard is like in the world of aviation.'

        '''
        The core of international aviation safety is governed by ICAO (International Civil Aviation Organization), a UN specialized agency. They establish SARPs (Standards and Recommended Practices) that form the foundation for civil aviation safety worldwide.

        ##### __Key Components of ICAO Includes__:

        * __ICAO Annexes__
        * __Safety Management Systems (SMS)__
        * __Certification Standards__
        * __Regional Regulations__
        * __IATA Operational Safety Audit (IOSA)__
        * __Quality Assurance Programs__
        '''
        'Lets look at the trend of crashes from the beginning and correlate the chart with significant events that took place.'
        # Generate and display the plot
        fig1 = question1(df, question_1_events)
        st.pyplot(fig1)
        st.caption("Yearly Trend of Crashes")
        '''
        The chart depicts the yearly trend of aviation crashes from the early 20th century to 2024. key aviatKon safety milestones are marked with dashed vertical lines and labeled with their respective years:
        * __The Chicago Convention (1944)__: An agreement establishing international aviation standards, likely contributing to an initial stabilization in crash rates.
        * __ICAO Formation (1947)__: Formation of the __International Civil Aviation Organization (ICAO)__.
        * __Major Developments (1960)__: Advancements in aviation technology and safety practices.
        * __Technology Integration (1970)__:  The implementation of advanced navigation and aircraft systems.
        * __Birth of IATA Operational Safety Audit (IOSA) (1974)__: A significant program to enhance operational safety in the aviation industry.
        
        The data indicates a peak in crashes around the mid-20th century, followed by a steady decline. This trend reflects improvements in technology, regulation, and global aviation safety standards. By the 2000s, crash numbers dropped significantly, showcasing the effectiveness of these safety measures.
        '''
    elif selected_categories == "**Air Travel Demand and Infastructure**":
        "# Air Travel Demand and Infastructure"
        'This segment uncovers what effect demand and infastructure have had on the world of air travel'
        '## Question 2: Is there a relationship between the volume of air travel passengers and crash rates over the years'
        'First we need to see the evolution of air travel passenger volume over the years.'
        # Generate the plots
        fig2_1 = question2_1(passenger_volume_data)
        fig2_2 = question2_2(df)
        st.pyplot(fig2_1)
        st.caption("Yearly Trend of Total Passengers in Air Travel Since 1945")
        'The chart above shows that air travel passengers volume rose from practically 0 in 1945 to over 4 billion in 2019, the chart also show a steady growth in passenger volume over the years. It is worth noting the massive dip in 2020 and it can be linked to the COVID-19 pandemic that became wide spread in the same year.'
        ''
        'On the other hand, the chart below shows the trend of air crash incidents since 1945, the chart shows a down trend signifying that crash incidents has been on the decline ever since.'
        st.pyplot(fig2_2)
        st.caption("Yearly Trend of Crashes Since 1945")
        # Create a full range of years
        all_years = pd.RangeIndex(start=min(passenger_volume_data['Year']), stop=max(passenger_volume_data['Year']) + 1)
        # Reindex both Series
        passengers_aboard = passenger_volume_data.groupby('Year')['Passengers'].sum().reindex(all_years, fill_value=0)
        casualties = df[df['Year'] >= 1945]['Year'].value_counts().sort_index().reindex(all_years, fill_value=0)
        # Combine into a DataFrame
        d = pd.DataFrame({
            'Passenger Volume': passengers_aboard,
            'Crash Incidents': casualties
        })
        'The heatmap below shows the correlation of passenger volume and air crash incidents over the years. The heatmap shows a strong negative correlatipon between bothe variables, this can be translated as an increase in passenger volume results to a decrease in crash incidents.'
        fig2_3 = question2_3(d)
        st.pyplot(fig2_3)
        st.caption("Correlation Heatmap: Passenger Volume Since 1945 vs Crash Incidents Since 1945")
        'The negative correlation can be expplainde with the advancements in technology and safety regulations which became more prominent in the evolution of air travel (as demonstrated in Question 1).'

        '## Question 3: How has the introduction of larger aircrafts impacted the number of fatalities per crash'
        "The chart below shows the trend of ground casualties and air fatalities over the years and how they've changed over the introduction of large aircrafts."
        fig3_1 = question3_1(df, large_aircraft_intro)
        st.pyplot(fig3_1)
        st.caption("Yearly Trend of Ground Casualties and Fatalities in the air")
        'In the chart above, ground casualties stays generally low except from 2001 when the terrorist attack of 9/11 happened. While air fatalities saw an initial rise and then fall in number over the years. The rise in Air fatalities correlate with the early times of air travel, a period during which the world saw the introduction of several new and world-first large passenger airliners like the Douglas DC-3 in 1938, Lockheed Constellation in 1947, Boeing 707 in 1958 and the infamous Boeing 747 (Queen of the Skies) in 1969.'
        'Soon after the early introduction of large aircrafts, more high tech large aircrafts like the famous Concorde (first supersonic passenger airplane), Airbus A380 (king of the skies/largest passenger airplane ever built) and Boeing 787 Dreamliner started entering service, this period correlates with periods of increased regulatory and safety standards along with advancements in air travel technology which aided added safety to air travel, this resulted in the decline of air fatalities and yearly crash incidents over the years (as shown in the chart below).'
        fig3_2 = question1(df, large_aircraft_intro)
        st.pyplot(fig3_2)
        st.caption("Yearly Trend of Crashes")
    elif selected_categories == "**Trend in Airplane Crashes Over Time**":
        "# Trend in Airplane Crashes Over Time"
        'This segment exhibits patterns in the trend of aircraft crash events over time.'
        '## Question 4: How has the frequency of airplane crashes changed over key aviation milestones'
        'Seven milestones have been considered in the answering of this question, the chart below shows the trend of each airplane crash incidents with each milestone time stamped with vertical lines.'
        # Generate and display the plot
        fig4_1 = question4_1(df, question_4_milestones)
        st.pyplot(fig4_1)
        st.caption("Yearly Trend of Crashes")
        "The first milestone is the birth of __Commercial Air Travel__ itself in 1914, the frequency of air travel rose after this point reaching it's peak in the 1940s."
        "The second milestone is the advent of __Commercial Jet Airliners__ in 1952. At this time, safety regulations are already taking their places in the world of aviation likely due to the losses and casualties realized from the history of air travel at the time."      
        "In the following year, the world of air travel saw more milestones which contributed to the increase in safety of air travel and the relative down trend of aircraft crash incidents, some of these milestones include the formation of __FAA in USA__ in 1958, the development of __Advanced Navigation Systems__ in 1970. and the implementation of __GPS__ in 1990"
        "The next milestone is the __Introduction of Enhanced Safety Regulations Post 9/11__ in 2001. This milestone -even though it was as a result of the most fatal aircraft crash casualty in history- led to a very stringent air travel policy which has become the standard in the world of air travel, this standard has proven effective in curbing any such threat. The following milestone after this is the __Advent of Automated Safety Systems and Predictive Maintanance Technologies__ in 2005, this tech has proven very effective as air crash incidents have massively declined after this."
        fig4_2 = question4_2(df, question_4_milestones)
        st.pyplot(fig4_2)
        plt.show()
        st.caption("Comparison of Crashes Before and After Key Milestones")
        "This chart above shows the volume crash incidents defore and after key milestones, the chart shows that with every milestone, there is a reduction in the volume of airplane crash incidents."

        '## Question 5: What is the severity of airplane crashes over time'
        "To figure out this question, let's first look at the volume of fatalities compared to that of survivors over time. The chart below shows just that."
        fig5_1 = question5_1(df)
        # Display the plot
        st.pyplot(fig5_1)
        st.caption("Fatalities vs Survivors in Airplane Crashes by Decade")
        "The stacked bar chart above compares the volume of fatalities and survivors over time and have be categorized into decades. From the chart we can see that both fatalities and survivors had a steady rise up to the 1970s. Noticeably, the margin between fatalities and surviors started dwindling from that point on as air travel became more safe and overall, fatalities per decade saw a downtrend."
        "Noticeably though, the volume of survivors never rose above that of fatalities, this is as a result of the nauture of aircrafts, the overall physics and science of reality at play during flight. Despite being marvels of modern engineering, when things go wrong, they go catastrophically wrong. Unlike many other forms of transportation, airplane accidents often leave little room for survival for example, a malfunction at cruising altitude can translate into a plummet from miles above ground, even when crashes occur during takeoff or landing—statistically the most accident-prone phases of flight—the forces at play tend to overwhelm safety measures. This stark contrast between the marvel of flight and the fatalistic nature of its failures is a sobering reminder of both the limits of engineering and the inherent risks of air travel."
        ""
        question5_2(df)
        ""



# Run the app
if __name__ == "__main__":
    main()
