library(ggplot2)
library(plyr)
library(ggthemes)

df_2013 <- read.csv(file.choose(),header=TRUE)
df_2014 <- read.csv(file.choose(),header=TRUE)
df_2015 <- read.csv(file.choose(),header=TRUE)

df_year_built_13 <- count(df_2013,"YEAR.BUILT.")
df_year_built_14 <- count(df_2014,"YEAR.BUILT.")
df_year_built_15 <- count(df_2015,"YEAR.BUILT.")

df_building_class_13 <- count(df_2013,"BUILDING.CLASS.AT.PRESENT.")
df_building_class_14 <- count(df_2014,"BUILDING.CLASS.AT.PRESENT.")
df_building_class_15 <- count(df_2015,"BUILDING.CLASS.AT.PRESENT.")

df_address_13 <- count(df_2013,"ADDRESS.") 
df_address_14 <- count(df_2014,"ADDRESS.")
df_address_15 <- count(df_2015,"ADDRESS.")

df_zip_13 <- count(df_2013,"ZIP.CODE.")
View(df_zip_13)
df_zip_13$ZIP.CODE. <- as.factor(df_zip_13$ZIP.CODE.)

ggplot(data=df_zip_13, aes(x=ZIP.CODE., y=freq)) +
geom_bar(stat="identity") +
theme_tufte() +
theme(axis.text.x = element_text(angle = 45, hjust = 1))


df_validate <- subset(df_2013, df_2013$NEIGHBORHOOD. == "Chelsea")

df_r4_13 <- subset(df_2013,df_2013$BUILDING.CLASS.AT.PRESENT. == "R4")
df_r4_13 <- df_r4_13[, c("BUILDING.CLASS.AT.PRESENT.", "BUILDING.CLASS.CATEGORY.")]
View(df_r4_13)

#year built vs no of sales scatter plot
ggplot(df_year_built_13, aes(x=YEAR.BUILT., y=freq)) +
geom_point() + 
geom_smooth() +
ylim(0, 1300) +
xlim(1830,2020)

ggplot(df_year_built_14, aes(x=YEAR.BUILT., y=freq)) +
  geom_point() + 
  geom_smooth() +
  ylim(0, 1300) +
  xlim(1830,2020)

ggplot(df_year_built_15, aes(x=YEAR.BUILT., y=freq)) +
  geom_point() + 
  geom_smooth() +
  ylim(0, 1300) +
  xlim(1830,2020)


#building class vs no of sales bar chart
df_building_class_13 <- df_building_class_13[complete.cases(df_building_class_13), ]
df_building_class_14 <- df_building_class_14[complete.cases(df_building_class_13), ]
df_building_class_15 <- df_building_class_15[complete.cases(df_building_class_132), ]


ggplot(df_building_class) + 
geom_bar( aes(x=BUILDING.CLASS.AT.PRESENT.))




agevsales <- subset(df_2013,select = c(df_2013$YEAR.BUILT.))
aggregated_data <-aggregate(df_2013, by=list(cyl,vs), FUN=mean, na.rm=TRUE)

View(df_2013)
View(df_2014)

View(df_year_built_13)
View(df_building_class_13)

View(df_address_13)
View(df_address_14)
View(df_address_15)

write.csv(df_building_class_13, file = "classcount.csv")
