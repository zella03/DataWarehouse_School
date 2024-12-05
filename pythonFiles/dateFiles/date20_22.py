import pandas as pd

listDates20_22 = []

def datesGen(startDate, endDate):
    dates = pd.DataFrame()
    dates["dates"] = pd.date_range(start=startDate, end=endDate)
    dates["day_of_week"] = dates["dates"].dt.day_name()
    dates = dates[dates["dates"].dt.dayofweek < 5]
    dates = dates[~dates["dates"].dt.month.isin([7, 8])]

    return dates

with open("pythonFiles/dateFiles/dateGen20_22.txt", "w+", encoding="UTF-8") as file:
    listDates20_22.append(datesGen("2020-09-01", "2022-06-30"))

    two_dimensional_list = listDates20_22[0].values.tolist()
    date_strings = [[str(date).split()[0] for date in row] for row in two_dimensional_list]
    output_string = "\n".join([",".join(map(str, row)) for row in date_strings])

    file.write(output_string)