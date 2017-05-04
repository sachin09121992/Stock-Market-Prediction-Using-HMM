#Loading the required packages
require(fpp)
require(fma)

#Loading the dataset
myData=read.csv(file.choose())

######################################################################################################################################
#Fetching close price only for stock AA and converting it to a time series
mydata=myData[myData$stock=="AA",]
data=ts(mydata$close)
actualAA=data[25]
data=data[1:24]

#Plotting  time series data to find any unusual patterns
plot(data)
  
#Applying the Box-Cox Transformation to stabilize the variance
lambda=BoxCox.lambda(data)
stabilizedData=BoxCox(data,lambda)
plot(stabilizedData)
  
#Plotting the results of the ACF function to check if the stabilizedData is stationary or not
plot(acf(stabilizedData))
#We do not need to apply differencing because the acf values are quickly dropping and hence the data is stationary
  
#Developing the ARIMA model
autoArimaModel = auto.arima(stabilizedData)
  
#Examining the residuals of autoArimaModel to find whether it behaves like a noise or not
plot(acf(residuals(autoArimaModel)))
BoxTestResult=Box.test(residuals(autoArimaModel), fitdf = 0)
#print("The p-value obtained by Box-Test is:")
#print(BoxTestResult$p.value)
#As it can be seen by the ACF plot that all the values are within the critical value(95% confidence value), therefore the residuals are white noise 
#It is also evident from the Box Test that the residuals are white noise as the p-value is: 0.9344128>0.05, which is insignificant
# As a result of both these observation, residuals are white noise
  
#Forecasting using ARIMA model
result=forecast(object=autoArimaModel,lambda=lambda)
predicted=result$mean[1]
errorAA=(abs(predicted-actualAA))/(actualAA)
print(errorAA)

#####################################################################################################################################
#Fetching close price only for stock AXP and converting it to a time series
mydata=myData[myData$stock=="AXP",]
data=ts(mydata$close)
actualAXP=data[25]
dataAXP=data[1:24]

#Plotting the electric equipment time series data to find any unusual patterns
plot(dataAXP)


#Plotting the results of the ACF function to check if the transformedData is stationary or not
plot(acf(dataAXP))
#As the Acf values are decreasing slowly, the transformedData is non-stationary
#We need to apply the Unit Root Test to find the order of differencing required to make it stationary in next step

#Applying the Unit Root Test to determine the order of differencing required
#nd=ndiffs(dataAXP)
#if(nd>0){
#  transformedAXP=diff(dataAXP, differences = nd)
#}
#plot(transformedAXP)
#plot(acf(transformedAXP))
#It can be seen from above plot that the transformed time series obtained after Differencing is stationary since the values of ACF plot decrease to 0 very quickly 

#Developing the ARIMA model
autoArimaModelAXP = auto.arima(dataAXP)

#Examining the residuals of autoArimaModel to find whether it behaves like a noise or not
plot(acf(residuals(autoArimaModelAXP)))
BoxTestResultAXP=Box.test(residuals(autoArimaModelAXP), fitdf = 0)
#print("The p-value obtained by Box-Test is:")
#print(BoxTestResultAXP$p.value)
#As it can be seen by the ACF plot that all the values are within the critical value(95% confidence value), therefore the residuals are white noise 
#It is also evident from the Box Test that the residuals are white noise as the p-value is: 0.9344128>0.05, which is insignificant
# As a result of both these observation, residuals are white noise

#Forecasting using ARIMA model
resultAXP=forecast(object=dataAXP,model=autoArimaModelAXP)
plot(resultAXP)
predictedAXP=resultAXP$mean[1]
errorAXP=(abs(predictedAXP-actualAXP))/(actualAXP)
print(errorAXP)
#######################################################################################################################################
#Fetching close price only for stock BA and converting it to a time series
mydata=myData[myData$stock=="BA",]
data=ts(mydata$close)
actualBA=data[25]
dataBA=ts(data[1:24])

#Plotting  time series data to find any unusual patterns
plot(dataBA)

#Plotting the results of the ACF function to check if the transformedData is stationary or not
plot(acf(dataBA))
#The transformed data is stationary

#Developing the ARIMA model
autoArimaModelBA = auto.arima(dataBA)

#Examining the residuals of autoArimaModel to find whether it behaves like a noise or not
plot(acf(residuals(autoArimaModelBA)))
BoxTestResultBA=Box.test(residuals(autoArimaModelBA), fitdf = 0)
#print("The p-value obtained by Box-Test is:")
#print(BoxTestResultBA$p.value)
#As it can be seen by the ACF plot that all the values are within the critical value(95% confidence value), therefore the residuals are white noise 


#Forecasting using ARIMA model
resultBA=forecast(object=dataBA,model=autoArimaModelBA)
plot(resultBA)
predictedBA=resultBA$mean[1]
errorBA=(abs(predictedBA-actualBA))/(actualBA)
print(errorBA)
###############################################################################################################################################
#Fetching close price only for stock BAC and converting it to a time series
mydata=myData[myData$stock=="BAC",]
data=ts(mydata$close)
actualBAC=data[25]
dataBAC=ts(data[1:24])

#Plotting  time series data to find any unusual patterns
plot(dataBAC)

#Applying the Box-Cox Transformation to stabilize the variance
lambdaBAC=BoxCox.lambda(dataBAC)
transformedBAC=BoxCox(dataBAC,lambdaBAC)
plot(transformedBAC)

#Plotting the results of the ACF function to check if the transformedBAC is stationary or not
plot(acf(transformedBAC))
#The ACFplot tells us that the data is stationary


#Developing the ARIMA model
autoArimaModelBAC = auto.arima(transformedBAC)

#Examining the residuals of autoArimaModel to find whether it behaves like a noise or not
plot(acf(residuals(autoArimaModelBAC)))
BoxTestResultBAC=Box.test(residuals(autoArimaModelBAC), fitdf = 0)
#print("The p-value obtained by Box-Test is:")
#print(BoxTestResultBAC$p.value)
#As it can be seen by the ACF plot that all the values are within the critical value(95% confidence value), therefore the residuals are white noise 


#Forecasting using ARIMA model
resultBAC=forecast(object=autoArimaModelBAC,lambda=lambdaBAC)
plot(resultBAC)
predictedBAC=resultBAC$mean[1]
errorBAC=(abs(predictedBAC-actualBAC))/(actualBAC)
print(errorBAC)
#######################################################################################################################################
error=(errorAA+errorAXP+errorBA+errorBAC)/4
print(error)