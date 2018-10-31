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
  meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range$lower < data$station.heluwobs.fb_730201.sbe38_9999a.temperature..Â.C. &&
  meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range$upper > data$station.heluwobs.fb_730201.sbe38_9999a.temperature..Â.C.


