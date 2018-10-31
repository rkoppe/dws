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

# access a properties of a sensor
meta$map$`station:heluwobs:fb_730201:sbe38_9999a:Temperature`$properties$range
meta$map[["station:heluwobs:fb_730201:sbe38_9999a:Temperature"]]$properties$range


