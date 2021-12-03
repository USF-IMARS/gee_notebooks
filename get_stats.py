"""
Function to get mean values.
"""
def get_stats(img):
    """
    Select and rename bands.
    
    Parameters:
    -----------
    img : ee.Image
        the image to get values from.
        
    Returns:
    --------
    ee.Feature
        object w/ the mean and std dev set on the feature
    """
    #image = ee.Image(img).select(band+'_mean').rename(renameBand)
    image = ee.Image(img).rename(renameBand)
    ## Create and combine reducers of mean and std.
    reducers = ee.Reducer.mean().combine(
        reducer2= ee.Reducer.stdDev(),
        sharedInputs= True)
    ## Apply reducers to the image.
    stats = image.reduceRegion(
        reducer= reducers,
        geometry= region,
        #bestEffort= True,
        scale= 1000,
        maxPixels= 1e9)
    
    ## Create feature variable to allocate data.
    feature = ee.Feature(None)
    ## Set properties of interest.
    properties = ['system:index','month','year',renameBand+'_mean',renameBand+'_stdDev']
    ## Apply the stats on every image and collect the output.
    imageStats = image.setMulti(stats)
    ## return feature with the selected properties.
    return ee.Feature(feature).copyProperties(imageStats, properties)