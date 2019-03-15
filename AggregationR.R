data<-read.csv(file.choose(), header= TRUE)
View(data)
data1<-data.frame(NEIGHBOURHOOD = data$NEIGHBORHOOD.,MONTH = data$MONTH,PRICE = data$SALE.PRICE.)
View(data1)
summary(data1)

#Removing NA costs
data1<-na.omit(data1)

#0 price values
length(data1$PRICE[data1$PRICE==0])
data1<-subset(data1,data1$PRICE!=0)


#agg = aggregate(data1$PRICE~data1$MONTH+data1$NEIGHBOURHOOD,data1,FUN = function(x) c(mn = mean(x), length(x))) 

#Aggregates for mean and count of real estate transactions per Month for each Neighbourhood
agg_count = aggregate(data1$PRICE~data1$MONTH+data1$NEIGHBOURHOOD,data1, length)
agg_mean = aggregate(data1$PRICE~data1$MONTH+data1$NEIGHBOURHOOD,data1, mean)

View(agg_mean)
View(agg_count)

#Clubbing together
agg_final<-agg_mean
agg_final$Count <- agg_count$`data1$PRICE`
colnames(agg_final)<- c("Month", "Neighbourhood", "Mean", "Count")
View(agg_final)
agg_final$Month+12

agg2014$Month<-agg2014$Month+12
agg2015$Month<-agg2015$Month+24
agg2016$Month<-agg2016$Month+36
agg2017$Month<-agg2017$Month+48

#Year-wise month padding
agg2013<-agg_final
agg2014<-agg_final
agg2015<-agg_final
agg2016<-agg_final
agg2017<-agg_final
View(agg2014)

agg_finalf<-rbind(agg2013, agg2014)
agg_finalf<-rbind(agg_finalf, agg2017)
View(agg_finalf)
write.csv(agg_finalf,"AggAll.csv")


