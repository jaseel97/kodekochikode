data<-read.csv(file.choose(), header= TRUE)

data1<-data.frame(NEIGHBOURHOOD = data$NEIGHBORHOOD.,MONTH = data$MONTH,PRICE = data$X.SALE.PRICE.)
View(data1)

#Removing NA costs
data1<-na.omit(data1)

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


