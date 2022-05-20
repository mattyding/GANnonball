import preprocessing
import postprocessing

data = preprocessing.loadData()

midi = postprocessing.vecToMidi(data[0])