
import pandas as pd
import streamlit as st
import pymysql
import sqlalchemy as sqlalchemy
from sqlalchemy import create_engine

Connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='Tommy039',
    database='myproject1db'
    )
host='localhost'
port=3306
user='root'
password='Tommy039'
database='myproject1db'

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

all_queries ={ 
'1. Top 10 strongest earthquakes (mag)':"""select * from earthquake order by mag desc limit 10;""",
'2. Top 10 deepest earthquakes (depth_km)':"""select * from earthquake order by depth_km desc limit 10;""",
'3. Shallow earthquakes < 50 km and mag > 7.5':"""select * from earthquake where depth_km<50 and mag>7.5;""",
'5. Average magnitude per magnitude type (magType)':"""select magType,avg(depth_km) as avg_magtype from earthquake group by magType;""",
'6. Year with most earthquakes':"""select year, COUNT(*) as max_count from earthquake group by year
ORDER BY max_count DESC limit 1;""",
'7. Month with highest number of earthquakes':"""select monthname(time),count(*) as count from earthquake group by monthname(time) 
order by count(*) desc limit 1;""",
'8. Day of week with most earthquakes':"""select dayofweek(time),count(*) as count from earthquake group by dayofweek(time) 
order by count(*) desc limit 1;""",
'9. Count of earthquakes per hour of day':"""select hour(time) as hour,count(*) as count from earthquake group by hour(time) 
order by hour;""",
'10. Most active reporting network (net)':"""select net as network ,count(*) as count from earthquake group by net 
order by count desc limit 1;""",
'11. Top 5 places with highest casualties':"""select country, max(felt) as casualties from earthquake group by country 
order by casualties desc limit 5;""",
'13. Average economic loss by alert level':"""select country,count(type) as eco_loss from earthquake group by country 
order by eco_loss desc;""",
'14. Count of reviewed vs automatic earthquakes (status)':"""select alert, count(*) as avg_eco_loss from earthquake group by alert having alert <>"" 
order by avg_eco_loss desc;""",
'15. Count by earthquake type (type)':"""select status,count(*) as count from earthquake group by status;""",
'16. Number of earthquakes by data type (types)':"""select type,count(*) as count from earthquake group by type;""",
'18. Events with high station coverage (nst > threshold)':"""select type, AVG(nst) AS Threshold from Earthquake
group by type having AVG(nst) > (select AVG(nst) FROM Earthquake);""",
'19. Number of tsunamis triggered per year':"""select year(time), sum(tsunami) as no_of_tsunami from earthquake group by year(time) 
order by no_of_tsunami desc;""",
'20. Count earthquakes by alert levels (red, orange, etc.)':"""select alert,count(*) as count from earthquake group by alert order by count desc;""",
'21.Find the top 5 countries with the highest average magnitude of earthquakes in the past 5 years':
"""select country, avg(mag) from earthquake group by country order by avg(mag) 
desc limit 5;""",
'22. Find countries that have experienced both shallow and deep earthquakes within the same month':
"""SELECT country, year(time), depth_flag, MONTHNAME(time) as month_name from Earthquake 
group by country,year(time), depth_flag, MONTHNAME(time) 
having sum(depth_km<=100)>0 and sum(depth_km>100)>0;""",
'23. Compute the year-over-year growth rate in the total number of earthquakes globally':
"""SELECT year,COUNT(*) AS total_quakes,
LAG(COUNT(*)) OVER (ORDER BY year) AS prev_year_quakes,
ROUND((COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY year)) / LAG(COUNT(*)) OVER (ORDER BY year) * 100,2) 
as yoy_growth_percent from Earthquake
group by year order by year;""",
'24. List the 3 most seismically active regions by combining both frequency and average magnitude':
"""SELECT country, count(type) as Frequency, avg(mag) as avg_mag,
(count(type)*avg(mag)) as active from Earthquake 
group by country order by active desc limit 3;""",
'25. For each country, calculate the average depth of earthquakes within ±5° latitude range of the equator':
"""select country, avg(depth_km) as avg_depth from earthquake where latitude between -5 and 5 
group by country;""",
'26. Identify countries having the highest ratio of shallow to deep earthquakes':
"""select country, sum(depth_km<=100) as shallow, sum(depth_km>100) as deep, 
ifnull(sum(depth_km<=100) / nullif(sum(depth_km>100),0),0) as ratio 
from earthquake group by country order by ratio desc;""",
'27. Find the average magnitude difference between earthquakes with tsunami alerts and those without':
"""select (select avg(mag) from earthquake where tsunami=1)-
(select avg(mag) from earthquake where tsunami=0) as avg_mag_diff;""",
'28. Using the gap and rms columns, identify events with the lowest data reliability (highest average error margins)':
"""select * from earthquake order by gap desc, rms desc limit 20;""",
'30. Determine the regions with the highest frequency of deep-focus earthquakes (depth > 300 km)':
"""select place, count(*) as frequency, depth_km as Depth from earthquake where depth_km>300 
group by place,depth_km order by count(*) desc;"""
}


# Streamlit UI
# --------------------------------------
st.title("🌍 Earthquake Data Analysis Dashboard")
st.write("Select any problem statement (1–30) to run the corresponding SQL query")

# Dropdown
task = st.selectbox("Choose Task Number", list(all_queries.keys()))

# Run button
if st.button("Run Query"):
    query = all_queries[task]
    df = pd.read_sql(query, engine)
    
    st.subheader(f"Results for: {task}")
    st.dataframe(df, use_container_width=True)





