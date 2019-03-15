my_data<-read.csv(file.choose(),header=TRUE)
summary(my_data)
View(my_data)

#Remove unnecessary columns
my_data$ï..BOROUGH. = NULL
my_data$EASE.MENT.= NULL
my_data$RESIDENTIAL.UNITS. = NULL
my_data$COMMERCIAL.UNITS. = NULL
my_data$TOTAL.UNITS.= NULL
my_data$APARTMENT.NUMBER.=NULL
my_data$LAND.SQUARE.FEET.=NULL
my_data$GROSS.SQUARE.FEET.=NULL
my_data$X.SALE.PRICE..=NULL

#(un)factorize necessary columns
my_data$ZIP.CODE.<-as.factor(my_data$ZIP.CODE.)
my_data$TAX.CLASS.AT.TIME.OF.SALE.<-as.factor(my_data$TAX.CLASS.AT.TIME.OF.SALE.)

my_data$SALE.PRICE.<-gsub("$","",my_data$SALE.PRICE.,fixed=TRUE)
my_data$SALE.PRICE.<-as.numeric(gsub(",","",my_data$SALE.PRICE.,fixed=TRUE))

my_data$X.SALE.PRICE.<-gsub("$","",my_data$X.SALE.PRICE.,fixed=TRUE)
my_data$X.SALE.PRICE.<-as.numeric(gsub(",","",my_data$X.SALE.PRICE.,fixed=TRUE))
 
#Fixing invalid entries
my_data$SALE.PRICE.[my_data$SALE.PRICE.<2992]<-2992  #10% of 2nd quarternary
my_data$YEAR.BUILT.[my_data$YEAR.BUILT.== 0]<-as.integer(mean(my_data$YEAR.BUILT.[my_data$YEAR.BUILT.!= 0]))

#Adding month column
my_data$MONTH<-format(as.Date(my_data$SALE.DATE.),"%m")
my_data$MONTH<-as.numeric(as.character(my_data$MONTH))

library(lubridate)
my_data$MONTH<-month(as.POSIXlt(my_data$SALE.DATE., format="%m-%d-%Y"))


#ZIP or NEIGHBOURHOOD??
length(unique(my_data$NEIGHBORHOOD.))
length(unique(my_data$ZIP.CODE.))

#Number of sales per Month
length(which(my_data$MONTH == 6))

#Tax Class Summary
summary(my_data$TAX.CLASS.AT.TIME.OF.SALE.)
mean(my_data$SALE.PRICE.[my_data$TAX.CLASS.AT.TIME.OF.SALE. == 2])
mean(my_data$SALE.PRICE.[my_data$TAX.CLASS.AT.TIME.OF.SALE. == 1])
mean(my_data$SALE.PRICE.[my_data$TAX.CLASS.AT.TIME.OF.SALE. == 4])
length(my_data$YEAR.BUILT.[my_data$YEAR.BUILT.<=1900])


write.csv(my_data, "2013.csv")
