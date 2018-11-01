# dws test requests

source("dws.R")

# get sensors
sensors <- dws.sensors()

# search for sensors
sensors <- dws.sensors("station:helu*")

# get sensor information
sensor <- dws.sensor("station:svluwobs:svluw2:ctd_181:temperature_sensor_01:Temperature")


# get json metadata
platform <- dws.platform("station:heluwobs:deko")
meta <- dws.meta.json("station:heluwobs:deko")
meta <- dws.meta.json("station:heluwobs:deko", pretty = TRUE)
meta


# get SensorML metadata
meta <- dws.meta.sensorML("station:heluwobs:deko")
meta


# get metadata prepared for R
#t <- fromJSON(dws.meta.json("station:heluwobs"))
meta <- dws.meta("station:heluwobs:deko")
meta

# access properties of a sensor
meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range
meta$map[["station:heluwobs:fb_730201:sbe38_9999a:Temperature"]]$properties$range


# use case: find sensor, get data, see metadata
sensors <- dws.sensors("station:helu*temp*")
data <- dws.get("station:heluwobs:fb_730201:sbe38_9999a:temperature", begin = "2018-10-01", end = "2018-10-31", aggregate = "second")
meta <- dws.meta("station:heluwobs")
data$flag_in_range <-
  meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range$lower < data$station.heluwobs.fb_730201.sbe38_9999a.temperature...C. &&
  meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range$upper > data$station.heluwobs.fb_730201.sbe38_9999a.temperature...C.



source("dws.R")
sensor <- dws.sensor("station:svluwobs:svluw2:ctd_181:temperature_sensor_01:Temperature")
sensor



data <- dws.get("station:svluwobs:svluw2:ctd_181:temperature", begin="2018-10-15", end="2018-11-05")
meta <- dws.meta("station:svluwobs")

range <- meta$map$`station:svluwobs:svluw2:ctd_181:temperature_sensor_01:temperature`$properties$local_range
range

spike <- meta$map$`station:svluwobs:svluw2:ctd_181:temperature_sensor_01:temperature`$properties$crit_spike_value
spike

data$range_check <- 
  range$lower < data$station.svluwobs.svluw2.ctd_181.temperature..mean....C. &&
  range$upper > data$station.svluwobs.svluw2.ctd_181.temperature..mean....C.





sensors <- dws.sensors("station:svluwobs:svluw2:ctd_181*")
sensors

data <- dws.get(
  c("station:svluwobs:svluw2:ctd_181:temperature", "station:svluwobs:svluw2:ctd_181:pressure"),
  begin="2018-10-01",
  end="2018-11-05",
  aggregate = "hour")
head(data)

library(ggplot2)
library(scales)

data$timestamp <- as.POSIXct(data$datetime, format = "%Y-%m-%dT%H:%M:%S")
gg <- ggplot(data, aes(x = timestamp, y = -station.svluwobs.svluw2.ctd_181.pressure..mean...dbar.)) +
  geom_point(aes(col = station.svluwobs.svluw2.ctd_181.temperature..mean....C.)) +
  labs(x = "datetime", y = "~ depth [m]", "ok") +
#  scale_color_gradient(low = "blue", mid = "green", high = "red")
#  scale_color_gradientn(colors = c("blue","red"), name = "temperature")
  scale_color_gradientn(colors = rev(rainbow(5)), name = "temperature [°C]") +
  scale_x_datetime(labels = date_format("%Y-%m-%d"), date_breaks = "7 days") 
#  coord_fixed(ratio =1)
options(repr.plot.width=10, repr.plot.height=8)
plot(gg)