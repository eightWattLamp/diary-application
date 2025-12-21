# Diary application

## An application for tracking personal daily behaviour based on custom variables.

The aim of the application is to generate daily surveys for the user based on the behaviours or variables to be tracked. The variables are first created by the user, with name and type of the variable specified. For example, the following three variables with corresponding types can be created:

* cups_of_water: numeric
* hours_slept: numeric
* ate_breakfast: categorical (yes, no)

Then, the application generates daily surveys for the user. In each survey, the user indicates the values of variables on a specific day (eg. how many cups of water they drank today, how much sleep they got, did they eat breakfast). There are only two types of variables: numeric and categorical. The example above for a categorical variable (ate_breakfast) has two categories (yes or no). However, when creating a categorical variable, any number of categories can be specified (though, I would not recommend having more than 6 categories, in such a case, a numeric variable would be more convenient to use). The names of each category are also specified by the user. By default, all the variables created are active, which means that they are included in the surveys. However, the user can inactivate certain variables if they want the surveys to not include them. In this way, old data about some variables can be saved, and the inactivated variables can be activated later to continue collecting data. Each variable can also be renamed or deleted. The data from all the surveys can be exported as a .csv file, which can be directly opened in R as a dataframe, to perform data analysis.

The bigger puprose of this application is not only to provide a way for users to track their daily behaviour, but to also give a comprehensive export system that would allow the data to be analysed. The results of data analysis can further be used to find out how daily behaviour affects certain aspects of life. For example, how late meals impact the duration of sleep or how amount of water drank influences the mood. Currently, the application can only record and exprot the data, but not work with it. At the moment, the exports from the application can be analysed with R, if one has sufficient knowledge and skills. Future updates will focus on implementing data analysis within the application by using pandas library.

## Installation instructions

1. Download and unarchive this project
2. Inside the main directory, "app_1.1", expand all directories.
3. In the following paths:
    * app_1.1 > variables > inactive
    * app_1.1 > variables > active
    * app_1.1 > export
    You will find files named "dummy_file.csv" (3 files with this name in total). Delete all 3 dummy files, without changing the folder structure.
4. Open the application script named "Application.py" and run it with a regular python compiler.

## Checkout the video installation instructions and a preview

https://helsinkifi-my.sharepoint.com/:v:/g/personal/gorsandr_ad_helsinki_fi/IQBkIWDfO0_6RqPBTE8v4i_hAZtKWQA4Gmfw6ncmizyNwto?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=3Pbwp2
